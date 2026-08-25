#!/usr/bin/env python3
"""lint_artifact.py — gate determinista de QA para Artifacts HTML/React de Movistar.

Mismo principio que `lint_artifact.py` de las 4 marcas del rediseño (alhambra/san-miguel/
solan-de-cabras/mahou): convierte el QA de artifacts web de "el modelo relee su propio código con
cuidado" (subjetivo, varía entre modelos) a un análisis MECÁNICO del HTML/CSS final. Python puro, sin
dependencias, sin red ni navegador — corre en el sandbox `code_execution` de producción.

No renderiza nada — es análisis ESTÁTICO del texto HTML/CSS: parsea la estructura, resuelve estilos
con heurísticas razonables (no es un motor CSS completo) y aplica un catálogo de reglas de marca +
composición propias de Movistar. Ante ambigüedad, DEGRADA A WARN o SKIP (nunca un FAIL falso).

El bloque MOTOR COMPARTIDO v2 (resolución de CSS/variables/`<link>`/contraste WCAG + degradados) es
idéntico byte a byte en las brand-guidelines de esta convención (alhambra/san-miguel/solan-de-cabras/
mahou/movistar). Mahou es la implementación CANÓNICA de ese motor. Los checks de abajo son PROPIOS de
Movistar.

⚠️ **Movistar es distinta de las otras marcas en un punto CRÍTICO: la FUENTE.** Movistar es la ÚNICA
marca cuya tipografía la inyecta el runtime de `artifact-flow` en los artifacts web
(`injectBrandFont`/`MOVISTAR_FONT_FACE`, gated a `brand.startsWith("movistar")`). Por eso su check de
fuente está INVERTIDO respecto a las demás: en vez de EXIGIR un `@font-face` base64 inline
(`check_fontface_inlined` en las otras 4), Movistar lo PROHÍBE (`check_fontface_not_pasted`) — teclear
el base64 cuesta ~15s y arriesga cortar el stream (docs/FONT-RUNTIME-INJECTION-PROPOSAL.md) — y en su
lugar exige declarar `font-family:'Movistar Sans'` (`check_font_family`). NO revertir esto a la
conducta de las otras marcas: rompería todos los artifacts correctos de la única marca en producción.
Movistar además es COLOR PLANO (cualquier degradado = FAIL), prohíbe el em-dash "—" y el blanco/negro
puros, y SÍ permite exclamaciones (con signos RAE de apertura+cierre). Ningún check se copió sin adaptar.

Uso:
    python3 lint_artifact.py archivo.html          # CLI: imprime hallazgos, exit code 1 si hay FAIL
    from lint_artifact import lint                    # librería: lint(html_text) -> list[Finding]

Severidades:
- FAIL: corrige y vuelve a lintar antes de entregar el artifact — no es opcional.
- WARN: revísalo y, si decides que está bien así, dilo explícitamente en la tabla de
  auto-verificación de `brand/artifact-qa.md` — no bloquea, pero no lo ignores en silencio.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent
_PALETTE_PATH = _SKILL_DIR / "assets" / "colors" / "palette.generated.json"

# -- Datos de marca (fuente de verdad: brand/color-palette.md + palette.generated.json) -----------
# Movistar es COLOR PLANO (sin degradados). Paleta = 3 principales + 4 secundarios claros + 4
# secundarios oscuros + gama de 8 grises del refresh nov-2025 (§4.5) + 8 semánticos (regular+hover,
# brand/contrast-matrix.md). Fallback si palette.generated.json no está disponible.
_FALLBACK_PALETTE_HEX = {
    "#0066ff", "#fffaf5", "#262423",                                     # principales
    "#d3eeff", "#cef7bf", "#ffe99c", "#ffc5a8",                          # secundarios claros
    "#022d67", "#36552b", "#5e4a09", "#62301a",                          # secundarios oscuros
    "#f3eeea", "#dfdbd6", "#bfbcb8", "#9f9c99", "#807d7b", "#605e5c", "#403f3d",  # grises §4.5
    "#005eeb", "#048239", "#036d30", "#926c00", "#745600", "#c10000", "#ad0000",  # semánticos
}

# Combinaciones "Prohibido" (brand/contrast-matrix.md): un color CLARO (Blanco Movistar + los 4
# secundarios claros) como texto/grafismo sobre un fondo CLARO = ilegible. Sin "#".
_LIGHT_HEXES = {"fffaf5", "d3eeff", "cef7bf", "ffe99c", "ffc5a8"}


def _load_palette_hex() -> set[str]:
    """Paleta plana de Movistar. Une `palette[]` (principales + secundarios claros) + los arrays
    ampliados del refresh nov-2025 (`secondary_dark[]`, `grays[]`, `semantic[]`) para que ninguno de
    esos colores legítimos dispare `check_out_of_palette`. Entradas con `hex: null` se ignoran."""
    try:
        data = json.loads(_PALETTE_PATH.read_text(encoding="utf-8"))
        hexes: set[str] = set()
        for key in ("palette", "secondary_dark", "grays", "semantic"):
            for c in data.get(key, []) or []:
                h = c.get("hex")
                if h:
                    hexes.add(h.lower())
        return hexes or set(_FALLBACK_PALETTE_HEX)
    except Exception:
        return set(_FALLBACK_PALETTE_HEX)


@dataclass
class Finding:
    rule: str
    severity: str  # "FAIL" | "WARN"
    detail: str
    snippet: str = ""

    def to_dict(self) -> dict:
        return {"rule": self.rule, "severity": self.severity, "detail": self.detail, "snippet": self.snippet}


# -- Parsing ligero de HTML a árbol con padres (genérico, sin cambios respecto a San Miguel) -------
@dataclass
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    parent: "Node | None" = None
    children: list = field(default_factory=list)
    text: str = ""  # texto propio (no de hijos), para checks de contenido visible

    @property
    def classes(self) -> list[str]:
        return (self.attrs.get("class") or "").split()

    @property
    def inline_style(self) -> dict[str, str]:
        return _parse_style_attr(self.attrs.get("style", ""))

    def ancestors(self):
        node = self.parent
        while node is not None:
            yield node
            node = node.parent

    def iter_all(self):
        yield self
        for c in self.children:
            yield from c.iter_all()


def _parse_style_attr(style: str) -> dict[str, str]:
    out = {}
    for decl in style.split(";"):
        if ":" not in decl:
            continue
        prop, _, val = decl.partition(":")
        out[prop.strip().lower()] = val.strip().lower()
    return out


_VOID_TAGS = {"br", "img", "input", "hr", "meta", "link", "area", "base", "col", "embed", "source", "track", "wbr"}
_SKIP_TEXT_TAGS = {"script", "style"}


class _TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node(tag="#root")
        self._stack = [self.root]
        self._skip_text_depth = 0

    def handle_starttag(self, tag, attrs):
        node = Node(tag=tag.lower(), attrs=dict(attrs), parent=self._stack[-1])
        self._stack[-1].children.append(node)
        if tag.lower() not in _VOID_TAGS:
            self._stack.append(node)
        if tag.lower() in _SKIP_TEXT_TAGS:
            self._skip_text_depth += 1

    def handle_startendtag(self, tag, attrs):
        node = Node(tag=tag.lower(), attrs=dict(attrs), parent=self._stack[-1])
        self._stack[-1].children.append(node)

    def handle_endtag(self, tag):
        if tag.lower() in _SKIP_TEXT_TAGS and self._skip_text_depth > 0:
            self._skip_text_depth -= 1
        if len(self._stack) > 1 and self._stack[-1].tag == tag.lower():
            self._stack.pop()
        elif len(self._stack) > 1:
            for i in range(len(self._stack) - 1, 0, -1):
                if self._stack[i].tag == tag.lower():
                    del self._stack[i:]
                    break

    def handle_data(self, data):
        if self._skip_text_depth == 0 and data.strip():
            self._stack[-1].text += data


def parse_html(html_text: str) -> Node:
    builder = _TreeBuilder()
    builder.feed(html_text)
    return builder.root


# ─────────────────────────────────────────────────────────────────────────────────────────────
# ── MOTOR COMPARTIDO v2 — sincronizado a mano entre las 4 brand-guidelines. Si tocas algo aquí,
#    replícalo en las otras 3 y corre scripts/qa/run_lint_fixtures.py.
# ─────────────────────────────────────────────────────────────────────────────────────────────
# Todo lo que va desde este marcador hasta "FIN MOTOR COMPARTIDO" es IDÉNTICO byte a byte en
# alhambra/san-miguel/solan-de-cabras/mahou: es el motor de resolución de CSS + contraste WCAG que
# las cuatro comparten. Los checks POR-MARCA (paleta, copy, tipografía, degradados propios) viven
# DESPUÉS del marcador de fin y NO forman parte del motor. `Node`, `parse_html`, `Finding` y
# `_parse_style_attr` se definen ANTES del motor (también idénticos, pero cada fichero los declara
# por su cuenta para poder correr suelto).
_ENGINE_VERSION = "2"

# -- Extracción de reglas CSS de los <style> + custom properties de :root ------------------------
_CSS_RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
_ROOT_BLOCK_RE = re.compile(r":root\s*\{([^{}]*)\}", re.S)
_VAR_DECL_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;]+);?")
_VAR_REF_RE = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)")
_CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)


def _strip_css_comments(css: str) -> str:
    """Quita comentarios `/* ... */` antes de parsear selectores. `_CSS_RULE_RE` captura el
    SELECTOR como "todo lo que no sea `{`/`}`", así que un comentario de documentación justo antes
    de una regla (el estilo real de `brand-tokens.css`, casi cada clase lleva su nota encima) se
    cuela dentro del selector de la regla SIGUIENTE, dejándolo con espacios/saltos que
    `_selector_matches` rechaza siempre — la regla nunca aplica y el color/contraste no se calcula.
    Sustituye por un espacio (no cadena vacía) para no pegar tokens a ambos lados del comentario."""
    return _CSS_COMMENT_RE.sub(" ", css)


def _extract_css_variables(html_text: str) -> dict[str, str]:
    """Custom properties declaradas en `:root { --nombre: valor; }`. Necesario aparte de
    `_extract_css_rules`: `_selector_matches` excluye cualquier selector con `:` (para no confundir
    pseudo-clases), así que `:root` nunca se captura como regla normal. Sin esto, la paleta de marca
    declarada como `var(--*)` sería invisible para los checks de color/contraste/degradado."""
    variables: dict[str, str] = {}
    for block_m in _ROOT_BLOCK_RE.finditer(html_text):
        for decl_m in _VAR_DECL_RE.finditer(block_m.group(1)):
            variables[decl_m.group(1)] = decl_m.group(2).strip()
    return variables


def _resolve_var_value(value: str, variables: dict[str, str]) -> str:
    """Sustituye TODAS las ocurrencias de `var(--nombre[, fallback])` por su valor de `:root` (una
    pasada global — la paleta de marca no anida `var()` dentro de `var()`). Funciona igual si el
    valor es un único `var(...)` o si contiene varios dentro de una función más larga (p.ej.
    `linear-gradient(var(--a), var(--b))`) — imprescindible para validar degradados por variable."""
    def _sub(m: "re.Match") -> str:
        name, fallback = m.group(1), m.group(2)
        return variables.get(name, fallback if fallback is not None else m.group(0))
    return _VAR_REF_RE.sub(_sub, value)


def _extract_css_rules(html_text: str) -> list[tuple[str, dict[str, str]]]:
    """Devuelve [(selector, {prop: val})] para reglas de los `<style>`. No es un motor CSS —
    selectores compuestos (descendientes, pseudo-clases) se guardan tal cual y se ignoran en la
    resolución por elemento (`_selector_matches`), evitando falsos positivos."""
    rules = []
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", html_text, re.S | re.I):
        css = _strip_css_comments(m.group(1))
        for sel_block in _CSS_RULE_RE.finditer(css):
            selectors = sel_block.group(1).strip()
            body = sel_block.group(2)
            decls = _parse_style_attr(body.replace("\n", ";"))
            for sel in selectors.split(","):
                rules.append((sel.strip(), decls))
    return rules


# -- Hojas de estilo enlazadas (<link rel="stylesheet">) -----------------------------------------
_LINK_TAG_RE = re.compile(r"<link\b[^>]*>", re.I)
_HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.I)
_REL_STYLESHEET_RE = re.compile(r'rel=["\']stylesheet["\']', re.I)


def _inline_linked_stylesheets(html_text: str, base_dir: "Path | None") -> str:
    """Resuelve `<link rel="stylesheet" href="...">` locales, devolviendo `html_text` + el CSS
    enlazado envuelto en un `<style>` extra al final — SOLO para uso de `_extract_css_rules`/
    `_extract_css_variables`, nunca para `parse_html`. `patterns.html` enlaza `brand-tokens.css`
    externamente a propósito (auto-testable con un navegador real) — sin esto, este linter (análisis
    de texto puro) vería 0 variables y quedaría ciego a la paleta real. Sin `base_dir` o con href
    remoto (`http(s)://`, `//`), el `<link>` se ignora en silencio — degrada sin romper."""
    if base_dir is None:
        return html_text
    extra_css = []
    for tag_m in _LINK_TAG_RE.finditer(html_text):
        tag = tag_m.group(0)
        if not _REL_STYLESHEET_RE.search(tag):
            continue
        href_m = _HREF_RE.search(tag)
        if not href_m:
            continue
        href = href_m.group(1)
        if href.startswith(("http://", "https://", "//")):
            continue
        css_path = (base_dir / href).resolve()
        try:
            extra_css.append(css_path.read_text(encoding="utf-8"))
        except OSError:
            continue
    if not extra_css:
        return html_text
    return html_text + "\n<style>\n" + "\n".join(extra_css) + "\n</style>\n"


def _selector_matches(sel: str, node: "Node") -> bool:
    sel = sel.strip()
    if not sel or any(ch in sel for ch in " >+~:["):
        return False
    if sel.startswith("."):
        return sel[1:] in node.classes
    if sel.startswith("#"):
        return node.attrs.get("id") == sel[1:]
    return sel.lower() == node.tag


def _resolve_prop(node: "Node", rules: list[tuple[str, dict]], prop: str,
                   variables: "dict[str, str] | None" = None) -> "str | None":
    """Última regla que matchea gana (aprox. de cascada CSS) + estilo inline (máxima prioridad).
    Si el valor final contiene `var(--nombre)`, lo resuelve contra `:root`. NO resuelve herencia
    entre nodos (un `<p>` sin `color` propio no hereda aquí el de su padre) — para eso están
    `_resolve_fg_bg` (color/fondo) y, si la marca lo necesita, un resolver de herencia propio."""
    value = None
    for sel, decls in rules:
        if prop in decls and _selector_matches(sel, node):
            value = decls[prop]
    inline = node.inline_style
    if prop in inline:
        value = inline[prop]
    if value and variables and "var(" in value:
        value = _resolve_var_value(value, variables)
    return value


# -- Color / contraste WCAG ----------------------------------------------------------------------
_HEX_RE = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
_RGB_RE = re.compile(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)")


def _parse_color(value: str) -> "tuple[int, int, int] | None":
    if not value:
        return None
    m = _HEX_RE.search(value)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = _RGB_RE.search(value)
    if m:
        return tuple(int(g) for g in m.groups())
    return None


def _hex_of(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def _relative_luminance(rgb: tuple[int, int, int]) -> float:
    def chan(c: int) -> float:
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def _contrast_ratio(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    l1, l2 = _relative_luminance(fg), _relative_luminance(bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# -- Degradados (detección + extracción de stops) ------------------------------------------------
_GRADIENT_START_RE = re.compile(r"(linear|radial|conic)-gradient\s*\(", re.I)
_COLOR_TOKEN_RE = re.compile(r"#[0-9a-fA-F]{3,6}\b|rgba?\([^)]*\)")


def _is_gradient_value(value: "str | None") -> bool:
    return bool(value and _GRADIENT_START_RE.search(value))


def _extract_balanced(text: str, open_paren_idx: int) -> str:
    """Contenido entre paréntesis balanceados empezando en `open_paren_idx` (debe apuntar a un
    '('). Un regex naive `\\(([^)]*)\\)` corta en el primer ')' interior — y un degradado real
    anida paréntesis (`rgb(...)`, `var(...)`). Degrada devolviendo cadena vacía / el resto del
    texto si el índice no es válido o no hay cierre — el linter nunca revienta por CSS mal formado,
    solo da un hallazgo de menos."""
    if open_paren_idx < 0 or open_paren_idx >= len(text) or text[open_paren_idx] != "(":
        return ""
    depth = 0
    for i in range(open_paren_idx, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return text[open_paren_idx + 1:i]
    return text[open_paren_idx + 1:]


def _gradient_body(value: str) -> str:
    m = _GRADIENT_START_RE.search(value)
    if not m:
        return ""
    return _extract_balanced(value, m.end() - 1)


def _gradient_stop_hexes(body: str, variables: "dict[str, str] | None") -> set[str]:
    """Conjunto de colores (hex normalizado, sin '#') declarados como stops dentro del cuerpo de un
    degradado. Limitación conocida y aceptada: no reconoce keywords CSS con nombre ("red", "gold") —
    solo hex/rgb()/var() ya resuelto. Un degradado escrito solo con keywords devuelve stops vacío
    (se salta, "no se puede juzgar", en vez de un falso FAIL o un falso pase)."""
    resolved = _resolve_var_value(body, variables) if variables else body
    hexes: set[str] = set()
    for tok in _COLOR_TOKEN_RE.finditer(resolved):
        rgb = _parse_color(tok.group(0))
        if rgb:
            hexes.add(_hex_of(rgb).lstrip("#"))
    return hexes


# -- Resolución de color de texto / fondo, tamaño de texto y backdrop de foto --------------------
_PX_RE = re.compile(r"([\d.]+)\s*px")


def _resolve_fg_bg(node: "Node", rules: list[tuple[str, dict]],
                    variables: "dict[str, str] | None" = None):
    """Color de texto y fondo HEREDADOS: el propio nodo o el primer ancestro que declare cada uno.
    Devuelve una TUPLA DE 3: `(fg, bg_solido_o_None, bg_degradado_crudo_o_None)`.

    ⚠️ `fg` recorre ancestros igual que `bg` (no solo la regla del propio nodo). El patrón real y
    más común de todas estas marcas es `<div class="bg-oscuro"><p>texto</p></div>`, donde el color
    lo trae el contenedor y el `<p>` no repite `color`: si `fg` solo mirara el nodo, quedaría en
    `None` y todo check de contraste/color se saltaría en silencio ese nodo (falso negativo real).

    Si el primer fondo resoluble en la cadena de ancestros es un degradado, `bg` queda en `None`
    (nunca se hace `_parse_color` sobre el string del degradado — capturaría solo el PRIMER stop
    como si fuera fondo sólido, un bug silencioso) y se devuelve crudo en la 3ª posición para que
    el check de contraste de cada marca decida qué hacer (en marcas de color plano, la mera
    presencia del degradado ya la condena su propio check_gradients, así que el contraste hace
    SKIP)."""
    fg: "tuple[int, int, int] | None" = None
    for n in [node, *node.ancestors()]:
        fg_val = _resolve_prop(n, rules, "color", variables)
        if fg_val:
            fg = _parse_color(fg_val)
            break
    bg: "tuple[int, int, int] | None" = None
    bg_gradient_raw: "str | None" = None
    for n in [node, *node.ancestors()]:
        raw = (_resolve_prop(n, rules, "background-color", variables)
               or _resolve_prop(n, rules, "background", variables))
        if not raw:
            continue
        if _is_gradient_value(raw):
            bg_gradient_raw = raw
            break
        parsed = _parse_color(raw)
        if parsed:
            bg = parsed
            break
    return fg, bg, bg_gradient_raw


def _is_large_text(node: "Node", rules: list[tuple[str, dict]],
                    variables: "dict[str, str] | None" = None) -> bool:
    """AA para 'texto grande' (umbral 3:1) es >=24px, o >=19px si además es bold — WCAG 2.1."""
    fs_val = _resolve_prop(node, rules, "font-size", variables)
    m = _PX_RE.search(fs_val or "")
    if not m:
        return False
    px = float(m.group(1))
    if px >= 24:
        return True
    weight = (_resolve_prop(node, rules, "font-weight", variables) or "").strip()
    is_bold = weight in ("bold", "bolder") or (weight.isdigit() and int(weight) >= 700)
    return px >= 19 and is_bold


def _media_backdrop_container(node: "Node", rules: list[tuple[str, dict]]) -> "Node | None":
    """Contenedor `position:relative` más cercano (entre `node` y sus ancestros) que además
    contenga un `<img>` hermano/descendiente — el patrón real de "texto sobre foto" de estas marcas
    es `<img>` + scrim + texto como HERMANOS dentro de un contenedor `position:relative` compartido,
    nunca texto como descendiente de `<img>` (imposible: elemento vacío)."""
    for ancestor in [node, *node.ancestors()]:
        if _resolve_prop(ancestor, rules, "position") == "relative":
            if any(n.tag == "img" for n in ancestor.iter_all() if n is not ancestor):
                return ancestor
    return None


def _ancestors_until(node: "Node", stop: "Node"):
    for a in node.ancestors():
        if a is stop:
            return
        yield a


# -- Selectores complejos que definen color/fondo y el motor NO resuelve (WARN agregado) ---------
_INTERACTION_PSEUDO_RE = re.compile(r"::?(hover|focus|active|selection|focus-visible|focus-within)", re.I)
_COLOR_DECL_RE = re.compile(r"\b(color|background|background-color|background-image|fill)\s*:", re.I)
_AT_BLOCK_RE = re.compile(r"@(media|keyframes|supports|font-face|page)\b", re.I)
_COMPLEX_SEL_CHARS = " >+~:["


def _remove_at_rule_blocks(css: str) -> str:
    """Elimina bloques @media/@keyframes/@supports/@font-face/@page con llaves balanceadas
    (anidamiento incluido) para que `check_unsupported_selectors` no confunda sus selectores
    internos (breakpoints, `0%`/`from`/`to`) con selectores complejos de color."""
    out = []
    i, n = 0, len(css)
    while i < n:
        m = _AT_BLOCK_RE.search(css, i)
        if not m:
            out.append(css[i:])
            break
        out.append(css[i:m.start()])
        brace = css.find("{", m.end())
        if brace == -1:
            break
        depth, j = 0, brace
        while j < n:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
        i = j
    return "".join(out)


def check_unsupported_selectors(html_text: str) -> list["Finding"]:
    """Motor: reextrae las reglas de los `<style>` SIN el filtro de `_selector_matches` y avisa
    (un único WARN agregado) de los selectores complejos (descendiente/hijo/hermano/atributo/
    pseudo-elemento) que definen color o fondo y que este linter NO resuelve — el contraste de esos
    nodos no queda cubierto por ningún otro check y hay que verificarlo a mano. Excluye los pseudos
    de interacción (`:hover`/`:focus`/`:active`/`::selection`) y los bloques `@media`/`@keyframes`/
    `@supports`/`@font-face`. Prefiere selectores de una sola clase para que el motor sí los
    evalúe."""
    complex_selectors: list[str] = []
    seen: set[str] = set()
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", html_text, re.S | re.I):
        css = _remove_at_rule_blocks(_strip_css_comments(m.group(1)))
        for sel_block in _CSS_RULE_RE.finditer(css):
            if not _COLOR_DECL_RE.search(sel_block.group(2)):
                continue
            for sel in sel_block.group(1).split(","):
                sel = sel.strip()
                if not sel or not any(ch in sel for ch in _COMPLEX_SEL_CHARS):
                    continue  # vacío o selector simple (tag/.clase/#id): el motor sí lo resuelve
                base = _INTERACTION_PSEUDO_RE.sub("", sel).strip()
                if not base or not any(ch in base for ch in _COMPLEX_SEL_CHARS):
                    continue  # solo un pseudo de interacción sobre un selector simple
                if sel in seen:
                    continue
                seen.add(sel)
                complex_selectors.append(sel)
    if not complex_selectors:
        return []
    lista = ", ".join(complex_selectors)
    return [Finding("selector_no_soportado", "WARN",
                    f"{len(complex_selectors)} selectores complejos definen color/fondo que este "
                    f"linter no resuelve: [{lista}] — verifica el contraste a mano, o reescríbelos "
                    "como selectores de una sola clase para que el motor los evalúe.", lista)]
# ─────────────────────────────────────────────────────────────────────────────────────────────
# ── FIN MOTOR COMPARTIDO v2
# ─────────────────────────────────────────────────────────────────────────────────────────────


# -- Helpers propios de Movistar -----------------------------------------------------------------
def _resolve_inherited_prop(node: Node, rules: list[tuple[str, dict]], prop: str,
                             variables: dict[str, str] | None = None) -> str | None:
    """Como `_resolve_prop` pero simulando herencia CSS real: el propio nodo, o el primer ancestro
    que declare `prop`. Necesario para `font-family` — casi ningún `<p>`/`<span>` la declara en su
    propia regla, la hereda de `body`/un contenedor (`.mvst-h1`, etc.)."""
    for n in [node, *node.ancestors()]:
        val = _resolve_prop(n, rules, prop, variables)
        if val:
            return val
    return None


def _first_family_token(family_value: str) -> str:
    return family_value.split(",")[0].strip().strip("'\"").lower()


def _under_head(node: Node) -> bool:
    """True si el nodo (o algún ancestro) es <head> — su texto (p.ej. `<title>`) no es contenido
    visible del cuerpo del artifact, así que no debe disparar las reglas de copy/tipografía."""
    return node.tag == "head" or any(a.tag == "head" for a in node.ancestors())


# -- Checks individuales de Movistar --------------------------------------------------------------

def check_gradients(css_text: str, variables: dict[str, str] | None = None) -> list[Finding]:
    """Movistar es COLOR PLANO (brand/color-palette.md §4): CUALQUIER degradado es FAIL (a diferencia
    de Mahou, que sí los permite con allowlist). `css_text` = html_text + hojas enlazadas inlineadas,
    así se cubren degradados en `<style>`/`:root` y en `style="..."` inline."""
    out = []
    seen: set[str] = set()
    for m in _GRADIENT_START_RE.finditer(css_text):
        snippet = css_text[max(0, m.start() - 12):m.start() + 40].strip()
        if snippet in seen:
            continue
        seen.add(snippet)
        out.append(Finding("color_plano", "FAIL",
                            "Movistar es color plano: no se permiten degradados "
                            f"({m.group(1).lower()}-gradient). Usa un color sólido de la paleta "
                            "(brand/color-palette.md §4).", snippet))
    return out


_EMDASH_RE = re.compile("—")  # — em-dash (U+2014)
# "movistar" con m minúscula como palabra de marca, excluyendo URLs/dominios/emails (movistar://, .es…)
_MOVISTAR_LOWER_RE = re.compile(r"(?<![\w/@.:-])movistar(?![\w.:/@-])")
_EXCL_OPEN_RE = re.compile("¡")   # ¡
_QUES_OPEN_RE = re.compile("¿")   # ¿


def check_brand_text(root: Node) -> list[Finding]:
    """Reglas de copy de Movistar verificables sobre TEXTO VISIBLE (nunca sobre atributos/URLs, así
    `movistar://<id>` en un `src` no dispara nada). Ver SKILL.md §"Reglas que más se incumplen" y
    brand/copywriting.md §1.3:
    - em-dash "—" prohibido (regla nº1) -> FAIL.
    - "M" de Movistar siempre en mayúscula (principio 1): "movistar" en minúscula -> FAIL.
    - exclamaciones/preguntas SÍ permitidas (principio 12) pero SIEMPRE con signo de apertura RAE:
      "!"/"?" sin su "¡"/"¿" en el mismo nodo -> WARN (puede ser texto partido entre nodos)."""
    out = []
    for node in root.iter_all():
        text = node.text.strip()
        if not text or _under_head(node):
            continue
        if _EMDASH_RE.search(text):
            out.append(Finding("em_dash", "FAIL",
                                'Em-dash "—" en el copy — Movistar no lo usa; sustituye por comas, '
                                "dos puntos o frases cortas (SKILL.md regla nº1, brand/copywriting.md "
                                "§1.3).", text[:80]))
        if _MOVISTAR_LOWER_RE.search(text):
            out.append(Finding("marca_m_minuscula", "FAIL",
                                '"movistar" con "m" minúscula en texto visible — la M de Movistar va '
                                "SIEMPRE en mayúscula (brand/copywriting.md §1.3 principio 1).",
                                text[:80]))
        if "!" in text and not _EXCL_OPEN_RE.search(text):
            out.append(Finding("exclamacion_sin_apertura", "WARN",
                                'Signo "!" de cierre sin su "¡" de apertura en el mismo texto — '
                                "Movistar sigue la RAE (apertura + cierre) en exclamaciones "
                                "(brand/copywriting.md §1.3 principio 12). Confírmalo si el texto se "
                                "parte entre nodos.", text[:80]))
        if "?" in text and not _QUES_OPEN_RE.search(text):
            out.append(Finding("interrogacion_sin_apertura", "WARN",
                                'Signo "?" de cierre sin su "¿" de apertura en el mismo texto — '
                                "Movistar sigue la RAE (apertura + cierre) en interrogaciones "
                                "(brand/copywriting.md §1.3 principio 12). Confírmalo si el texto se "
                                "parte entre nodos.", text[:80]))
    return out


_TITULAR_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
_TITULAR_CLASS_RE = re.compile(r"\b(titular|headline|hero-title|mvst-h[1-6]|display|eyebrow)\b", re.I)
_ELLIPSIS_END_RE = re.compile(r"(\.\.\.|…)$")


def check_titular_period(root: Node, rules: list[tuple[str, dict]],
                          variables: dict[str, str] | None = None) -> list[Finding]:
    """Titulares abiertos, sin punto final (brand/copywriting.md §1.3 principio 14; SKILL.md regla
    nº2). Los puntos suspensivos ("..."/"…") SÍ se permiten (principio 13), así que se eximen.
    WARN (no FAIL): distinguir titular de cuerpo por heurística (etiqueta h1-h6 / clase de titular)
    no es 100% fiable, y un punto en un caso legítimo no debe bloquear."""
    out = []
    for node in root.iter_all():
        text = node.text.strip()
        if not text:
            continue
        is_titular = (node.tag in _TITULAR_TAGS
                      or any(_TITULAR_CLASS_RE.search(c) for c in node.classes))
        if not is_titular or _ELLIPSIS_END_RE.search(text):
            continue
        if text.endswith("."):
            out.append(Finding("titular_con_punto", "WARN",
                                "Titular terminado en punto — los titulares de Movistar van abiertos, "
                                "sin punto final (brand/copywriting.md §1.3 principio 14). Los puntos "
                                "suspensivos sí se permiten.", text[:80]))
    return out


_PURE_BW_RE = re.compile(r"#(?:ffffff|fff|000000|000)(?![0-9a-fA-F])", re.I)


def check_pure_black_white(html_text: str) -> list[Finding]:
    """Blanco/negro puros prohibidos (SKILL.md regla nº5): usa Blanco Movistar #fffaf5 / Negro
    Movistar #262423. Solo hex sólido de 3/6 dígitos — un hex de 4/8 dígitos (con alfa, p.ej.
    #00000080) NO se marca (scrim/sombra rgba legítimos)."""
    out = []
    seen: set[str] = set()
    for m in _PURE_BW_RE.finditer(html_text):
        h = m.group(0).lower()
        norm = "#ffffff" if h in ("#fff", "#ffffff") else "#000000"
        if norm in seen:
            continue
        seen.add(norm)
        alt = "Blanco Movistar #fffaf5" if norm == "#ffffff" else "Negro Movistar #262423"
        out.append(Finding("blanco_negro_puro", "FAIL",
                            f"{norm} (puro) usado como color — Movistar no usa blanco/negro puros; "
                            f"usa {alt} (brand/color-palette.md §4.1/§4.5, SKILL.md regla nº5).", h))
    return out


def check_prohibited_combos(root: Node, rules: list[tuple[str, dict]],
                             variables: dict[str, str] | None = None) -> list[Finding]:
    """Matriz "Prohibido" de brand/contrast-matrix.md: un color CLARO (Blanco Movistar o un
    secundario claro) como texto/grafismo sobre un fondo CLARO. Caso estáticamente decidible (ambos
    resueltos a hex conocidos de la gama clara) -> FAIL con el nombre de regla de marca concreto. El
    caso general de contraste bajo lo cubre check_contrast (que salta este caso para no duplicar)."""
    out = []
    for node in root.iter_all():
        if not node.text.strip() or _under_head(node):
            continue
        if _media_backdrop_container(node, rules):
            continue  # texto sobre foto: lo cubre check_text_over_image, no "claro sobre claro"
        fg, bg, bg_grad = _resolve_fg_bg(node, rules, variables)
        if not fg or not bg:
            continue
        if _hex_of(fg).lstrip("#") in _LIGHT_HEXES and _hex_of(bg).lstrip("#") in _LIGHT_HEXES:
            out.append(Finding("combinacion_prohibida", "FAIL",
                                "Texto/grafismo en un color CLARO (Blanco Movistar o secundario claro) "
                                "sobre fondo CLARO — combinación \"Prohibido\" de la matriz de "
                                "contraste (brand/contrast-matrix.md). Sobre claros usa Negro "
                                "Movistar.", node.text.strip()[:80]))
    return out


def check_contrast(root: Node, rules: list[tuple[str, dict]],
                    variables: dict[str, str] | None = None) -> list[Finding]:
    """MANTENIDO (motor WCAG genérico). Salta fondos de foto (check_text_over_image lo cubre), fondos
    de degradado (Movistar no los permite; check_gradients ya los marca) y el caso claro-sobre-claro
    (check_prohibited_combos le da el nombre de marca)."""
    out = []
    for node in root.iter_all():
        if not node.text.strip():
            continue
        if _media_backdrop_container(node, rules):
            continue
        fg, bg, bg_grad = _resolve_fg_bg(node, rules, variables)
        if bg_grad or not fg or not bg:
            continue
        if _hex_of(fg).lstrip("#") in _LIGHT_HEXES and _hex_of(bg).lstrip("#") in _LIGHT_HEXES:
            continue  # cubierto por check_prohibited_combos
        ratio = _contrast_ratio(fg, bg)
        threshold = 3.0 if _is_large_text(node, rules, variables) else 4.5
        if ratio < threshold:
            out.append(Finding("contraste_bajo", "FAIL",
                                f"Contraste {ratio:.2f}:1 entre texto y fondo — por debajo del mínimo "
                                f"AA para este tamaño ({threshold}:1). Ver brand/contrast-matrix.md "
                                "para los pares canónicos.", node.text.strip()[:80]))
    return out


_GENERIC_FAMILIES = {
    "sans-serif", "serif", "monospace", "system-ui", "ui-sans-serif", "ui-monospace", "ui-serif",
    "inherit", "initial", "unset", "revert", "-apple-system", "blinkmacsystemfont", "cursive",
    "fantasy", "emoji", "math", "fangsong",
}


def check_font_family(root: Node, rules: list[tuple[str, dict]],
                       variables: dict[str, str] | None = None) -> list[Finding]:
    """La marca usa Movistar Sans (SKILL.md regla nº3, brand/typography.md §3). El texto visible debe
    resolver una `font-family` cuyo primer token sea 'Movistar Sans'. Un primer token que sea OTRA
    fuente concreta (no genérica) -> FAIL. Si ningún ancestro declara font-family (cae a fuente de
    sistema) -> WARN (declara explícitamente 'Movistar Sans'; el runtime la inyecta en artifacts web)."""
    out = []
    warned_missing = False
    seen_bad: set[str] = set()
    for node in root.iter_all():
        if not node.text.strip() or _under_head(node):
            continue
        family = _resolve_inherited_prop(node, rules, "font-family", variables)
        if not family:
            if not warned_missing:
                warned_missing = True
                out.append(Finding("fuente_no_declarada", "WARN",
                                    "Texto de marca sin ninguna `font-family` declarada ni heredada — "
                                    "caerá a la fuente del sistema. Declara `font-family:'Movistar "
                                    "Sans'` (el runtime la inyecta en artifacts web).",
                                    node.text.strip()[:80]))
            continue
        first = _first_family_token(family)
        if not first or "movistar sans" in first or first == "movistar" or first.startswith("var("):
            continue
        if first in _GENERIC_FAMILIES:
            continue
        if first in seen_bad:
            continue
        seen_bad.add(first)
        out.append(Finding("fuente_no_movistar", "FAIL",
                            f"Texto de marca en '{first}' — la marca usa Movistar Sans "
                            "(brand/typography.md §3). Escribe `font-family:'Movistar Sans'` (el "
                            "runtime la inyecta; no pegues @font-face base64).",
                            node.text.strip()[:80]))
    return out


_FONTFACE_BLOCK_RE = re.compile(r"@font-face\s*\{([^{}]*)\}", re.S | re.I)


def check_fontface_not_pasted(html_text: str) -> list[Finding]:
    """INVERSIÓN respecto a las otras marcas. El runtime de artifact-flow inyecta Movistar Sans en
    los artifacts web (`injectBrandFont`, gated a movistar) — pegar el `@font-face` con la fuente en
    base64 (`url(data:...)`) es innecesario, cuesta ~15s de tokens y arriesga cortar el stream
    (docs/FONT-RUNTIME-INJECTION-PROPOSAL.md) -> FAIL. Un `@font-face` con `url('file://...')` (ruta
    de fichero, para HTML standalone / PDF WeasyPrint) SÍ está permitido y no se marca."""
    out = []
    for m in _FONTFACE_BLOCK_RE.finditer(html_text):
        block = m.group(1)
        if "url(data:" in block.replace(" ", "").lower():
            fam_m = re.search(r"font-family\s*:\s*['\"]?([^;'\"]+)", block, re.I)
            fam = fam_m.group(1).strip() if fam_m else "?"
            out.append(Finding("fontface_base64_pegado", "FAIL",
                                f"@font-face con la fuente en base64 (`url(data:...)`) para '{fam}' — "
                                "en Movistar el runtime inyecta la fuente en artifacts web; NO pegues "
                                "el base64 (ralentiza y puede cortar el stream). Escribe solo "
                                "`font-family:'Movistar Sans'`. Para HTML standalone/PDF usa "
                                "`url('file://...')`, no base64 (SKILL.md §Tipografía).", block[:80]))
    return out


def check_images(root: Node, rules: list[tuple[str, dict]]) -> list[Finding]:
    """MANTENIDO — genérico, sin cambios respecto a las otras marcas."""
    out = []
    for node in root.iter_all():
        if node.tag != "img":
            continue
        attrs = node.attrs
        style = node.inline_style
        has_w = "width" in attrs or "width" in style
        has_h = "height" in attrs or "height" in style
        has_object_fit = "object-fit" in style or _resolve_prop(node, rules, "object-fit")
        if not (has_w and has_h):
            out.append(Finding("img_sin_dimensiones", "FAIL",
                                "<img> sin width/height explícitos — puede desbordar su contenedor y "
                                "solapar el texto siguiente.", str(attrs)[:100]))
        elif not has_object_fit:
            out.append(Finding("img_sin_object_fit", "WARN",
                                "<img> con dimensiones pero sin object-fit — si la proporción real no "
                                "coincide con el hueco, puede deformarse o desbordar.", str(attrs)[:100]))
    return out


_SCRIM_CLASS_RE = re.compile(r"scrim", re.I)


def check_text_over_image(root: Node, rules: list[tuple[str, dict]],
                           variables: dict[str, str] | None = None) -> list[Finding]:
    """MANTENIDO — texto sobre foto (`background:url(...)` o `<img>` de fondo) necesita un scrim
    (clase con 'scrim') o z-index explícito en el texto (SKILL.md regla nº8, §Accesibilidad)."""
    out = []
    seen_containers: set[int] = set()
    for node in root.iter_all():
        bg = (_resolve_prop(node, rules, "background-image", variables)
              or _resolve_prop(node, rules, "background", variables))
        is_photo_container = bool(bg and "url(" in bg)
        container = node if is_photo_container else _media_backdrop_container(node, rules)
        if not container or id(container) in seen_containers:
            continue
        text_descendants = [n for n in container.iter_all()
                            if n is not container and n.tag != "img" and n.text.strip()]
        if not text_descendants:
            continue
        seen_containers.add(id(container))
        has_scrim = any(_SCRIM_CLASS_RE.search(" ".join(n.classes))
                        for n in [container, *container.iter_all()])
        has_zindex_on_text = any(
            "z-index" in d.inline_style or _resolve_prop(d, rules, "z-index", variables)
            for t in text_descendants
            for d in [t, *_ancestors_until(t, container)]
        )
        if not has_scrim and not has_zindex_on_text:
            out.append(Finding("texto_sobre_foto_sin_scrim", "FAIL",
                                "Texto sobre foto sin clase de scrim ni z-index explícito — revisa el "
                                "contraste real contra la zona concreta de la foto "
                                "(brand/contrast-matrix.md; SKILL.md regla nº8).",
                                text_descendants[0].text.strip()[:80]))
    return out


def check_positioning(root: Node, rules: list[tuple[str, dict]]) -> list[Finding]:
    """MANTENIDO — genérico, sin cambios."""
    out = []
    has_any_relative = any(
        _resolve_prop(n, rules, "position") in ("relative", "absolute", "fixed") for n in root.iter_all()
    )
    for node in root.iter_all():
        pos = _resolve_prop(node, rules, "position")
        if pos not in ("absolute", "fixed"):
            continue
        positioned_ancestor = any(
            _resolve_prop(a, rules, "position") in ("relative", "absolute", "fixed") for a in node.ancestors()
        )
        if not positioned_ancestor:
            sev = "WARN" if has_any_relative else "FAIL"
            out.append(Finding("absolute_sin_relative", sev,
                                f"<{node.tag}> con position:{pos} sin ningún ancestro con "
                                "position:relative dimensionado — se posicionará respecto al "
                                "viewport/página completa, probable causa de solapamiento real.",
                                str(node.attrs)[:100]))
    return out


def check_movistar_hero_overlay(root: Node, rules: list[tuple[str, dict]]) -> list[Finding]:
    """La capa `.mvst-over` debe cubrir realmente el hero; z-index sin overlay la deja fuera."""
    out = []
    for node in root.iter_all():
        if "mvst-over" not in node.classes:
            continue
        position = _resolve_prop(node, rules, "position")
        inset = _resolve_prop(node, rules, "inset")
        has_edges = all(_resolve_prop(node, rules, edge) is not None
                        for edge in ("top", "right", "bottom", "left"))
        if position != "absolute" or not (inset is not None or has_edges):
            out.append(Finding(
                "hero_overlay_no_cubre", "FAIL",
                ".mvst-over debe usar position:absolute y cubrir el contenedor con inset o los "
                "cuatro bordes; position:relative + z-index deja el texto fuera de la foto.",
                str(node.attrs)[:100],
            ))
    return out


def check_duplicate_svg(html_text: str) -> list[Finding]:
    """MANTENIDO — Movistar SÍ tiene SVG limpio del logo (la "M", `assets/logo/*.svg`) — este check
    es activamente relevante: si la M se incrusta más de una vez, usar `<symbol>`+`<use>`."""
    out = []
    paths = re.findall(r'<path\s+[^>]*\bd="([^"]{40,})"', html_text)
    seen: dict[str, int] = {}
    for p in paths:
        seen[p] = seen.get(p, 0) + 1
    dupes = [p for p, n in seen.items() if n >= 2]
    has_symbol_use = "<symbol" in html_text and "<use" in html_text
    if dupes and not has_symbol_use:
        out.append(Finding("logo_duplicado", "WARN",
                            f"Un mismo <path> aparece {max(seen.values())} veces sin usar el patrón "
                            "<symbol>+<use> — duplica el payload del artifact innecesariamente (la M "
                            "es un solo path).", dupes[0][:60] + "…"))
    return out


_CLASS_TOKEN_RE = re.compile(r"\.([\w-]+)")


def check_undefined_classes(root: Node, rules: list[tuple[str, dict]]) -> list[Finding]:
    """MANTENIDO — genérico (bug real que lo motivó: una clase usada pero nunca definida se queda con
    el estilo por defecto del navegador, en silencio)."""
    defined = set()
    for sel, _ in rules:
        defined.update(_CLASS_TOKEN_RE.findall(sel))
    out = []
    seen = set()
    for node in root.iter_all():
        for cls in node.classes:
            if cls not in defined and cls not in seen:
                seen.add(cls)
                out.append(Finding("clase_sin_definir", "FAIL",
                                    f"La clase '.{cls}' se usa en el HTML pero ninguna regla CSS la "
                                    "define — el elemento se queda con el estilo por defecto del "
                                    "navegador, en silencio.", f'class="{cls}"'))
    return out


def check_out_of_palette(html_text: str, palette_hex: set[str]) -> list[Finding]:
    """MANTENIDO — genérico. `palette_hex` ya incluye principales + secundarios (claros y oscuros) +
    grises §4.5 + semánticos (ver `_load_palette_hex`), así que usarlos no dispara este WARN."""
    out = []
    seen = set()
    for m in _HEX_RE.finditer(html_text):
        h = m.group(0).lower()
        if len(h) == 4:
            h = "#" + "".join(c * 2 for c in h[1:])
        if h in seen or h in palette_hex:
            continue
        seen.add(h)
        out.append(Finding("color_fuera_paleta", "WARN",
                            f"Color {h} no está en la paleta de marca "
                            "(assets/colors/palette.generated.json) — confirma que es intencional "
                            "(p.ej. un tono de foto) y no un color inventado.", h))
    return out


# -- Orquestación -------------------------------------------------------------------------------
def lint(html_text: str, base_dir: Path | None = None) -> list[Finding]:
    """`base_dir` (opcional): carpeta del fichero .html original, para resolver `<link
    rel="stylesheet" href="...">` locales. `None` (llamada como librería solo con texto en memoria)
    simplemente omite ese paso."""
    root = parse_html(html_text)
    css_text = _inline_linked_stylesheets(html_text, base_dir)
    rules = _extract_css_rules(css_text)
    variables = _extract_css_variables(css_text)
    palette_hex = _load_palette_hex()
    findings: list[Finding] = []
    findings += check_gradients(css_text, variables)
    findings += check_brand_text(root)
    findings += check_titular_period(root, rules, variables)
    findings += check_pure_black_white(html_text)
    findings += check_prohibited_combos(root, rules, variables)
    findings += check_contrast(root, rules, variables)
    findings += check_font_family(root, rules, variables)
    findings += check_fontface_not_pasted(html_text)
    findings += check_images(root, rules)
    findings += check_text_over_image(root, rules, variables)
    findings += check_positioning(root, rules)
    findings += check_movistar_hero_overlay(root, rules)
    findings += check_duplicate_svg(html_text)
    findings += check_undefined_classes(root, rules)
    findings += check_out_of_palette(html_text, palette_hex)
    findings += check_unsupported_selectors(html_text)
    return findings


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) != 2:
        print("Uso: python3 lint_artifact.py <fichero.html>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"No existe: {path}", file=sys.stderr)
        return 2
    html_text = path.read_text(encoding="utf-8")
    findings = lint(html_text, base_dir=path.parent)
    fails = [f for f in findings if f.severity == "FAIL"]
    warns = [f for f in findings if f.severity == "WARN"]
    if not findings:
        print("[lint_artifact] OK — sin hallazgos.")
        return 0
    print(f"[lint_artifact] {len(fails)} FAIL, {len(warns)} WARN\n")
    for f in fails + warns:
        print(f"[{f.severity}] {f.rule}: {f.detail}")
        if f.snippet:
            print(f"   snippet: {f.snippet!r}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
