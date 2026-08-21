#!/usr/bin/env python3
"""
generate_image.py: genera fotografia de marca con OpenAI (gpt-image-2 por defecto).

Lee la API key de la variable de entorno OPENAI_API_KEY.
Nunca pongas la clave en claro en config, prompts ni codigo.

El prompt debe venir YA escrito en estilo Magic Prompt (ver guidelines/magic-prompt.md):
4-5 frases cinematograficas en ingles, realismo editorial Movistar. Este script no
reescribe el prompt, solo lo envia.

Uso:
  python3 scripts/generate_image.py -p "A warm morning kitchen scene..." -o out/hero.png
  python3 scripts/generate_image.py --prompt-file prompt.txt -o out/hero.png --aspect 2:3
  python3 scripts/generate_image.py -p "..." -o out/hero.png --size 2048x1152
  python3 scripts/generate_image.py -p "..." -o out/hero.png --quality high

Aspect ratios preconfigurados (todos multiplos de 16, respetan ratio max 3:1):
  1:1  -> 1024x1024
  2:3  -> 1024x1536      (MUPI, valla vertical, story)
  3:2  -> 1536x1024      (email hero, banner horizontal)
  3:4  -> 1152x1536      (portrait 3:4)
  4:3  -> 1536x1152      (landscape 4:3)
  9:16 -> 1152x2048      (story vertical 2K)
  16:9 -> 2048x1152      (landscape 2K)
  4K-portrait  -> 2160x3840
  4K-landscape -> 3840x2160

Puedes forzar cualquier tamano con --size WxH (ambos multiplos de 16, max 3840px por lado,
total entre 655.360 y 8.294.400 pixeles, ratio max 3:1).

Modelos disponibles (via --model o env OPENAI_IMAGE_MODEL):
  gpt-image-2 (por defecto, state-of-the-art)
  gpt-image-1.5
  gpt-image-1
  gpt-image-1-mini

Calidad (via --quality o env OPENAI_IMAGE_QUALITY):
  low | medium | high | auto (por defecto)

Sin dependencias externas: usa urllib de la libreria estandar.
"""
import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

DEFAULT_MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-2")
DEFAULT_QUALITY = os.environ.get("OPENAI_IMAGE_QUALITY", "auto")
ENDPOINT = "https://api.openai.com/v1/images/generations"

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


def main():
    ap = argparse.ArgumentParser()
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
    args = ap.parse_args()

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("ERROR: falta OPENAI_API_KEY en el entorno. "
                 "En Windows configuralo como variable de usuario y reinicia Claude. "
                 "Para probar en shell: export OPENAI_API_KEY=sk-...")

    prompt = args.prompt or Path(args.prompt_file).read_text(encoding="utf-8").strip()
    size = validate_size(args.size) if args.size else ASPECT_TO_SIZE[args.aspect]

    body = {
        "model": args.model,
        "prompt": prompt,
        "size": size,
        "quality": args.quality,
        "n": 1,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:800]
        sys.exit(f"ERROR API ({e.code}): {detail}")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    for item in data.get("data", []):
        b64 = item.get("b64_json")
        if b64:
            out.write_bytes(base64.b64decode(b64))
            print(f"OK: {out} ({out.stat().st_size // 1024} KB, {size}, {args.model}, quality={args.quality})")
            return

    sys.exit(f"ERROR: la respuesta no contiene imagen. Respuesta: {json.dumps(data)[:500]}")


if __name__ == "__main__":
    main()
