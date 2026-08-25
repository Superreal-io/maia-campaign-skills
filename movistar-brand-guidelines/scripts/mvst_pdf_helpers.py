"""
mvst_pdf_helpers.py — helpers reutilizables para generar un PDF de marca Movistar con la skill
prebuilt `pdf` (reportlab).

Por qué existe: mismo principio que `alh_pdf_helpers.py`/`sm_pdf_helpers.py`/`mahou_pdf_helpers.py`
(Alhambra/San Miguel/Mahou) y que `assets/html/patterns.html` para artifacts HTML/React: dar el
boilerplate ya resuelto (registro de fuente, tracking aislado, ajuste de línea seguro, logo) en vez
de dejar que cada generación lo redescubra.

**Verificado, no asumido**: los `.ttf` de `assets/fonts/ttf/` (Movistar Sans Light/Regular/Medium/
Bold/Extrabold + itálicas) son `glyf` (TrueType) reales — NO el bug CFF de Alhambra
(`Gotham-Book.ttf` rechazado por reportlab). Por eso este helper no tiene equivalente a `ttf-pdf/`
ni conversión de fuente — solo registro directo.

**Movistar es COLOR PLANO** (a diferencia de Mahou, que sí tiene degradados de marca): este helper
NO expone `draw_brand_gradient()` — usa fondos de color sólido de la paleta.

Uso típico:

    import sys
    sys.path.insert(0, "<ruta a movistar-brand-guidelines-v1>/scripts")
    from mvst_pdf_helpers import get_palette, register_movistar_sans, tracked_text, wrapped, draw_logo
    from reportlab.pdfgen import canvas

    register_movistar_sans(("Regular", "Bold"))
    pal = get_palette()
    c = canvas.Canvas("salida.pdf", pagesize=(792, 445.5))
    c.setFillColor(pal["azul"]); c.rect(0, 0, 792, 445.5, fill=1, stroke=0)
    draw_logo(c, "blanco", 40, 350, 48)
    tracked_text(c, 40, 110, "Conectamos por ti", "MovistarSans-Bold", 34, pal["blanco"])
    c.save()

No importa `reportlab`/`PIL` a nivel de módulo (solo dentro de las funciones) para que este fichero
se pueda inspeccionar/testear sin esas dependencias instaladas.
"""
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.dirname(_HERE)

FONTS_DIR = os.path.join(_SKILL_ROOT, "assets", "fonts", "ttf")
LOGO_DIR = os.path.join(_SKILL_ROOT, "assets", "logo", "png")
_PALETTE_JSON = os.path.join(_SKILL_ROOT, "assets", "colors", "palette.generated.json")

_STYLES = ["Light", "Regular", "Medium", "Bold", "Extrabold",
           "Light-Italic", "Italic", "Medium-Italic", "Bold-Italic", "Extrabold-Italic"]

# hex (mayúsculas) -> clave corta y estable, para no hardcodear HEX en los scripts de generación.
_PALETTE_KEY_BY_HEX = {
    "#0066FF": "azul", "#FFFAF5": "blanco", "#262423": "negro",
    "#D3EEFF": "azul_claro", "#CEF7BF": "verde_claro", "#FFE99C": "amarillo_claro", "#FFC5A8": "coral_claro",
    "#022D67": "azul_oscuro", "#36552B": "verde_oscuro", "#5E4A09": "amarillo_oscuro", "#62301A": "coral_oscuro",
}

_palette_cache = None


def get_palette():
    """Devuelve un dict {clave: reportlab.lib.colors.HexColor} leído de
    assets/colors/palette.generated.json (fuente única de verdad) — no hardcodees los HEX en tu
    script, léelos de aquí. Claves principales: 'azul' (#0066FF), 'blanco' (#FFFAF5, NO blanco puro),
    'negro' (#262423, NO negro puro); secundarios claros 'azul_claro'/'verde_claro'/'amarillo_claro'/
    'coral_claro'; secundarios oscuros 'azul_oscuro'/'verde_oscuro'/'amarillo_oscuro'/'coral_oscuro'.
    Movistar es color plano: para "fondos ricos" usa color sólido + fotografía de marca, nunca
    degradados."""
    global _palette_cache
    if _palette_cache is None:
        from reportlab.lib.colors import HexColor
        data = json.load(open(_PALETTE_JSON, encoding="utf-8"))
        _palette_cache = {}
        for arr in ("palette", "secondary_dark"):
            for entry in data.get(arr, []) or []:
                hexv = (entry.get("hex") or "").upper()
                key = _PALETTE_KEY_BY_HEX.get(hexv)
                if key and hexv:
                    _palette_cache[key] = HexColor(hexv)
    return _palette_cache


def register_movistar_sans(styles=("Regular", "Bold")):
    """Registra los pesos de Movistar Sans indicados desde `assets/fonts/ttf/`. Pesos válidos:
    Light, Regular, Medium, Bold, Extrabold (+ itálicas: Light-Italic, Italic, Medium-Italic,
    Bold-Italic, Extrabold-Italic). Nombre de fuente resultante: `'MovistarSans-<Peso>'` (p.ej.
    `'MovistarSans-Bold'`; la cursiva Regular es `'MovistarSans-Italic'`)."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    for style in styles:
        if style not in _STYLES:
            raise ValueError(f"Peso de Movistar Sans desconocido: {style!r}. Válidos: {_STYLES}")
        pdfmetrics.registerFont(
            TTFont(f"MovistarSans-{style}", os.path.join(FONTS_DIR, f"MovistarSans-{style}.ttf"))
        )


def tracked_text(c, x, y, text, font, size, color, tracking_em=0.0, align="left"):
    """Dibuja una línea de texto con tracking (letter-spacing) real vía `setCharSpace()`. Movistar
    Sans no exige un tracking de marca específico — por defecto 0.0. `align`: 'left' (por defecto),
    'center' o 'right'."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    if align == "left":
        origin_x = x
    elif align == "center":
        origin_x = x - stringWidth(text, font, size) / 2 - (len(text) - 1) * size * tracking_em / 2
    elif align == "right":
        origin_x = x - stringWidth(text, font, size) - (len(text) - 1) * size * tracking_em
    else:
        raise ValueError("align debe ser 'left', 'center' o 'right'")
    # El `Tc` (char space) que emite setCharSpace vive en el content stream y, tras ET, PERSISTE en
    # el estado gráfico del PDF (spec PDF §9.3.1): sin aislarlo, el tracking de este titular se
    # filtra a los drawString de cuerpo siguientes (bug real de esta familia de skills: cuerpo
    # desbordado sin lanzar error). q/Q (saveState/restoreState) lo contienen.
    c.saveState()
    t = c.beginText(origin_x, y)
    t.setFont(font, size)
    t.setFillColor(color)
    t.setCharSpace(size * tracking_em)
    t.textLine(text)
    c.drawText(t)
    c.restoreState()


def wrapped(c, x, y, text, font, size, color, max_width, leading_mult=1.35, safety_margin=0.92):
    """Reflow palabra a palabra para un párrafo de cuerpo — alternativa ligera a Platypus cuando
    compones la página directamente con `Canvas` de bajo nivel. `safety_margin=0.92` por defecto:
    margen de seguridad frente a que `pdfmetrics.stringWidth()` infravalore el ancho real
    renderizado de ciertos caracteres. Devuelve la coordenada `y` final, para encadenar el siguiente
    bloque debajo."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    safe_width = max_width * safety_margin
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if stringWidth(trial, font, size) <= safe_width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    c.setFillColor(color)
    c.setFont(font, size)
    for i, line in enumerate(lines):
        c.drawString(x, y - i * size * leading_mult, line)
    return y - len(lines) * size * leading_mult


_LOGO_FILES = {
    "azul": "movistar-m-blue.png",     # la M en Azul Movistar — sobre fondo claro/Blanco Movistar
    "blanco": "movistar-m-white.png",  # la M en blanco — sobre Azul Movistar / Negro / foto azulada
    "mono": "movistar-m-mono.png",     # monocromo/neutro — casos especiales
}


def logo_path(version="azul"):
    """Ruta al PNG de la "M". `version`: 'azul' (por defecto — sobre fondos claros/Blanco Movistar),
    'blanco' (sobre Azul Movistar / Negro / foto azulada legible), 'mono' (neutro). La M va SIEMPRE
    en Azul Movistar salvo sobre fondo azul/oscuro (ver `assets/logo/README.md`). reportlab no
    soporta SVG — usa siempre el PNG pre-rasterizado; NUNCA rasterices el SVG con PyMuPDF/`fitz`
    (bug real `fill-rule:evenodd`, ver playbook §6) — hazlo con un motor de navegador real."""
    if version not in _LOGO_FILES:
        raise ValueError(f"Versión de logo no válida: {version!r}. Válidas: {sorted(_LOGO_FILES)}")
    return os.path.join(LOGO_DIR, _LOGO_FILES[version])


def draw_logo(c, version, x, y, h):
    """Dibuja la "M" a una altura `h` (pt) manteniendo el aspect ratio real del PNG. Sobre Azul
    Movistar/Negro/foto azulada usa `version='blanco'`; sobre fondo claro/Blanco Movistar,
    `version='azul'` (ver `assets/logo/README.md`). Devuelve el ancho dibujado."""
    from PIL import Image as PILImage
    path = logo_path(version)
    im = PILImage.open(path)
    w = h * (im.width / im.height)
    c.drawImage(path, x, y, width=w, height=h, mask="auto")
    return w
