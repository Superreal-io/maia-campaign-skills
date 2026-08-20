#!/usr/bin/env python3
"""
generate_image.py: genera fotografia de marca con OpenAI (gpt-image-2 por defecto).

Dos modos:

  1. TEXTO -> IMAGEN  (endpoint /v1/images/generations)
     Sin referencias. Igual que la version anterior.

  2. REFERENCIA + TEXTO -> IMAGEN  (endpoint /v1/images/edits)
     Con una o varias imagenes de referencia via --ref. El modelo toma composicion,
     luz y codigo visual de las referencias, y el contenido del prompt. Es el modo
     recomendado para piezas de marca: los Gold Standards transmiten lo que el
     prompt no puede describir.

Lee la API key de la variable de entorno OPENAI_API_KEY.
Nunca pongas la clave en claro en config, prompts ni codigo.

El prompt debe venir YA escrito en estilo Magic Prompt (ver guidelines/magic-prompt.md):
4-5 frases cinematograficas en ingles, realismo editorial Movistar. Este script no
reescribe el prompt, solo lo envia.

Uso:
  # sin referencias (modo clasico)
  python3 scripts/generate_image.py -p "A warm morning kitchen scene..." -o out/hero.png --aspect 3:2

  # con Gold Standards como referencia (modo recomendado)
  python3 scripts/generate_image.py -p "A warm morning kitchen scene..." \
      -o out/hero.png --aspect 3:2 \
      --ref gold-standards/email/email-claro-dispositivos.png \
      --ref gold-standards/email/email-foto-futbol.png

  # verificar la peticion sin gastar credito
  python3 scripts/generate_image.py -p "..." -o out/hero.png --ref a.png --dry-run

Aspect ratios preconfigurados (todos multiplos de 16, respetan ratio max 3:1):
  1:1  -> 1024x1024
  2:3  -> 1024x1536      (MUPI, valla vertical, story, cartel A3)
  3:2  -> 1536x1024      (email hero, banner horizontal)
  3:4  -> 1152x1536      (portrait 3:4)
  4:3  -> 1536x1152      (landscape 4:3)
  9:16 -> 1152x2048      (story vertical 2K)
  16:9 -> 2048x1152      (landscape 2K, Movistar+)
  4K-portrait  -> 2160x3840
  4K-landscape -> 3840x2160

Puedes forzar cualquier tamano con --size WxH (ambos multiplos de 16, max 3840px por lado,
total entre 655.360 y 8.294.400 pixeles, ratio max 3:1).

Modelos disponibles (via --model o env OPENAI_IMAGE_MODEL):
  gpt-image-2 (por defecto, state-of-the-art, acepta imagenes de entrada)
  gpt-image-1.5
  gpt-image-1
  gpt-image-1-mini

Calidad (via --quality o env OPENAI_IMAGE_QUALITY):
  low | medium | high | auto (por defecto)

Sobre las referencias:
  - EL ORDEN IMPORTA. La primera referencia de la lista conserva el detalle mas fino
    y la textura mas rica; las siguientes influyen menos. Pon primero la que mas se
    parezca a lo que quieres conseguir. Si hay caras en juego, la de las caras va primera.
  - Maximo 16 por peticion (limite de la API). Recomendado 2-3: mas referencias
    diluyen la senal y encarecen la llamada, porque las imagenes de entrada se
    facturan como tokens. Con gpt-image-2 las entradas se procesan siempre en alta
    fidelidad, asi que cada referencia extra cuesta de verdad.
  - Formatos aceptados: PNG, JPEG, WEBP. Maximo 25 MB por archivo.
  - Las referencias transmiten composicion, luz, jerarquia y codigo de marca.
    El prompt sigue describiendo la ESCENA. No escribas "en el estilo de la
    referencia": describe lo que quieres ver y deja que la referencia haga su trabajo.

Sin dependencias externas: usa urllib de la libreria estandar.
"""
import argparse
import base64
import json
import mimetypes
import os
import secrets
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-2")
DEFAULT_QUALITY = os.environ.get("OPENAI_IMAGE_QUALITY", "auto")
ENDPOINT_GENERATE = "https://api.openai.com/v1/images/generations"
ENDPOINT_EDIT = "https://api.openai.com/v1/images/edits"

MAX_REFS = 16
WARN_REFS = 4
MAX_REF_BYTES = 25 * 1024 * 1024   # limite de la API por imagen de entrada
ALLOWED_REF_EXT = {".png", ".jpg", ".jpeg", ".webp"}

ASPECT_TO_SIZE = {
    "1:1":          "1024x1024",
    "2:3":          "1024x1536",
    "3:2":          "1536x1024",
    "3:4":          "1152x1536",
    "4:3":          "1536x1152",
    "9:16":         "1152x2048",
    "16:9":         "2048x1152",
    "4K-portrait":  "2160x3840",
    "4K-landscape": "3840x2160",
    "auto":         "auto",
}


def validate_size(size: str) -> str:
    if size == "auto":
        return size
    try:
        w, h = [int(x) for x in size.lower().split("x")]
    except Exception:
        sys.exit(f"ERROR: --size invalido '{size}'. Formato esperado: WxH (ej 2048x1152)")
    if w % 16 or h % 16:
        sys.exit(f"ERROR: ambos lados deben ser multiplos de 16 ({w}x{h})")
    if max(w, h) > 3840:
        sys.exit(f"ERROR: lado maximo 3840px ({w}x{h})")
    total = w * h
    if total < 655_360 or total > 8_294_400:
        sys.exit(f"ERROR: pixeles totales {total} fuera de [655360, 8294400]")
    ratio = max(w, h) / min(w, h)
    if ratio > 3.0:
        sys.exit(f"ERROR: ratio {ratio:.2f} excede 3:1")
    return f"{w}x{h}"


def validate_refs(paths):
    """Comprueba que las referencias existen, tienen formato valido y no exceden el limite."""
    resolved = []
    for raw in paths:
        p = Path(raw)
        if not p.exists():
            sys.exit(f"ERROR: referencia no encontrada: {raw}\n"
                     f"       Las rutas son relativas al directorio desde el que ejecutas "
                     f"el script (cwd actual: {Path.cwd()})")
        if not p.is_file():
            sys.exit(f"ERROR: la referencia no es un archivo: {raw}")
        if p.suffix.lower() not in ALLOWED_REF_EXT:
            sys.exit(f"ERROR: formato de referencia no soportado '{p.suffix}' en {raw}. "
                     f"Usa PNG, JPG o WEBP")
        size = p.stat().st_size
        if size == 0:
            sys.exit(f"ERROR: la referencia esta vacia: {raw}")
        if size > MAX_REF_BYTES:
            sys.exit(f"ERROR: la referencia pesa {size // (1024*1024)} MB y el maximo de la API "
                     f"es 25 MB: {raw}\n"
                     f"       Normalizala a JPEG q90 con lado largo 1536 px "
                     f"(ver references/gold-standards/INDEX.md)")
        resolved.append(p)

    if len(resolved) > MAX_REFS:
        sys.exit(f"ERROR: {len(resolved)} referencias, el maximo de la API es {MAX_REFS}")
    if len(resolved) > WARN_REFS:
        print(f"AVISO: {len(resolved)} referencias. Recomendado 2-3: mas diluyen la senal "
              f"y encarecen la llamada.", file=sys.stderr)
    return resolved


def build_multipart(fields, files):
    """
    Construye un cuerpo multipart/form-data sin dependencias externas.

    fields: dict de campos de texto  {nombre: valor}
    files:  lista de tuplas (nombre_campo, Path)
    Devuelve (body_bytes, content_type_header)
    """
    boundary = "----MovistarBoundary" + secrets.token_hex(16)
    crlf = b"\r\n"
    parts = []

    for name, value in fields.items():
        if value is None:
            continue
        parts.append(b"--" + boundary.encode())
        parts.append(f'Content-Disposition: form-data; name="{name}"'.encode("utf-8"))
        parts.append(b"")
        parts.append(str(value).encode("utf-8"))

    for field_name, path in files:
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        parts.append(b"--" + boundary.encode())
        parts.append(
            f'Content-Disposition: form-data; name="{field_name}"; filename="{path.name}"'
            .encode("utf-8")
        )
        parts.append(f"Content-Type: {ctype}".encode("utf-8"))
        parts.append(b"")
        parts.append(path.read_bytes())

    parts.append(b"--" + boundary.encode() + b"--")
    parts.append(b"")

    body = crlf.join(parts)
    return body, f"multipart/form-data; boundary={boundary}"


def _send(req, timeout):
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:1200]
        sys.exit(f"ERROR API ({e.code}): {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR de red: {e.reason}")


def post_json(url, body_dict, key, timeout):
    req = urllib.request.Request(
        url,
        data=json.dumps(body_dict).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    return _send(req, timeout)


def post_multipart(url, fields, files, key, timeout):
    body, content_type = build_multipart(fields, files)
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": content_type,
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    return _send(req, timeout)


def main():
    ap = argparse.ArgumentParser(
        description="Genera fotografia de marca Movistar. Con --ref usa Gold Standards "
                    "como referencia visual (endpoint /images/edits)."
    )
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("-p", "--prompt")
    g.add_argument("--prompt-file")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--aspect", default="1:1",
                    choices=list(ASPECT_TO_SIZE.keys()),
                    help="Aspect ratio preconfigurado (ignorado si se pasa --size)")
    ap.add_argument("--size",
                    help="Tamano custom WxH. Ej: 2048x1536. Ignora --aspect")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    choices=["gpt-image-2", "gpt-image-1.5", "gpt-image-1", "gpt-image-1-mini"])
    ap.add_argument("--quality", default=DEFAULT_QUALITY,
                    choices=["low", "medium", "high", "auto"])
    ap.add_argument("--ref", action="append", default=[], metavar="RUTA",
                    help="Imagen de referencia (Gold Standard). Repetible. "
                         "Recomendado 2-3, maximo 16. Activa el endpoint /images/edits. "
                         "EL ORDEN IMPORTA: la primera conserva mas detalle y textura")
    ap.add_argument("--timeout", type=int, default=300,
                    help="Timeout en segundos (default 300)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Muestra la peticion que se enviaria y termina, sin llamar a la API "
                         "ni gastar credito")
    args = ap.parse_args()

    prompt = args.prompt or Path(args.prompt_file).read_text(encoding="utf-8").strip()
    if not prompt:
        sys.exit("ERROR: el prompt esta vacio")
    size = validate_size(args.size) if args.size else ASPECT_TO_SIZE[args.aspect]
    refs = validate_refs(args.ref) if args.ref else []
    use_edits = bool(refs)

    if args.dry_run:
        print("=== DRY RUN (no se llama a la API, no se gasta credito) ===")
        print(f"endpoint : {ENDPOINT_EDIT if use_edits else ENDPOINT_GENERATE}")
        print(f"encoding : {'multipart/form-data' if use_edits else 'application/json'}")
        print(f"model    : {args.model}")
        print(f"size     : {size}")
        print(f"quality  : {args.quality}")
        print(f"output   : {args.output}")
        print(f"refs     : {len(refs)}  (el orden importa: la 1a domina)")
        for i, r in enumerate(refs, 1):
            marca = " <- DOMINANTE" if i == 1 else ""
            print(f"   {i}. {r} ({r.stat().st_size // 1024} KB, "
                  f"{mimetypes.guess_type(r.name)[0]}){marca}")
        if use_edits:
            body, ctype = build_multipart(
                {"model": args.model, "prompt": prompt, "size": size,
                 "quality": args.quality, "n": 1},
                [("image[]", p) for p in refs],
            )
            print(f"body     : {len(body)} bytes")
            print(f"boundary : {ctype.split('boundary=')[1][:40]}...")
        print(f"prompt   : {prompt[:220]}{'...' if len(prompt) > 220 else ''}")
        print(f"OPENAI_API_KEY: {'presente' if os.environ.get('OPENAI_API_KEY') else 'AUSENTE -- la llamada real fallaria'}")
        print("=== fin dry run ===")
        return

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("ERROR: falta OPENAI_API_KEY en el entorno. "
                 "En Windows configuralo como variable de usuario y reinicia Claude. "
                 "Para probar en shell: export OPENAI_API_KEY=sk-...")

    if use_edits:
        fields = {
            "model": args.model,
            "prompt": prompt,
            "size": size,
            "quality": args.quality,
            "n": 1,
        }
        files = [("image[]", p) for p in refs]
        data = post_multipart(ENDPOINT_EDIT, fields, files, key, args.timeout)
    else:
        body = {
            "model": args.model,
            "prompt": prompt,
            "size": size,
            "quality": args.quality,
            "n": 1,
        }
        data = post_json(ENDPOINT_GENERATE, body, key, args.timeout)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    for item in data.get("data", []):
        b64 = item.get("b64_json")
        if b64:
            out.write_bytes(base64.b64decode(b64))
            mode = f"refs={len(refs)}" if use_edits else "sin refs"
            print(f"OK: {out} ({out.stat().st_size // 1024} KB, {size}, {args.model}, "
                  f"quality={args.quality}, {mode})")
            for i, r in enumerate(refs, 1):
                print(f"    ref {i}{' (dominante)' if i == 1 else ''}: {r}")
            return

    sys.exit(f"ERROR: la respuesta no contiene imagen. Respuesta: {json.dumps(data)[:500]}")


if __name__ == "__main__":
    main()
