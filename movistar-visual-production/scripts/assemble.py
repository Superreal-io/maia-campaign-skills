#!/usr/bin/env python3
"""
assemble.py: ensambla piezas HTML/SVG de Movistar rellenando slots con assets reales.

El modelo NUNCA escribe base64. Escribe HTML/SVG con slots y este script los rellena
programaticamente desde brand/. Asi la fuente y los logos llegan siempre intactos.

Slots soportados (en cualquier archivo de texto, HTML o SVG):

  {{FONT_FACE}}          Bloque @font-face completo con las fuentes en base64 (5 pesos + italicas)
  {{FONT_FACE_MIN}}      Solo Regular(400), Bold(700) y Extrabold(800), para piezas ligeras
  {{TOKENS_CSS}}         Variables CSS de marca (colors + spacing + typography)
  {{LOGO_MARK}}          Data URI del icono M (azul, para fondo claro)
  {{LOGO_MARK_INVERSE}}  Data URI del icono M (blanco, para fondo oscuro/azul)
  {{LOGO_MARK_DARK}}     Data URI del icono M (negro Movistar)
  {{LOGO_LOCKUP}}        Data URI del lockup horizontal (fondo claro)
  {{LOGO_LOCKUP_INVERSE}} Data URI del lockup horizontal (fondo oscuro)
  {{LOGO_WORDMARK}}      Data URI del wordmark
  {{LOGO_WORDMARK_INVERSE}} Data URI del wordmark inverso
  {{IMG:ruta/relativa.png}} Data URI de cualquier imagen (fotos generadas, referencias)

Uso:
  python3 scripts/assemble.py -i pieza.slots.html -o pieza.html
  python3 scripts/assemble.py -i pieza.slots.html -o pieza.html --font min
  python3 scripts/assemble.py -i email.slots.html -o email.html --no-font   # emails: sin @font-face

Las rutas de {{IMG:...}} se resuelven relativas al directorio del archivo de entrada,
y si no existen ahi, relativas a la raiz del bundle.
"""
import argparse
import base64
import re
import sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent
FONTS = BUNDLE / "brand" / "fonts"
LOGOS = BUNDLE / "brand" / "logos"
TOKENS = BUNDLE / "brand" / "tokens"

WEIGHTS = [
    ("MovistarSans-Light.woff2", 300, "normal"),
    ("MovistarSans-Light-Italic.woff2", 300, "italic"),
    ("MovistarSans-Regular.woff2", 400, "normal"),
    ("MovistarSans-Italic.woff2", 400, "italic"),
    ("MovistarSans-Medium.woff2", 500, "normal"),
    ("MovistarSans-Medium-Italic.woff2", 500, "italic"),
    ("MovistarSans-Bold.woff2", 700, "normal"),
    ("MovistarSans-Bold-Italic.woff2", 700, "italic"),
    ("MovistarSans-Extrabold.woff2", 800, "normal"),
    ("MovistarSans-Extrabold-Italic.woff2", 800, "italic"),
]
WEIGHTS_MIN = [w for w in WEIGHTS if w[1] in (400, 700, 800) and w[2] == "normal"]

LOGO_SLOTS = {
    "LOGO_MARK": "mark.svg",
    "LOGO_MARK_INVERSE": "mark-inverse.svg",
    "LOGO_MARK_DARK": "mark-dark.svg",
    "LOGO_LOCKUP": "lockup-horizontal.svg",
    "LOGO_LOCKUP_INVERSE": "lockup-horizontal-inverse.svg",
    "LOGO_WORDMARK": "wordmark.svg",
    "LOGO_WORDMARK_INVERSE": "wordmark-inverse.svg",
}

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".webp": "image/webp", ".svg": "image/svg+xml", ".gif": "image/gif",
        ".avif": "image/avif"}


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def data_uri(path: Path) -> str:
    mime = MIME.get(path.suffix.lower(), "application/octet-stream")
    return f"data:{mime};base64,{b64(path)}"


def font_face_block(weights) -> str:
    blocks = []
    for fname, weight, style in weights:
        p = FONTS / fname
        if not p.exists():
            print(f"AVISO: falta la fuente {fname}, se omite", file=sys.stderr)
            continue
        blocks.append(
            "@font-face {\n"
            '  font-family: "Movistar Sans";\n'
            f"  font-style: {style};\n"
            f"  font-weight: {weight};\n"
            "  font-display: swap;\n"
            f'  src: url("data:font/woff2;base64,{b64(p)}") format("woff2");\n'
            "}"
        )
    return "\n".join(blocks)


def tokens_css() -> str:
    parts = []
    for name in ("colors.css", "spacing.css", "typography.css"):
        p = TOKENS / name
        if p.exists():
            css = p.read_text(encoding="utf-8")
            css = re.sub(r'@import[^;]+;', '', css)  # sin imports anidados
            parts.append(f"/* {name} */\n{css}")
    return "\n".join(parts)


def resolve_img(ref: str, base_dir: Path) -> Path:
    for candidate in (base_dir / ref, BUNDLE / ref):
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Imagen no encontrada: {ref} (buscado en {base_dir} y {BUNDLE})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True)
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--font", choices=["full", "min"], default="min",
                    help="full = 10 variantes, min = 400/700/800 normales (por defecto)")
    ap.add_argument("--no-font", action="store_true",
                    help="No embeber @font-face (emails). Los slots FONT_FACE quedan vacios.")
    args = ap.parse_args()

    src = Path(args.input)
    text = src.read_text(encoding="utf-8")
    missing = []

    if "{{FONT_FACE}}" in text or "{{FONT_FACE_MIN}}" in text:
        if args.no_font:
            text = text.replace("{{FONT_FACE}}", "").replace("{{FONT_FACE_MIN}}", "")
        else:
            weights = WEIGHTS if args.font == "full" else WEIGHTS_MIN
            text = text.replace("{{FONT_FACE}}", font_face_block(weights))
            text = text.replace("{{FONT_FACE_MIN}}", font_face_block(WEIGHTS_MIN))

    if "{{TOKENS_CSS}}" in text:
        text = text.replace("{{TOKENS_CSS}}", tokens_css())

    for slot, fname in LOGO_SLOTS.items():
        token = "{{" + slot + "}}"
        if token in text:
            p = LOGOS / fname
            if p.exists():
                text = text.replace(token, data_uri(p))
            else:
                missing.append(fname)

    for m in re.finditer(r"\{\{IMG:([^}]+)\}\}", text):
        ref = m.group(1).strip()
        try:
            uri = data_uri(resolve_img(ref, src.parent))
            text = text.replace(m.group(0), uri)
        except FileNotFoundError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            missing.append(ref)

    leftover = re.findall(r"\{\{[A-Z_]+(?::[^}]*)?\}\}", text)
    if leftover:
        print(f"AVISO: slots sin resolver: {sorted(set(leftover))}", file=sys.stderr)

    Path(args.output).write_text(text, encoding="utf-8")
    status = "con avisos" if (missing or leftover) else "OK"
    print(f"Ensamblado {status}: {args.output} ({Path(args.output).stat().st_size // 1024} KB)")
    if missing:
        sys.exit(2)


if __name__ == "__main__":
    main()
