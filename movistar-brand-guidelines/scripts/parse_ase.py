#!/usr/bin/env python3
"""
parse_ase.py — Movistar brand-guidelines skill

Lee el fichero `.ase` (Adobe Swatch Exchange) de la paleta Movistar y lo trata
como FUENTE DE VERDAD del color. Movistar es **color plano** (sin degradados),
así que esto genera la PALETA de swatches (name, hex, rgb), no degradados.

Uso:
    python parse_ase.py inspect [carpeta]
    python parse_ase.py generate [carpeta] [salida.json]

Por defecto carpeta = ../assets/colors (relativa a este script) y
salida = ../assets/colors/palette.generated.json
Solo librería estándar (struct).
"""
import json, os, struct, sys

# Roles de marca por hex (Brand Guardian §4). El color sale del .ase; esto solo etiqueta.
ROLES = {
    "#0066FF": {"rol": "Azul Movistar", "uso": "principal; presente en toda comunicacion"},
    "#FFFAF5": {"rol": "Blanco Movistar", "uso": "fondo claro (NO blanco puro)"},
    "#262423": {"rol": "Negro Movistar", "uso": "texto/fondo oscuro (NO negro puro)"},
    "#D3EEFF": {"rol": "Azul claro (secundario)", "uso": "acento por seccion/capitulo"},
    "#CEF7BF": {"rol": "Verde claro (secundario)", "uso": "acento por seccion/capitulo"},
    "#FFE99C": {"rol": "Amarillo claro (secundario)", "uso": "acento por seccion/capitulo"},
    "#FFC5A8": {"rol": "Coral claro (secundario)", "uso": "acento por seccion/capitulo"},
}

# --- Colores NO presentes en el .ase (solo trae 7 swatches base) --------------------------------
# Provienen de la guía de marca y del refresh nov-2025, documentados en brand/color-palette.md
# §4.1.2 (secundarios oscuros) y §4.5 (gama de grises), y brand/contrast-matrix.md (semánticos).
# Se emiten como arrays aparte para que lint_artifact.py (_load_palette_hex) reconozca como
# válidos estos colores sin tener que meterlos en el .ase (que es la fuente del color PLANO base).
SECONDARY_DARK = [
    {"hex": "#022D67", "rgb": [2, 45, 103], "rol": "Azul oscuro (secundario)"},
    {"hex": "#36552B", "rgb": [54, 85, 43], "rol": "Verde oscuro (secundario)"},
    {"hex": "#5E4A09", "rgb": [94, 74, 9], "rol": "Amarillo oscuro (secundario)"},
    {"hex": "#62301A", "rgb": [98, 48, 26], "rol": "Coral oscuro (secundario)"},
]
# Gama de 10 pasos (§4.5, refresh nov-2025). Extremos = Blanco/Negro Movistar. El paso 10
# (#000000 negro puro) se documenta "solo referencia, no usar" — se OMITE a propósito (lo marca
# check_pure_black_white como FAIL si aparece).
GRAYS = [
    {"hex": "#FFFAF5", "rgb": [255, 250, 245], "step": 1, "rol": "Blanco Movistar"},
    {"hex": "#F3EEEA", "rgb": [243, 238, 234], "step": 2},
    {"hex": "#DFDBD6", "rgb": [223, 219, 214], "step": 3},
    {"hex": "#BFBCB8", "rgb": [191, 188, 184], "step": 4},
    {"hex": "#9F9C99", "rgb": [159, 156, 153], "step": 5},
    {"hex": "#807D7B", "rgb": [128, 125, 123], "step": 6},
    {"hex": "#605E5C", "rgb": [96, 94, 92], "step": 7},
    {"hex": "#403F3D", "rgb": [64, 63, 61], "step": 8},
    {"hex": "#262423", "rgb": [38, 36, 35], "step": 9, "rol": "Negro Movistar"},
]
# Colores semánticos (brand/contrast-matrix.md): estado regular + hover.
SEMANTIC = [
    {"hex": "#0066FF", "rol": "Acento", "estado": "regular"},
    {"hex": "#005EEB", "rol": "Acento", "estado": "hover"},
    {"hex": "#048239", "rol": "Positivo", "estado": "regular"},
    {"hex": "#036D30", "rol": "Positivo", "estado": "hover"},
    {"hex": "#926C00", "rol": "Alerta", "estado": "regular"},
    {"hex": "#745600", "rol": "Alerta", "estado": "hover"},
    {"hex": "#C10000", "rol": "Negativo", "estado": "regular"},
    {"hex": "#AD0000", "rol": "Negativo", "estado": "hover"},
]


def _utf16be(buf, n):
    return buf[: n * 2].decode("utf-16-be").rstrip("\x00")


def parse_ase(path):
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:4] != b"ASEF":
        raise ValueError(f"{path}: no es ASE (falta cabecera ASEF)")
    (n_blocks,) = struct.unpack(">I", data[8:12])
    pos, out = 12, []
    for _ in range(n_blocks):
        if pos + 6 > len(data):
            break
        (btype,) = struct.unpack(">H", data[pos:pos + 2])
        (blen,) = struct.unpack(">I", data[pos + 2:pos + 6])
        body = data[pos + 6:pos + 6 + blen]
        pos += 6 + blen
        if btype != 0x0001:
            continue
        (nlen,) = struct.unpack(">H", body[0:2])
        name = _utf16be(body[2:], nlen)
        off = 2 + nlen * 2
        model = body[off:off + 4].decode("ascii").strip()
        off += 4
        if model == "RGB":
            r, g, b = struct.unpack(">fff", body[off:off + 12])
            rgb = (round(r * 255), round(g * 255), round(b * 255))
        elif model == "CMYK":
            c, m, y, k = struct.unpack(">ffff", body[off:off + 16])
            rgb = (round(255 * (1 - c) * (1 - k)), round(255 * (1 - m) * (1 - k)), round(255 * (1 - y) * (1 - k)))
        elif model == "Gray":
            (gr,) = struct.unpack(">f", body[off:off + 4]); v = round(gr * 255); rgb = (v, v, v)
        else:
            rgb = None
        hexv = ("#%02X%02X%02X" % rgb) if rgb else None
        out.append({"name": name, "model": model, "hex": hexv, "rgb": list(rgb) if rgb else None})
    return out


def _default_folder():
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "colors"))


def _find_ase(folder):
    for fn in os.listdir(folder):
        if fn.lower().endswith(".ase"):
            return os.path.join(folder, fn)
    return None


def generate(folder, out_path):
    ase = _find_ase(folder)
    swatches = parse_ase(ase)
    palette = []
    for s in swatches:
        role = ROLES.get((s["hex"] or "").upper(), {})
        palette.append({**s, **role})
    res = {
        "brand": "movistar",
        "source": os.path.basename(ase) + " (Adobe .ase = fuente de verdad del color base)",
        "note": ("Generado por scripts/parse_ase.py. No editar a mano; re-generar. `palette` sale "
                 "del .ase (7 swatches base: 3 principales + 4 secundarios claros). "
                 "`secondary_dark`/`grays`/`semantic` NO están en el .ase — son colores derivados de "
                 "brand/color-palette.md §4.1.2/§4.5 y brand/contrast-matrix.md (refresh nov-2025), "
                 "definidos en las constantes de parse_ase.py. Movistar es COLOR PLANO: sin degradados."),
        "color_model": "flat",
        "palette": palette,
        "secondary_dark": SECONDARY_DARK,
        "grays": GRAYS,
        "semantic": SEMANTIC,
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=2)
    return res


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "generate"
    folder = argv[2] if len(argv) > 2 else _default_folder()
    if cmd == "inspect":
        for s in parse_ase(_find_ase(folder)):
            print(f"  {s['name']!r:14} {s['model']:5} {s['hex']}  rgb={s['rgb']}")
    elif cmd == "generate":
        out = argv[3] if len(argv) > 3 else os.path.join(folder, "palette.generated.json")
        res = generate(folder, out)
        print(f"Escrito: {out}  ({len(res['palette'])} swatches)")
    else:
        print(__doc__); return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
