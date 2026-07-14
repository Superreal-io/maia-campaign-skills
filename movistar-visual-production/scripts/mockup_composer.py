"""
mockup_composer.py: compone una pieza plana dentro de un template contextual.

Uso basico:
    python mockup_composer.py \
        --creative path/to/creative.png \
        --template ../mockup-templates/exterior/marquesina-gran-via.png \
        --corners ../mockup-templates/exterior/marquesina-gran-via.corners.json \
        --output ../out/mupi-final.png

Uso rapido (auto-detecta corners.json):
    python mockup_composer.py -c creative.png -t marquesina-gran-via.png -o out.png

Uso con esquinas ad-hoc (sin JSON):
    python mockup_composer.py -c creative.png -t template.png -o out.png \
        --tl 100 50 --tr 900 60 --br 890 700 --bl 110 690

Requisitos: pip install Pillow numpy
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageFilter
    import numpy as np
except ImportError:
    sys.stderr.write("Falta Pillow o numpy. Instala con: pip install Pillow numpy\n")
    sys.exit(1)


def find_coeffs(source_coords, target_coords):
    """Coeficientes de perspectiva para PIL.Image.transform.

    El mapa que produce va de `target_coords` a `source_coords`:
        para cada (x_out, y_out) en el canvas del template,
        devuelve (x_in, y_in) en el origen.
    Por eso llamalo con source_coords=src (rectangulo de la creativa)
    y target_coords=dst (4 esquinas destino en el template).
    """
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0] * t[0], -s[0] * t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1] * t[0], -s[1] * t[1]])
    A = np.matrix(matrix, dtype=np.float64)
    B = np.array(source_coords).reshape(8)
    res = np.dot(np.linalg.pinv(A), B)
    return np.array(res).reshape(8)


def compose(creative_path, template_path, corners, output_path, shadow_opacity=0.0):
    """Deforma la creativa a las 4 esquinas del template y las funde."""
    creative = Image.open(creative_path).convert("RGBA")
    template = Image.open(template_path).convert("RGBA")

    tw, th = template.size
    cw, ch = creative.size

    src = [(0, 0), (cw, 0), (cw, ch), (0, ch)]
    dst = [
        tuple(corners["top_left"]),
        tuple(corners["top_right"]),
        tuple(corners["bottom_right"]),
        tuple(corners["bottom_left"]),
    ]

    coeffs = find_coeffs(src, dst)

    warped = creative.transform(
        (tw, th),
        Image.PERSPECTIVE,
        coeffs,
        Image.BICUBIC,
    )

    result = template.copy()

    if shadow_opacity > 0:
        shadow_mask = warped.split()[-1]
        shadow_layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        shadow_layer.paste(
            (0, 0, 0, int(255 * shadow_opacity)),
            mask=shadow_mask.filter(ImageFilter.GaussianBlur(6)),
        )
        result = Image.alpha_composite(result, shadow_layer)

    result = Image.alpha_composite(result, warped)
    result.convert("RGB").save(output_path, quality=95)
    print("OK -> " + str(output_path))


def load_corners(args):
    if args.corners:
        with open(args.corners, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("corners", data), data.get("shadow_opacity", 0.0)

    if all([args.tl, args.tr, args.br, args.bl]):
        return {
            "top_left": args.tl,
            "top_right": args.tr,
            "bottom_right": args.br,
            "bottom_left": args.bl,
        }, args.shadow

    auto = Path(args.template).with_suffix(".corners.json")
    if auto.exists():
        with open(auto, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("corners", data), data.get("shadow_opacity", 0.0)

    sys.stderr.write("Faltan esquinas. Usa --corners archivo.json, o --tl --tr --br --bl.\n")
    sys.exit(2)


def main():
    p = argparse.ArgumentParser(description="Componer creativa dentro de un mockup template.")
    p.add_argument("-c", "--creative", required=True, help="PNG/JPG de la creativa plana.")
    p.add_argument("-t", "--template", required=True, help="PNG del template contextual.")
    p.add_argument("-o", "--output", required=True, help="Ruta de salida.")
    p.add_argument("--corners", help="JSON con las 4 esquinas del hueco.")
    p.add_argument("--tl", nargs=2, type=int, metavar=("X", "Y"), help="Top-left corner.")
    p.add_argument("--tr", nargs=2, type=int, metavar=("X", "Y"), help="Top-right corner.")
    p.add_argument("--br", nargs=2, type=int, metavar=("X", "Y"), help="Bottom-right corner.")
    p.add_argument("--bl", nargs=2, type=int, metavar=("X", "Y"), help="Bottom-left corner.")
    p.add_argument("--shadow", type=float, default=0.0, help="Opacidad de sombra 0-1 (default 0).")
    args = p.parse_args()

    corners, shadow_opacity = load_corners(args)
    compose(args.creative, args.template, corners, args.output, shadow_opacity or args.shadow)


if __name__ == "__main__":
    main()
