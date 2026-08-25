#!/usr/bin/env python3
"""
mvst_pptx.py (v4) — Motor de decks Movistar: CLONA la diapositiva real que mejor encaja el
contenido y rellena su texto/imágenes. La "diapo-diseño" ES la unidad de trabajo, igual que
si un humano duplicara en PowerPoint la diapositiva de ejemplo correcta y editara su
contenido. No hay recomendador de scoring ni layouts abstractos que rellenar por rol.

QUÉ CAMBIA EN LA v4 — EL CATÁLOGO LO CONSULTA EL MOTOR, NO EL MODELO
--------------------------------------------------------------------
La v3 tenía 54 arquetipos y su catálogo (`references/slides-catalog-movistar.json`) pesaba
~180 KB: abrirlo era caro pero posible, y el `SKILL.md` mandaba hacerlo para sacar los
`shape_name`. La v4 tiene **156 arquetipos en dos sistemas de diseño** y ese mismo fichero
pesa **1,1 MB (~330.000 tokens)**: leerlo no cabe en el turno de 20 minutos de SuperStudio.

Así que el contrato se INVIERTE. El catálogo lo carga el MOTOR en memoria, y el modelo le
pregunta al motor:

    families()                      panorama: 12 familias, su arquetipo por defecto
    find_slides(...)                filtra por familia/rol/nº de bloques/foto/gráfica/…
    describe("NOMBRE")              ficha corta: cuándo sí, cuándo no, hermanos
    fill_spec(slide_o_nombre)       SOLO la tabla de relleno de una diapositiva
    use(deck, "NOMBRE")             clona Y **imprime su propio fill-spec**

`use()` imprimiendo su fill-spec es la pieza que cierra el sistema, por dos razones:

1. Elimina el único motivo legítimo que quedaba para abrir el JSON (sacar un `shape_name`).
2. Hace **estructuralmente imposible** el bug clásico de esta plantilla: un `shape_name`
   ("Title 2", "cuerpo_1", "Text Placeholder 4"…) NO es único entre diapositivas distintas,
   solo dentro de la suya. Con el fill-spec, el modelo recibe los nombres de ESA
   diapositiva, no de una parecida.

El precio son ~85 tokens por diapositiva clonada (opt-out con `use(..., quiet=True)`), muy
por debajo de lo que cuesta una sola consulta al catálogo.

DOS SISTEMAS DE DISEÑO EN UN MISMO .PPTX
----------------------------------------
La plantilla trae DOS `slideMaster`: `refresh-2025` (vigente, 27 layouts, arquetipos SIN
sufijo) y `clasico` (101 layouts, arquetipos con sufijo `_CLASICO`). Los dos son material
oficial del cliente y los dos son válidos; **no se mezclan en el mismo deck** salvo petición
explícita, porque son dos lenguajes visuales distintos. `verify_deck()` avisa si un deck
queda con un master minoritario residual y propone el hermano equivalente del dominante.

`set_page_header()` — divergencia deliberada frente a `sm_pptx.set_deck_title()`
------------------------------------------------------------------------------
San Miguel tiene una cabecera genuinamente COMPARTIDA y repetida idéntica en 61/72
diapositivas, de ahí que su `set_deck_title(deck, title)` reciba el DECK y se llame una vez.
En Movistar el "título de página" de cada diapositiva interior es contenido PROPIO y DISTINTO
de esa diapositiva (verificado contra el XML: cada arquetipo trae su propio "Título de página
Movistar Sans NNpt" de ejemplo, no un valor compartido) — rellenarlo con el mismo texto en
todas sería activamente incorrecto. Por eso `set_page_header()` recibe la SLIDE y se llama
UNA VEZ POR CADA diapositiva de contenido, igual que `set_text()`. Lo que sí comparte con San
Miguel es la razón de ser: abstraer el nombre real del título/subtítulo (que varía de
arquetipo a arquetipo) resolviéndolo por el `role` del catálogo. **18 de los 156 arquetipos
no tienen zona de título** (los cierres sin texto, los separadores cuyo único texto es el
nombre del capítulo, las citas cuya zona protagonista es `display`): en ellos la función
LANZA a propósito —elegir uno de esos para una página de contenido con cabecera es un error
de elección, no un caso a degradar en silencio— y el mensaje lista las zonas que SÍ tiene.

PROHIBIDO crear `Presentation()` en blanco, usar otra plantilla u otra fuente que la
embebida. Si `new_deck()` no encuentra la plantilla oficial: DETENTE y repórtalo.
"""
from __future__ import annotations
import copy
import difflib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.oxml import parse_xml
from pptx.oxml.ns import qn
from pptx.util import Cm

_SKILL_DIR = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
_REFS = _SKILL_DIR / "references"
_TPL_DIR = _SKILL_DIR / "assets" / "template"
_CATALOG_PATH = _REFS / "slides-catalog-movistar.json"
_BRAND_CONFIG_PATH = _SKILL_DIR / "assets" / "brand-config.json"

__version__ = "4.0.0"


def enable_utf8_stdout() -> None:
    """La consola de desarrollo de esta skill es cp1252: un `print()` con una flecha o un
    acento mata el script con `UnicodeEncodeError` DESPUÉS de haber hecho el trabajo. El
    sandbox de producción ya es UTF-8, así que esto es idempotente y gratis allí."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):  # stream redirigido o ya cerrado
            pass


enable_utf8_stdout()

_BRAND_CONFIG_CACHE: dict | None = None


def brand_config() -> dict:
    """`assets/brand-config.json` — fuente ÚNICA de los gates de QA deterministas
    (`qa_gates`) y del sistema de color de capítulos. No hardcodear umbrales en el código:
    si cambian, cambian ahí (y se regenera el catálogo para que la prosa de
    `references/slides-index.md` siga derivándose de estos valores)."""
    global _BRAND_CONFIG_CACHE
    if _BRAND_CONFIG_CACHE is None:
        _BRAND_CONFIG_CACHE = json.loads(_BRAND_CONFIG_PATH.read_text(encoding="utf-8"))
    return _BRAND_CONFIG_CACHE


_CATALOG_CACHE: dict | None = None


def catalog() -> dict:
    """Catálogo completo en memoria. **No lo imprimas ni lo serialices**: son 1,1 MB.
    Úsalo por la API de consulta (`families()`/`find_slides()`/`describe()`/`fill_spec()`)."""
    global _CATALOG_CACHE
    if _CATALOG_CACHE is None:
        _CATALOG_CACHE = json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))
    return _CATALOG_CACHE


# ---------------------------------------------------------------------------
# Alias: canónicos, estrictos y obsoletos
# ---------------------------------------------------------------------------
# ⚠️ `scripts/_contracts.py` (donde viven `STRICT_ALIASES`/`DEPRECATED_ALIASES` como fuente
# de verdad de build-time) está EXCLUIDO del .zip de producción vía `.skillignore`, así que
# este módulo NO puede importarlo en runtime. El catálogo publica las dos tablas
# (`aliases`/`deprecated_aliases`) precisamente para esto: se leen de ahí, que es la misma
# información serializada por `build_catalog.py` desde `_contracts`. Un solo origen, dos
# superficies.
def _alias_tables() -> tuple[dict, dict]:
    cat = catalog()
    return (cat.get("aliases") or {}), (cat.get("deprecated_aliases") or {})


_ALIAS_WARNED: set[str] = set()


def resolve_name(name: str, *, warn: bool = True) -> str:
    """Alias -> nombre canónico. Acepta los alias estrictos (nombres que la gramática actual
    haría deducir de otra forma) y los obsoletos (los 3 arquetipos que la v3 dibujaba a mano
    con primitivas y que ahora se sirven con el arte REAL del cliente), estos últimos con
    aviso una sola vez por nombre."""
    strict, deprecated = _alias_tables()
    if name in deprecated:
        target = deprecated[name]
        if warn and name not in _ALIAS_WARNED:
            _ALIAS_WARNED.add(name)
            print(f"[deck-qa] '{name}' está OBSOLETO (era una composición dibujada a mano con "
                  f"primitivas); se usa el arte real del cliente '{target}'. ⚠️ Sus zonas NO se "
                  f"llaman igual — fíate del fill-spec que imprime use(), no de tu memoria.")
        return target
    return strict.get(name, name)


def slide_names(*, include_aliases: bool = False) -> list[str]:
    """Nombres válidos para `use()`, en orden de plantilla. Por defecto SOLO los canónicos
    (156); con `include_aliases=True` añade además los alias aceptados como entrada."""
    names = list(catalog()["slides"].keys())
    if not include_aliases:
        return names
    strict, deprecated = _alias_tables()
    return names + sorted(set(strict) | set(deprecated))


def _slide_info(name: str) -> dict:
    """Entrada de catálogo de `name` (resolviendo alias). Lanza con los 5 nombres más
    parecidos — nunca con los 156, que es justo lo que no cabe en el turno."""
    canonical = resolve_name(name)
    slides = catalog()["slides"]
    if canonical in slides:
        return slides[canonical]
    universe = slide_names(include_aliases=True)
    close = difflib.get_close_matches(name, universe, n=5, cutoff=0.45)
    if not close:
        upper = name.upper()
        close = [n for n in universe if upper in n][:5]
    hint = ("¿querías " + " · ".join(close) + "?") if close else (
        "usa find_slides(family=…) o families() para orientarte")
    raise ValueError(
        f"'{name}' no es un arquetipo de Movistar ({len(slides)} disponibles). {hint}")


# ---------------------------------------------------------------------------
# §CONSULTA — lo que el modelo usa en vez de abrir el JSON
# ---------------------------------------------------------------------------
_SYSTEM_LABEL = {"refresh-2025": "refresh", "clasico": "clásico"}
_TYPE_LABEL = {"text": "txt", "image": "img", "background": "img", "chart": "chart",
               "table": "tabla"}

#: Etiqueta corta del tipo de gráfica, para el fill-spec (§G26): saber que la gráfica del
#: refresh es una TARTA cambia qué datos tiene sentido meterle.
_CHART_TYPE_LABEL = {
    "PIE": "tarta", "PIE_EXPLODED": "tarta", "DOUGHNUT": "anillo",
    "COLUMN_CLUSTERED": "columnas", "COLUMN_STACKED": "columnas apiladas",
    "COLUMN_STACKED_100": "columnas 100%", "BAR_CLUSTERED": "barras",
    "BAR_STACKED": "barras apiladas", "BAR_STACKED_100": "barras 100%",
    "LINE": "líneas", "LINE_MARKERS": "líneas", "AREA": "área",
    "AREA_STACKED": "área apilada", "XY_SCATTER": "dispersión", "RADAR": "radar",
}

#: Tipos de gráfica que representan una PARTE DE UN TOTAL: una serie temporal ahí es un error
#: de lectura, no una preferencia estética.
_PART_OF_WHOLE_CHARTS = ("PIE", "PIE_EXPLODED", "DOUGHNUT")

#: ⚠️ HALLAZGO DE ESTA RONDA, que corrige la premisa con la que se planificó §G18.
#: La plantilla tiene 5 formas AUTO_SHAPE (`roundRect` de color plano, sin `<p:blipFill>`) a las
#: que el build llamó `imagen_N` y a las que el manifiesto asignó `role: image`. El catálogo
#: NO las publica, y la conclusión que se dio por buena era que el catálogo se equivocaba.
#: Es al revés: **no son huecos de foto, son TARJETAS de color**. Medido sobre el binario y
#: confirmado por render, cada una tiene ENCIMA (>50% de solape) una zona de texto `cuerpo_N`
#: escrita en un secundario OSCURO (#38552B verde, #6A2C13 coral) sobre el relleno secundario
#: CLARO de la tarjeta (accent2 CEF7BF, accent4 FFC5A8). Rellenarlas con una foto deja ese
#: texto sin fondo de contraste — exactamente el fallo de marca que prohíbe
#: `movistar-brand-guidelines/brand/contrast-matrix.md`, verificado en el render de prueba
#: (texto verde oscuro ilegible sobre la foto). El `_CAPTION` de sus nombres es un artefacto
#: del heurístico de nombrado, no un pie de foto.
#:
#: La MECÁNICA de convertir una AUTO_SHAPE en hueco de foto sí se implementa (`_inject_blipfill`)
#: y funciona; lo que se añade es el guardarraíl: si la forma tiene texto encima, `set_image()`
#: se niega y explica las dos salidas. Esta tabla es solo para que `fill_spec(NOMBRE)` pueda
#: decirlo ANTES de clonar; con una diapositiva delante manda la geometría real
#: (`_overlapping_text_zone()`).
_COLOR_CARD_ZONES = {
    "INTERIOR_TXT_3IMG_CAPTION_CLASICO": {"imagen_1": "cuerpo_2", "imagen_2": "cuerpo_3",
                                          "imagen_3": "cuerpo_4"},
    "INTERIOR_TXT_2IMG_CAPTION_CLASICO": {"imagen_1": "cuerpo_2", "imagen_2": "cuerpo_3"},
}

#: Nombre que el build da a una zona de imagen. `set_image()` lo usa para decidir si una
#: AUTO_SHAPE sin `blipFill` es un hueco de foto o una forma decorativa: rellenar por error
#: un `Rectángulo 6` decorativo con una foto sería peor que lanzar.
_IMAGE_ZONE_NAME_RE = re.compile(r"^(imagen|foto|image|img|picture)(_\d+)?$", re.IGNORECASE)


def families() -> dict:
    """`{FAMILIA: {n, default, compositions}}` — el panorama en una llamada.

    `n` = arquetipos de la familia · `default` = el que usar si no tienes una razón para
    otro · `compositions` = nº de maquetas físicas distintas (las variantes de color de una
    misma maqueta cuentan como una)."""
    out = {}
    for fam, info in catalog()["families"].items():
        out[fam] = {"n": info["n_archetypes"], "default": info["default"],
                    "compositions": info["n_compositions"]}
    return out


_CARDINAL_IN_NAME_RE = re.compile(r"(?<![A-Z0-9])(\d{1,2})(?:[A-Z]+)?(?![0-9])")


def _name_cardinals(name: str) -> set[int]:
    """Cardinalidades que el propio NOMBRE declara (`5COL`, `3IMG`, `2PANEL`, `15`…).

    Hace falta porque `n_items.bloques` del manifiesto cuenta ZONAS repetidas, no columnas:
    `INDICE_3COL_CLASICO` declara 9 bloques (3 columnas × 3 zonas) y
    `INTERIOR_TXT_6PANEL_CLASICO` declara 7. Cuando el modelo pide "3 bloques" quiere lo que
    dice el nombre, así que `find_slides(n_items=3)` casa contra las dos cosas."""
    return {int(m) for m in _CARDINAL_IN_NAME_RE.findall(name)}


def _blocks_of(info: dict) -> int | None:
    return (info.get("n_items") or {}).get("bloques")


def _has_page_header(info: dict) -> bool:
    """¿Funciona `set_page_header()` en este arquetipo?

    Se deriva de `header.title` (la zona que la función resuelve), NO del campo
    `chrome.has_page_header` del catálogo: ese último es False en arquetipos que sí tienen
    título, subtítulo y número de página (p.ej. `INTERIOR_TXT_1IMG`), porque lo calcula el
    manifiesto con otro criterio. Filtrar por él daría respuestas falsas justo en la pregunta
    que el modelo hace: "¿puedo poner cabecera aquí?"."""
    return bool((info.get("header") or {}).get("title"))


def _color_token(info: dict) -> str | None:
    """Token de color de fondo del arquetipo (`AZUL`, `VERDE`, `CREMA`…), o None si el fondo
    es una foto. Prefiere la variante declarada; si no, el semántico del fondo resuelto."""
    variant = info.get("variant") or {}
    if variant.get("axis") == "color" and variant.get("value"):
        return variant["value"]
    return info.get("bg_semantic")


def _preferred_system() -> str | None:
    """Sistema que ya domina el deck en construcción (`refresh-2025`/`clasico`), o None si
    aún no hay nada clonado. `find_slides()` lo usa para ordenar: cuando el deck ya va por el
    clásico, ofrecerle primero arquetipos del refresh sería empujarle a mezclar sistemas."""
    if not _USED_SYSTEMS:
        return None
    top = _USED_SYSTEMS.most_common()
    if len(top) > 1 and top[0][1] == top[1][1]:
        return None  # empate: es una decisión del modelo, no una preferencia del motor
    return top[0][0]


#: Contador de sistemas clonados en el turno (lo alimenta `use()`), por si hay varios decks.
_USED_SYSTEMS: Counter = Counter()


def find_slides(*, family: str | None = None, role_in_deck: str | None = None,
                n_items: int | None = None, has_image: bool | None = None,
                has_chart: bool | None = None, has_table: bool | None = None,
                has_page_header: bool | None = None, variant: str | None = None,
                master: str | None = None, composition_id: str | None = None,
                limit: int = 8, verbose: bool = False) -> list[str]:
    """Nombres de arquetipo que cumplen TODOS los filtros dados, los mejores primero.

    Sustituye a abrir el catálogo. Filtros (todos opcionales, todos AND):

        family          "INTERIOR", "SEPARADOR", … (ver families(); acepta minúsculas)
        role_in_deck    cover|index|divider|content|comparison|timeline|closing|legal
        n_items         nº de bloques repetidos: casa contra la cardinalidad del NOMBRE
                        (`5COL`, `3IMG`) o contra `n_items.bloques`
        has_image       True/False -> tiene (o no) hueco de foto
        has_chart       True/False -> gráfica nativa editable
        has_table       True/False -> tabla nativa
        has_page_header True/False -> set_page_header() funciona (False = los 18 sin título)
        variant         token de color de fondo: "AZUL","VERDE","CREMA","NEGRO",…
        master          "refresh" | "clasico" (o el nombre completo del sistema)
        composition_id  todos los hermanos de una maqueta concreta

    Orden: **los `[C]` por defecto de su familia primero**, después el sistema que ya domina
    el deck en construcción (para no empujar a mezclar), después por nombre. `limit=8` porque
    una lista de 40 nombres no ayuda a decidir; `verbose=True` imprime además una línea por
    resultado con familia/rol/zonas.

    Devuelve la lista (además de imprimirla, para que sea encadenable).
    """
    slides = catalog()["slides"]
    fam = family.upper() if family else None
    if fam is not None and fam not in catalog()["families"]:
        close = difflib.get_close_matches(fam, list(catalog()["families"]), n=3, cutoff=0.4)
        raise ValueError(f"familia '{family}' no existe. Disponibles: "
                         f"{' · '.join(catalog()['families'])}"
                         + (f" (¿{close[0]}?)" if close else ""))
    want_master = None
    if master:
        m = master.lower()
        want_master = ("refresh-2025" if m.startswith("refresh")
                       else "clasico" if m.startswith("clas") else master)
    want_variant = variant.upper() if variant else None
    comp_id = composition_id

    hits: list[str] = []
    for name, info in slides.items():
        slots = info.get("slots") or {}
        if fam and info.get("family") != fam:
            continue
        if role_in_deck and info.get("role_in_deck") != role_in_deck:
            continue
        if want_master and info.get("system") != want_master:
            continue
        if comp_id and info.get("composition_id") != comp_id:
            continue
        if want_variant and _color_token(info) != want_variant:
            continue
        if n_items is not None and n_items not in _name_cardinals(name) | {_blocks_of(info)}:
            continue
        for flag, key in ((has_image, "image"), (has_chart, "chart"), (has_table, "table")):
            if flag is None:
                continue
            present = bool(slots.get(key)) or (key == "image" and info.get("has_background_image"))
            if bool(flag) != present:
                break
        else:
            if has_page_header is not None and bool(has_page_header) != _has_page_header(info):
                continue
            hits.append(name)

    preferred = _preferred_system()
    hits.sort(key=lambda n: (
        not slides[n].get("is_default"),
        0 if (preferred and slides[n]["system"] == preferred) else 1,
        n,
    ))
    total = len(hits)
    out = hits[:max(1, limit)]
    if not out:
        print("[find_slides] 0 resultados con esos filtros — relaja el más específico "
              "(n_items o variant suelen ser los que sobran) o mira families().")
        return []
    print(f"[find_slides] {total} resultado(s)"
          + (f", los {len(out)} primeros" if total > len(out) else "") + ":")
    for name in out:
        info = slides[name]
        mark = " [C]" if info.get("is_default") else ""
        if verbose:
            print(f"  {name}{mark} · {info['family']}/{info['role_in_deck']} · "
                  f"{_SYSTEM_LABEL.get(info['system'], info['system'])} · {_zones_summary(name)}")
        else:
            print(f"  {name}{mark}")
    if total > len(out):
        print(f"  … +{total - len(out)} más (sube limit= si de verdad los necesitas)")
    return out


def _zones_summary(name: str) -> str:
    info = _slide_info(name)
    slots = info.get("slots") or {}
    parts = [f"{info.get('n_text_zones', 0)} txt"]
    for n, label in ((slots.get("image") or 0, "img"), (slots.get("chart") or 0, "chart"),
                     (slots.get("table") or 0, "tabla"),
                     (len(_color_card_zones(name)), "tarjeta color")):
        if n:
            parts.append(f"{n} {label}")
    blocks = _blocks_of(info)
    if blocks:
        parts.append(f"{blocks} bloques/{(info.get('n_items') or {}).get('eje')}")
    return " · ".join(parts)


def _color_card_zones(name: str) -> dict:
    """`{zona_tarjeta: zona_de_texto_encima}` del arquetipo (ver `_COLOR_CARD_ZONES`)."""
    return _COLOR_CARD_ZONES.get(resolve_name(name, warn=False), {})


def _cross_system_twin(name: str) -> str | None:
    """Arquetipo equivalente en el OTRO sistema de diseño, o None.

    `composition_id` es `<sistema>.<maqueta>`, así que el gemelo exacto es la misma `<maqueta>`
    bajo el otro prefijo (`refresh2025.interior.txt.2img` <-> `clasico.interior.txt.2img`). Si esa
    maqueta no existe al otro lado, se elige de la MISMA familia y el MISMO rol de deck el
    candidato con la firma estructural más cercana (nº de zonas de texto, fotos, gráficas,
    tablas, bloques). Caer al `[C]` de la familia sin más daba sustituciones malas: para un
    `SEPARADOR_NUMERO_04_VERDE` (2 zonas, un número y un título) proponía la agenda de cinco
    columnas del clásico."""
    info = _slide_info(name)
    comp = info.get("composition_id") or ""
    if "." not in comp:
        return None
    _, tail = comp.split(".", 1)
    comps = catalog()["compositions"]
    for other_id, other in comps.items():
        if other_id == comp or other["system"] == info["system"]:
            continue
        if other_id.split(".", 1)[1] == tail:
            return other["base"]

    slides = catalog()["slides"]

    def signature(s: dict) -> tuple:
        slots = s.get("slots") or {}
        return (s.get("n_text_zones") or 0, slots.get("image") or 0, slots.get("chart") or 0,
                slots.get("table") or 0, _blocks_of(s) or 0)

    def data_kind(s: dict) -> tuple:
        slots = s.get("slots") or {}
        return (bool(slots.get("chart")), bool(slots.get("table")))

    mine, mine_data = signature(info), data_kind(info)
    best, best_dist = None, None
    for n, s in slides.items():
        if s["system"] == info["system"]:
            continue
        dist = sum(abs(a - b) for a, b in zip(mine, signature(s)))
        # Llevar gráfica o tabla pesa MÁS que la familia: `INTERIOR_CHART` es familia INTERIOR y
        # su equivalente clásico es `DATOS_CHART_CLASICO` (familia DATOS), así que restringir la
        # búsqueda a la familia daba sustituciones sin gráfica para una diapositiva de datos.
        if data_kind(s) != mine_data:
            dist += 40
        if s["family"] != info["family"]:
            dist += 6
        if s.get("role_in_deck") != info.get("role_in_deck"):
            dist += 5
        if s.get("background_treatment") != info.get("background_treatment"):
            dist += 2
        if not s.get("is_default"):
            dist += 0.5      # a igualdad de firma, el [C] de la familia
        if best_dist is None or dist < best_dist:
            best, best_dist = n, dist
    return best


def _wrap(text: str, *, indent: str = "    ", width: int = 112, max_chars: int) -> list[str]:
    import textwrap
    t = " ".join(str(text or "").split())
    if len(t) > max_chars:
        cut = t.rfind(". ", 0, max_chars)
        t = (t[:cut + 1] if cut > max_chars * 0.5 else t[:max_chars].rstrip() + "…")
    return textwrap.wrap(t, width=width, initial_indent=indent, subsequent_indent=indent) or []


def describe(slide_name: str) -> None:
    """Ficha corta de un arquetipo: familia, composición, cuándo sí / cuándo no, hermanos y
    de dónde sale. Es el paso 2 cuando el mapa de familias del `SKILL.md` no te determina el
    arquetipo; para las zonas exactas usa `fill_spec()` (o simplemente `use()`, que las
    imprime)."""
    name = resolve_name(slide_name)
    info = _slide_info(name)
    slots = info.get("slots") or {}
    fam_default = (catalog()["families"].get(info["family"]) or {}).get("default")
    mark = "  [C] por defecto de " + info["family"] if fam_default == name else ""
    bg = info.get("bg_semantic") or info.get("bg_hex") or "foto"
    print(f"{name}{mark}")
    print(f"    {info['family']} · rol {info['role_in_deck']} · sistema "
          f"{_SYSTEM_LABEL.get(info['system'], info['system'])} · maqueta "
          f"{info['composition_id']}")
    print(f"    fondo {info.get('background_treatment')} ({bg})"
          + ("  ⚠️ NECESITA scrim/zona de contraste para el texto" if info.get("needs_scrim") else "")
          + f" · {_zones_summary(name)}")
    # Caps deliberados: `describe()` es una ficha de 6-10 líneas para decidir rápido, no el texto
    # íntegro del juicio de marca (que puede pasar de 600 caracteres). Si necesitas el resto,
    # `fill_spec()` te da las zonas y el propio `use()` no te va a dejar equivocarte de nombre.
    for label, key, cap in (("SÍ", "use_when", 300), ("NO", "use_when_not", 200)):
        lines = _wrap(info.get(key), max_chars=cap)
        if lines:
            print(f"    cuándo {label}: {lines[0].strip()}")
            for extra in lines[1:]:
                print(f"      {extra.strip()}")
    sib = info.get("siblings") or []
    twin = _cross_system_twin(name)
    print(f"    hermanos (misma maqueta, otro color): "
          + (" · ".join(sib) if sib else "—")
          + (f" · equivalente en el otro sistema: {twin}" if twin else ""))
    if not _has_page_header(info):
        print("    ⚠️ sin zona de título: set_page_header() LANZA aquí — usa set_text().")
    print(f"    zonas exactas: fill_spec(\"{name}\")  (use() ya las imprime al clonar)")


# ---------------------------------------------------------------------------
# §FILL-SPEC — la tabla de relleno, y nada más
# ---------------------------------------------------------------------------
_FILL_SPEC_MAX_ZONES = 14


def _is_autoshape_image_zone(shp) -> bool:
    """¿Es `shp` una AUTO_SHAPE que el cliente maquetó como zona de imagen? (ver §G18).

    Conservador a propósito: exige que el NOMBRE lo declare (`imagen_2`, `foto`…) y que la
    propia forma no lleve texto. Aceptar cualquier AUTO_SHAPE grande sin relleno de imagen
    convertiría en hueco de foto cualquier rectángulo decorativo de las infografías."""
    if shp.shape_type != MSO_SHAPE_TYPE.AUTO_SHAPE:
        return False
    if not _IMAGE_ZONE_NAME_RE.match(shp.name or ""):
        return False
    if getattr(shp, "has_text_frame", False) and shp.text_frame.text.strip():
        return False
    return shp._element.find(qn("p:blipFill")) is None


_CARD_OVERLAP_MIN = 0.5


def _overlapping_text_zone(slide, shp) -> str | None:
    """Nombre de la zona de texto NO VACÍA que cubre >50% de `shp`, o None.

    Es lo que distingue una TARJETA de color (texto encima, ver `_COLOR_CARD_ZONES`) de un
    hueco de foto de verdad. Se mide sobre la diapositiva real y no sobre una tabla, para que
    valga también si el modelo ya vació o borró ese texto: entonces la forma sí puede ser un
    hueco de foto legítimo."""
    left, top = shp.left or 0, shp.top or 0
    right, bottom = left + (shp.width or 0), top + (shp.height or 0)
    for other in _iter_shapes_recursive(slide.shapes):
        if other is shp or not getattr(other, "has_text_frame", False):
            continue
        if not other.text_frame.text.strip():
            continue
        o_l, o_t = other.left or 0, other.top or 0
        o_r, o_b = o_l + (other.width or 0), o_t + (other.height or 0)
        area = (o_r - o_l) * (o_b - o_t)
        if not area:
            continue
        inter = (max(0, min(right, o_r) - max(left, o_l))
                 * max(0, min(bottom, o_b) - max(top, o_t)))
        if inter / area > _CARD_OVERLAP_MIN:
            return other.name
    return None


#: Tolerancia de banda (cm) para agrupar zonas en la misma "fila" al ordenar por lectura.
_READING_BAND_CM = 1.5


def _reading_key(x_cm: float | None, y_cm: float | None) -> tuple:
    """Clave de ORDEN DE LECTURA (arriba→abajo, izquierda→derecha) de una zona.

    Importa más de lo que parece. El orden en que la plantilla guarda los shapes NO es el
    orden visual: en `AGENDA_5COL_OSCURO` la primera pareja `13 CuadroTexto`/`__2` del árbol
    es la SEGUNDA columna en pantalla, así que un fill-spec en orden de shape hace que el
    modelo escriba el bloque 1 en la columna 2 — un error silencioso, porque la diapositiva
    sale llena y bien maquetada, solo con los bloques permutados. Encontrado por render, mismo
    fallo que `repsol-pptx` documenta en su G9. Con esta clave, el orden impreso ES el orden en
    que se lee la diapositiva."""
    if y_cm is None or x_cm is None:
        return (1, 0.0, 0.0)
    return (0, round(y_cm / _READING_BAND_CM), x_cm)


def _zone_rows(name: str, slide=None) -> tuple[list[tuple[str, str, str]], dict]:
    """`([(shape_name, rol, tipo)], header)` de un arquetipo, EN ORDEN DE LECTURA.

    Si se pasa `slide` (la copia recién clonada), las filas se calculan recorriendo LA
    DIAPOSITIVA REAL y cruzándola con el catálogo por `shape_name`. Es lo que garantiza que
    los nombres impresos son los de esa diapositiva y no los de una parecida — y lo que hace
    aparecer las zonas que el catálogo no publica (las tarjetas de color, §G18)."""
    info = _slide_info(name)
    by_name = {e["shape_name"]: e for e in info.get("elements", [])}
    rows: list[tuple[str, str, str]] = []
    order: dict[str, tuple] = {}

    def _row(shape_name: str, el: dict | None, forced_type: str | None = None) -> None:
        el = el or {}
        kind = forced_type or _TYPE_LABEL.get(el.get("kind") or "", None)
        if kind is None:
            return
        role = el.get("role") or "—"
        if kind == "txt":
            cap = el.get("max_chars_approx")
            detail = f"txt ≤{cap}" if cap else "txt"
            if el.get("example_text_kind") == "numerico":
                detail += " num"
        elif kind == "img":
            detail = "img"
            if el.get("seeded"):
                detail = "img SEMILLA→sustituir"
            elif el.get("has_image_fill") is False:
                detail = "img vacía"
        else:
            detail = kind
            if kind == "tabla" and el.get("rows"):
                detail = f"tabla {el['rows']}x{el['cols']}"
            if kind == "chart":
                if el.get("chart_editable") is False:
                    detail = "chart NO editable"
                elif el.get("n_series"):
                    # El TIPO de gráfica es parte del contrato de relleno: la del refresh es una
                    # TARTA, y una serie temporal en una tarta es un fallo de lectura que el
                    # catálogo ya sabía pero el fill-spec no decía (hallazgo de QA, §G26).
                    kind = _CHART_TYPE_LABEL.get(el.get("chart_type") or "", "")
                    detail = (f"chart {kind} {el['n_series']}s×{el.get('n_categories')}c"
                              if kind else
                              f"chart {el['n_series']}s×{el.get('n_categories')}c")
        rows.append((shape_name, role, detail))

    cards = _color_card_zones(name)
    if slide is not None:
        seen: set[str] = set()
        for shp in _iter_shapes_recursive(slide.shapes):
            if shp.name in seen:
                continue
            seen.add(shp.name)
            el = by_name.get(shp.name)
            is_card = False
            if el is None:
                if not _is_autoshape_image_zone(shp):
                    continue
                over = _overlapping_text_zone(slide, shp)
                if over:
                    rows.append((shp.name, "tarjeta", f"color · texto en '{over}'"))
                    is_card = True
                else:
                    _row(shp.name, {"role": "image", "has_image_fill": False}, "img")
            else:
                _row(shp.name, el)
            if el is not None or is_card or rows and rows[-1][0] == shp.name:
                order[shp.name] = _reading_key((shp.left or 0) / 914400 * 2.54,
                                               (shp.top or 0) / 914400 * 2.54)
    else:
        for el in info.get("elements", []):
            _row(el["shape_name"], el)
            order[el["shape_name"]] = _reading_key(el.get("x_cm"), el.get("y_cm"))
        for card, over in cards.items():
            rows.append((card, "tarjeta", f"color · texto en '{over}'"))
            # Sin diapositiva delante no hay geometría de la tarjeta en el catálogo (no la
            # publica): se ancla junto a su zona de texto, que sí está.
            twin = by_name.get(over) or {}
            order[card] = _reading_key(twin.get("x_cm"), twin.get("y_cm"))
    rows.sort(key=lambda r: (order.get(r[0], (1, 0.0, 0.0)), r[0]))
    return rows, (info.get("header") or {})


def fill_spec(slide_or_name, *, max_zones: int = _FILL_SPEC_MAX_ZONES) -> None:
    """Imprime SOLO la tabla de relleno de una diapositiva: `shape_name · rol · tipo/capacidad`.

    Acepta el nombre del arquetipo (antes de clonar) o la diapositiva devuelta por `use()`
    (mejor: entonces los nombres salen de la diapositiva real, incluidas las zonas de imagen
    que el catálogo no publica). `use()` ya llama a esto por ti; esta función es para volver a
    verlo, o para ver las zonas que el fill-spec de `use()` truncó."""
    if isinstance(slide_or_name, str):
        name, slide = resolve_name(slide_or_name), None
    else:
        slide = slide_or_name
        name = _origin_slide_name(slide)
        if name is None:
            raise RuntimeError("Esta diapositiva no viene de use(); pasa el NOMBRE del "
                               "arquetipo en su lugar.")
    _print_fill_spec(name, slide, prefix="[fill_spec]", max_zones=max_zones)


def _suffix_order_warnings(name: str) -> list[str]:
    """Familias de zonas `base_N` cuyo sufijo NO sigue el orden visual de izquierda a derecha.

    §G28 — hallazgo real de QA: en `DATOS_DASHBOARD_6CHART_CLASICO` los seis porcentajes
    grandes se llaman `subtitulo_2..subtitulo_7`, pero de izquierda a derecha son 4, 5, 6, 3, 2
    y 7: rellenarlos en orden de sufijo (lo natural) deja cada número sobre la barra y la
    etiqueta de OTRA columna, y la diapositiva sale llena y creíble, con los datos cambiados de
    sitio. El orden de lectura que imprime el fill-spec tampoco los ordena bien, porque están
    escalonados en vertical (cada número flota sobre su barra, a distinta altura) y caen en
    bandas distintas. Mismo tipo de defecto que `repsol-pptx` G9, pero dentro de una fila.

    Devuelve una línea por familia afectada, con el orden visual explícito."""
    # La familia es base + MISMO ROL: en el dashboard, `subtitulo_1` es el subtítulo de cabecera
    # y `subtitulo_2..7` los seis porcentajes; metidos en el mismo grupo, la cabecera se cuela
    # entre las columnas y desactiva la comprobación.
    groups: dict[tuple[str, str], list[tuple[str, float, float]]] = {}
    for el in _slide_info(name).get("elements", []):
        m = re.fullmatch(r"(.+?)_(\d{1,2})", el.get("shape_name") or "")
        if not m or el.get("x_cm") is None or el.get("y_cm") is None:
            continue
        groups.setdefault((m.group(1), str(el.get("role"))), []).append(
            (el["shape_name"], float(el["x_cm"]), float(el["y_cm"])))

    out = []
    for (base, _role), members in sorted(groups.items()):
        if len(members) < 3:
            continue
        # Solo una FILA horizontal de zonas DISTINTAS en x. Si dos comparten columna (una
        # rejilla de dos filas, o el número y el cuerpo de una misma columna de agenda), el
        # sufijo por filas es correcto y avisar sería un falso positivo: en
        # `GRID_MOSAICO_12_CLASICO` imagen_1..6 es la fila de arriba e imagen_7..12 la de abajo.
        xs = sorted(m[1] for m in members)
        if xs[-1] - xs[0] < 5.0:
            continue
        if any(b - a < 1.0 for a, b in zip(xs, xs[1:])):
            continue
        by_suffix = [m[0] for m in sorted(
            members, key=lambda m: int(re.fullmatch(r".+?_(\d{1,2})", m[0]).group(1)))]
        by_x = [m[0] for m in sorted(members, key=lambda m: m[1])]
        if by_suffix == by_x:
            continue
        out.append(f"⚠️ '{base}_N': el sufijo NO es el orden visual. De IZQUIERDA a DERECHA: "
                   + " → ".join(by_x) + " (§G28)")
    return out


def _covered_zone_warnings(name: str) -> list[str]:
    """Zonas del MISMO rol en las que una contiene a otra: la de fuera queda tapada.

    §G29 — hallazgo real de QA: `INFOGRAFIA_GAUGES` publica SIETE zonas `gauge_percent` para
    cinco indicadores. `Oval 9__4` y `Oval 9__5` (4,1 cm) son los ANILLOS de los dos primeros
    gauges y contienen a `Oval 11` y `Oval 9__6` (2,78 cm), que son los círculos del número.
    Escribir en el anillo no lanza y no se ve: el número desaparece detrás del círculo interior
    y los cinco valores quedan corridos una posición sin ningún aviso."""
    # Solo zonas de TEXTO: un número grande encima de su gráfica (el dashboard del clásico)
    # está así a propósito y no es un texto tapado.
    zones = [e for e in _slide_info(name).get("elements", [])
             if e.get("kind") == "text"
             and all(e.get(k) is not None for k in ("x_cm", "y_cm", "w_cm", "h_cm"))]
    out = []
    for outer in zones:
        for inner in zones:
            if inner is outer or inner.get("role") != outer.get("role"):
                continue
            if (float(inner["x_cm"]) > float(outer["x_cm"])
                    and float(inner["y_cm"]) > float(outer["y_cm"])
                    and float(inner["x_cm"]) + float(inner["w_cm"])
                    < float(outer["x_cm"]) + float(outer["w_cm"])
                    and float(inner["y_cm"]) + float(inner["h_cm"])
                    < float(outer["y_cm"]) + float(outer["h_cm"])):
                out.append(
                    f"⚠️ '{outer['shape_name']}' CONTIENE a '{inner['shape_name']}' (mismo rol): "
                    f"lo que escribas en la de fuera queda TAPADO. Escribe en "
                    f"'{inner['shape_name']}' (§G29)")
                break
    return out


def _print_fill_spec(name: str, slide, *, prefix: str, max_zones: int) -> None:
    info = _slide_info(name)
    rows, header = _zone_rows(name, slide)
    bg = info.get("bg_semantic") or ("foto" if info.get("has_background_image") else
                                     info.get("bg_hex") or "—")
    head = (f"{prefix} {name} · {info['family']}/{info['role_in_deck']} · "
            f"{_SYSTEM_LABEL.get(info['system'], info['system'])} · fondo {bg.lower()} · "
            f"{len(rows)} zonas")
    if info.get("needs_scrim"):
        head += " · ⚠️scrim"
    blocks = _blocks_of(info)
    if blocks:
        head += f" · {blocks} bloques/{(info.get('n_items') or {}).get('eje')}"
    print(head)
    if not rows:
        print("  (sin zonas rellenables: se clona tal cual)")
        return
    shown = rows[:max_zones]
    width = min(34, max(len(r[0]) for r in shown))
    for shape_name, role, detail in shown:
        print(f"  {shape_name:<{width}}  {role:<14} {detail}")
    if len(rows) > len(shown):
        print(f"  … +{len(rows) - len(shown)} zonas → fill_spec(s)")
    for warning in _suffix_order_warnings(name) + _covered_zone_warnings(name):
        print(f"  {warning}")
    if header.get("title"):
        bits = [f'set_page_header(s, "…")→{header["title"]}']
        if header.get("subtitle"):
            bits.append(f'subtitle=→{header["subtitle"]}')
        if header.get("page_number"):
            bits.append("number= disponible")
        print("  " + " · ".join(bits))
    else:
        print("  sin zona de título: NO llames a set_page_header() aquí")


# ---------------------------------------------------------------------------
# §LOCALIZACIÓN DE LA PLANTILLA
# ---------------------------------------------------------------------------
# La plantilla NO va bundleada en el .zip (excluida vía `.skillignore`): llega inyectada por
# `container_upload`/`templateFileId`, confirmado que el backend materializa el fichero en el
# sandbox. Este discovery la busca por nombre + Nº DE SLIDES.
#
# ⚠️ `_MIN_SLIDES` subió de 20 a 100 en la v4 y NO es cosmético: durante el rollout pueden
# convivir en el mismo sandbox la plantilla de la v3 (54 diapositivas) y la de la v4 (156).
# Con el umbral viejo, la primera que apareciera por orden de filesystem ganaba, y `new_deck()`
# fallaba con un error de desincronización en vez de coger la correcta. Además, entre los
# candidatos que casan por NOMBRE se prefiere el que tenga exactamente `len(slide_names())`
# diapositivas; solo si ninguno lo cumple se cae al de más diapositivas.
_NAME_HINTS = ("movistar", "plantilla", "template")
_MIN_SLIDES = 100
_PRUNE_DIRS = {"proc", "sys", "dev", "run", "old_root", "__pycache__", ".git", "node_modules"}
_OUTPUT_HINTS = ("/files/output", "/output", "/outputs")


def _slide_count(path: str) -> int:
    try:
        return len(Presentation(path).slides)
    except Exception:
        return -1


def _search_roots() -> list[str]:
    roots: list[str] = []
    for ev in ("INPUT_DIR", "ANTHROPIC_INPUT_DIR"):
        v = os.environ.get(ev)
        if v:
            roots.append(v)
    roots += ["/files/input", "/files", "/mnt/user-data/uploads", "/mnt", os.getcwd(),
              "/tmp", "/skills"]
    seen, out = set(), []
    for r in roots:
        if r and r not in seen and os.path.isdir(r):
            seen.add(r)
            out.append(r)
    return out


def _walk_pptx(root: str, cap: int = 80000) -> list[str]:
    out, n = [], 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _PRUNE_DIRS]
        rp = os.path.realpath(dirpath).replace("\\", "/")
        if any(h in rp for h in _OUTPUT_HINTS):
            continue
        for fn in filenames:
            n += 1
            if fn.lower().endswith(".pptx"):
                out.append(os.path.join(dirpath, fn))
        if n > cap:
            break
    return out


def _candidate_pptx() -> list[str]:
    seen: set[str] = set()
    out: list[str] = []

    def _collect(root: str) -> None:
        for p in _walk_pptx(root):
            rp = os.path.realpath(p)
            if rp in seen or not os.path.isfile(rp):
                continue
            seen.add(rp)
            out.append(rp)

    for root in _search_roots():
        _collect(root)
    if not out:
        _collect("/")
    return out


def _discover_template() -> str | None:
    cands = _candidate_pptx()
    if not cands:
        return None
    expected = len(slide_names())
    named = [p for p in cands if any(h in os.path.basename(p).lower() for h in _NAME_HINTS)]
    rest = [p for p in cands if p not in named]
    named_ok: list[tuple[int, int, str]] = []
    best: tuple[int, int, str] | None = None
    for p in named + rest:
        n = _slide_count(p)
        if n < _MIN_SLIDES:
            continue
        size = os.path.getsize(p)
        if p in named:
            if n == expected:
                return p                      # coincidencia exacta: no hay nada mejor
            named_ok.append((n, size, p))
            continue
        if best is None or (n, size) > (best[0], best[1]):
            best = (n, size, p)
    if named_ok:
        named_ok.sort(key=lambda t: (abs(t[0] - expected), -t[1]))
        return named_ok[0][2]
    return best[2] if best else None


def _template_path() -> str | None:
    p = _TPL_DIR / "movistar.pptx"
    if p.is_file():
        return str(p)
    import glob
    for base in ("/skills", "/mnt/skills", str(_SKILL_DIR), os.getcwd()):
        hits = glob.glob(f"{base}/**/movistar-pptx*/assets/template/movistar.pptx",
                         recursive=True)
        if hits:
            return sorted(hits)[0]
    return _discover_template()


# ---------------------------------------------------------------------------
# §CICLO DE VIDA DEL DECK
# ---------------------------------------------------------------------------
# id(Presentation) -> set(partname) de las 156 diapositivas canónicas ORIGINALES, capturado
# en new_deck(). save() las elimina; nunca se editan directamente.
_ORIGINALS_BY_DECK: dict = {}
# id(Presentation) -> {slide_name: partname de la diapositiva ORIGINAL en la plantilla}. Se
# localiza por POSICIÓN (el orden del catálogo == el orden del binario, invariante que
# garantiza `_contracts.validate_manifest()`: index == posición) y se guarda el `partname`,
# porque las partes se renumeraron en la fase final del merge y derivarlas por posición cada
# vez sería frágil (§G6).
_ORIGINAL_PARTNAME_BY_NAME_BY_DECK: dict = {}
# id(package) -> {partname de diapositiva CLONADA: slide_name canónico de origen}. La
# capacidad/rol de un shape_name se resuelve SIEMPRE dentro del alcance de su arquetipo de
# origen: un índice plano global colisionaría entre arquetipos que comparten nombre de shape.
_CLONE_ORIGIN_BY_DECK: dict = {}
# id(package) -> {(partname, shape_name)} de zonas atendidas explícitamente. Alimenta los
# gates de save(): imagen-semilla, anti-vacío y texto de ejemplo.
_TOUCHED: dict = {}
_IMAGES_SET: dict = {}
_CONFIRMED_EXAMPLE_TEXT: dict = {}
_CONFIRMED_EXAMPLE_IMAGE: dict = {}


def new_deck(template_path: str | None = None) -> Presentation:
    """Abre la plantilla oficial Movistar (156 arquetipos en 2 slideMaster + Movistar Sans /
    Medium / Extrabold realmente embebidas). NUNCA crea un deck en blanco. Si no encuentra la
    plantilla, lanza `RuntimeError`: DETENTE y repórtalo, no improvises con otra plantilla ni
    otra fuente."""
    path = (template_path if (template_path and Path(template_path).is_file())
            else _template_path())
    if not path:
        raise RuntimeError(
            "No se encontró la plantilla Movistar (assets/template/movistar.pptx, 156 "
            "arquetipos). DETENTE y repórtalo. NO construyas el deck desde cero ni con otra "
            "plantilla ni con Presentation() en blanco.")
    prs = Presentation(path)
    originals = list(prs.slides)
    names = slide_names()
    if len(originals) != len(names):
        raise RuntimeError(
            f"Plantilla desincronizada del catálogo: {len(originals)} diapositivas en el "
            f".pptx vs {len(names)} entradas en slides-catalog-movistar.json ({path}). "
            f"¿Se ha encontrado la plantilla de la v3 (54) o la vieja de 101 slideLayouts sin "
            f"diapositivas físicas, en vez de la de 156? Regenera con build_catalog.py si de "
            f"verdad has cambiado la plantilla.")
    _ORIGINALS_BY_DECK[id(prs)] = {slide.part.partname for slide in originals}
    _ORIGINAL_PARTNAME_BY_NAME_BY_DECK[id(prs)] = {
        name: slide.part.partname for name, slide in zip(names, originals)
    }
    return prs


def _find_canonical_slide(deck, slide_name: str):
    _slide_info(slide_name)  # valida y resuelve alias (lanza con sugerencias)
    canonical = resolve_name(slide_name)
    partname = _ORIGINAL_PARTNAME_BY_NAME_BY_DECK.get(id(deck), {}).get(canonical)
    if partname is None:
        raise RuntimeError("Este deck no viene de new_deck(); use() no puede operar sobre él.")
    for slide in deck.slides:
        if slide.part.partname == partname:
            return slide
    raise RuntimeError(
        f"No se encontró la diapositiva canónica '{canonical}' en la plantilla cargada "
        f"(¿plantilla y catálogo desincronizados? ejecuta build_catalog.py).")


_RID_TAGS = (qn("r:embed"), qn("r:link"), qn("r:id"))
_CLONE_SKIP_RELTYPES = ("/slideLayout", "/notesSlide")


def _clone_chart_part(chart_part):
    """Devuelve una COPIA independiente de un `chart` part y de todo lo que cuelga de él.

    Ver §G34. Copia el XML de la gráfica y, recursivamente, sus propias relaciones — el libro de
    Excel incrustado (`/package`), `colors*.xml`, `style*.xml`, `themeOverride*.xml` — para que
    `chart.replace_data()` en un clon no toque al otro. El partname nuevo se pide al paquete, que
    ya sabe asignar el siguiente índice libre.
    """
    package = chart_part.package
    # Se usa el classmethod `load(partname, content_type, blob, package)` en vez del constructor:
    # el orden de argumentos de `XmlPart.__init__` es (partname, content_type, package, element) y
    # equivocarlo no falla al construir, falla mucho más tarde con un AttributeError opaco
    # ('Package' object has no attribute 'chart'). Firma real de load(), comprobada con
    # inspect.signature: (partname, content_type, package, blob).
    new_part = type(chart_part).load(
        package.next_partname("/ppt/charts/chart%d.xml"),
        chart_part.content_type, package, chart_part.blob,
    )
    # Las relaciones de la gráfica: el workbook incrustado también se copia, porque
    # `replace_data()` lo reescribe.
    for sub in chart_part.rels.values():
        if sub.is_external:
            new_part.rels.get_or_add_ext_rel(sub.reltype, sub.target_ref)
            continue
        target = sub.target_part
        if sub.reltype.endswith("/package"):          # el .xlsx incrustado
            dup = type(target).load(
                package.next_partname("/ppt/embeddings/Microsoft_Excel_Sheet%d.xlsx"),
                target.content_type, package, target.blob,
            )
            new_part.relate_to(dup, sub.reltype)
        else:
            new_part.relate_to(target, sub.reltype)   # colors/style/theme: solo lectura
    return new_part


def _duplicate_slide(deck, source_slide):
    """Clona `source_slide` DENTRO del mismo deck: copia cada shape y re-liga sus relaciones
    (imágenes, gráficas) a los mismos media parts, remapeando los rId. NUNCA copia la
    relación `notesSlide` del original (§G5: PowerPoint pedía "reparar" el archivo por
    notesSlide compartidas entre clones; `verify_pptx.py` tiene el gate).

    TAMBIÉN copia `<p:bg>` si existe: varias diapositivas canónicas usan `<p:bg>` como su
    ÚNICO fondo de color plano, y `<p:bg>` no es una shape (vive como hermano de `<p:spTree>`
    dentro de `<p:cSld>`), así que `source_slide.shapes` nunca lo incluye — sin este paso cada
    clon perdía su color de fondo."""
    dest = deck.slides.add_slide(source_slide.slide_layout)
    for shp in list(dest.shapes):
        shp._element.getparent().remove(shp._element)

    src_bg = source_slide._element.find(qn("p:cSld")).find(qn("p:bg"))
    if src_bg is not None:
        dest_cSld = dest._element.find(qn("p:cSld"))
        dest_spTree = dest_cSld.find(qn("p:spTree"))
        dest_spTree.addprevious(copy.deepcopy(src_bg))

    rid_map = {}
    for rel in source_slide.part.rels.values():
        if any(rel.reltype.endswith(suffix) for suffix in _CLONE_SKIP_RELTYPES):
            continue
        if rel.is_external:
            new_rid = dest.part.rels.get_or_add_ext_rel(rel.reltype, rel.target_ref)
        elif rel.reltype.endswith("/chart"):
            # §G34 — una gráfica NO se puede compartir entre clones: lleva sus DATOS dentro.
            # Compartir el media part de una imagen es correcto (es un blob de solo lectura), pero
            # `set_chart_data()` REESCRIBE el `chart` part, así que dos `use()` del mismo arquetipo
            # de gráfica acababan apuntando al mismo `chartN.xml` y la segunda llamada destruía los
            # datos de la primera **en silencio**: el deck se entregaba con las dos diapositivas
            # mostrando los números de la última. Misma familia que G5 (notesSlide compartida).
            new_rid = dest.part.relate_to(_clone_chart_part(rel.target_part), rel.reltype)
        else:
            new_rid = dest.part.relate_to(rel.target_part, rel.reltype)
        rid_map[rel.rId] = new_rid

    for shp in source_slide.shapes:
        el = copy.deepcopy(shp._element)
        for node in el.iter():
            for tag in _RID_TAGS:
                old = node.get(tag)
                if old and old in rid_map:
                    node.set(tag, rid_map[old])
        dest.shapes._spTree.append(el)
    return dest


def use(deck, slide_name: str, *, quiet: bool = False):
    """Clona el arquetipo `slide_name` y lo añade al final del deck. Devuelve la copia, lista
    para `set_text()`/`set_image()`/`set_page_header()`.

    **Imprime su propio fill-spec** (`shape_name · rol · tipo/capacidad`): esos son los
    nombres de ESTA diapositiva, y son los únicos en los que debes fiarte. Un `shape_name` no
    es único entre arquetipos distintos, así que copiarlo de otro sitio (o de memoria) es el
    error clásico de esta plantilla. `quiet=True` lo silencia; no lo uses salvo que ya tengas
    los nombres delante."""
    if id(deck) not in _ORIGINALS_BY_DECK:
        raise RuntimeError("Este deck no viene de new_deck(); use() no puede operar sobre él.")
    canonical = resolve_name(slide_name)
    source = _find_canonical_slide(deck, canonical)
    dest = _duplicate_slide(deck, source)
    _CLONE_ORIGIN_BY_DECK.setdefault(id(dest.part.package), {})[str(dest.part.partname)] = canonical
    _USED_SYSTEMS[_slide_info(canonical)["system"]] += 1
    if not quiet:
        n = len(_CLONE_ORIGIN_BY_DECK[id(dest.part.package)])
        _print_fill_spec(canonical, dest, prefix=f"[use {n}]",
                         max_zones=_FILL_SPEC_MAX_ZONES)
    return dest


def _origin_slide_name(slide) -> str | None:
    """Arquetipo del que procede `slide`, si fue creada con `use()`. Se indexa por
    `id(slide.part.package)` en vez de recibir `deck` como parámetro, para que
    `set_text()`/`set_page_header()` mantengan la misma firma que en la v3."""
    return _CLONE_ORIGIN_BY_DECK.get(id(slide.part.package), {}).get(str(slide.part.partname))


def _iter_shapes_recursive(shapes):
    """Recorre `shapes` en profundidad, entrando en GRUPOS — necesario porque varios
    arquetipos (`AGENDA_5COL_*`, las rejillas de columnas del clásico) tienen sus zonas
    editables ANIDADAS dentro de `<p:grpSp>`: el build desambiguó los nombres duplicados pero
    no aplanó los grupos (§G4)."""
    for shp in shapes:
        yield shp
        if shp.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from _iter_shapes_recursive(shp.shapes)


def _find_shape(slide, shape_name: str):
    for shp in _iter_shapes_recursive(slide.shapes):
        if shp.name == shape_name:
            return shp
    available = [s.name for s in _iter_shapes_recursive(slide.shapes)]
    close = difflib.get_close_matches(shape_name, available, n=5, cutoff=0.4)
    origin = _origin_slide_name(slide)
    raise ValueError(
        f"la zona {shape_name!r} no existe en esta diapositiva"
        + (f" ({origin})" if origin else "")
        + (f". ¿{' · '.join(close)}?" if close else "")
        + f" — llama a fill_spec(s) para ver las {len(available)} zonas reales; un shape_name "
          f"NO es único entre arquetipos distintos.")


def _touch(slide, shape_name: str, registry: dict = None) -> None:
    reg = _TOUCHED if registry is None else registry
    reg.setdefault(id(slide.part.package), set()).add((str(slide.part.partname), shape_name))


def _is_touched(slide, shape_name: str, registry: dict) -> bool:
    return (str(slide.part.partname), shape_name) in registry.get(
        id(slide.part.package), set())


# ---------------------------------------------------------------------------
# §CABECERA DE PÁGINA
# ---------------------------------------------------------------------------
def set_page_header(slide, title: str, *, subtitle: str | None = None,
                    number: str | None = None) -> None:
    """Rellena la cabecera de una diapositiva de CONTENIDO resolviendo el shape por ROL de
    catálogo (`title`/`subtitle`/`page_number`), nunca por nombre fijo (varía por arquetipo).

    Llámala UNA VEZ por cada diapositiva de contenido devuelta por `use()` (NO una sola vez al
    final del deck — ver el docstring del módulo, §G8). `subtitle`/`number` son opcionales;
    `number` casi nunca hace falta: es un campo dinámico de PowerPoint que se recalcula al
    abrir el fichero.

    **18 de los 156 arquetipos no tienen zona de título** y aquí se LANZA a propósito: elegir
    un cierre o un separador-de-una-palabra para una página con cabecera es un error de
    elección, no algo que degradar en silencio. El mensaje lista las zonas de texto que ese
    arquetipo SÍ tiene, y el fill-spec de `use()` ya lo avisa antes de llegar aquí."""
    origin = _origin_slide_name(slide)
    if origin is None:
        raise RuntimeError("Esta diapositiva no viene de use(); set_page_header() no puede "
                           "operar sobre ella.")
    info = _slide_info(origin)
    header = info.get("header") or {}
    title_shape = header.get("title")
    if title_shape is None:
        texts = [f"{e['shape_name']} ({e.get('role') or 'texto'}, ≤{e.get('max_chars_approx')})"
                 for e in info.get("elements", []) if e.get("kind") == "text"]
        raise RuntimeError(
            f"'{origin}' NO tiene zona de título: set_page_header() no aplica aquí.\n"
            + ("  Zonas de texto que sí tiene, rellénalas con set_text():\n"
               + "\n".join(f"    - {t}" for t in texts) if texts else
               "  No tiene ninguna zona de texto: se clona tal cual (es un cierre o un fondo).")
            + f"\n  Si querías una página de contenido con cabecera, usa "
              f"find_slides(family='{info['family']}', has_page_header=True).")
    set_text(slide, title_shape, title)
    if subtitle is not None:
        sub_shape = header.get("subtitle")
        if sub_shape is None:
            print(f"[deck-qa] '{origin}' no tiene zona 'subtitle' — se ignora subtitle=. "
                  f"Métela en el título o elige otro arquetipo.")
        else:
            set_text(slide, sub_shape, subtitle)
    if number is not None:
        num_shape = header.get("page_number")
        if num_shape is None:
            print(f"[deck-qa] '{origin}' no tiene zona 'page_number' — se ignora number=.")
            return
        shp = _find_shape(slide, num_shape)
        fld = None
        for p in shp.text_frame.paragraphs:
            for child in p._p:
                if child.tag == qn("a:fld"):
                    fld = child
                    break
            if fld is not None:
                break
        if fld is None:
            print(f"[deck-qa] '{num_shape}': no se encontró el campo de número de página — "
                  f"se ignora number=.")
            return
        t = fld.find(qn("a:t"))
        if t is None:
            t = parse_xml('<a:t xmlns:a="http://schemas.openxmlformats.org/drawingml/'
                          '2006/main"/>')
            fld.append(t)
        t.text = str(number)
        _touch(slide, num_shape)


# ---------------------------------------------------------------------------
# §RELLENO DE TEXTO
# ---------------------------------------------------------------------------
_QA_GATES_CACHE: dict | None = None


def _qa_gates() -> dict:
    global _QA_GATES_CACHE
    if _QA_GATES_CACHE is None:
        g = brand_config().get("qa_gates", {})
        _QA_GATES_CACHE = {
            "movistar_lowercase": re.compile(g.get("movistar_lowercase_pattern",
                                                   r"\bmovistar\b")),
            "em_dash": re.compile(g.get("em_dash_pattern", "—")),
            "max_dominant_slide_ratio": g.get("max_dominant_slide_ratio", 0.30),
            "max_dominant_composition_ratio": g.get("max_dominant_composition_ratio", 0.35),
            "max_divider_ratio": g.get("max_divider_ratio", 0.25),
            "min_master_share": g.get("min_master_share", 0.25),
            "min_filled_ratio": g.get("min_filled_ratio", 0.80),
            "seed_image_gate": str(g.get("seed_image_gate", "warn")).lower(),
        }
    return _QA_GATES_CACHE


def _element_for(origin: str | None, shape_name: str) -> dict:
    if not origin:
        return {}
    for el in _slide_info(origin).get("elements", []):
        if el["shape_name"] == shape_name:
            return el
    return {}


def _write_text_frame(tf, text: str) -> None:
    """Escribe conservando los párrafos/runs existentes siempre que sea posible (§G12: un
    `\\n` literal dentro de un `<a:t>` NO es un salto de línea en OOXML — si el shape ya trae
    tantos párrafos como líneas, se reparte una línea por párrafo EXISTENTE y así cada uno
    conserva su propio formato)."""
    lines = str(text).split("\n")
    paragraphs = list(tf.paragraphs)
    if len(lines) > 1 and len(paragraphs) >= len(lines):
        for i, line in enumerate(lines):
            p = paragraphs[i]
            if not p.runs:
                p.text = line
            else:
                p.runs[0].text = line
                for extra_r in list(p.runs[1:]):
                    extra_r._r.getparent().remove(extra_r._r)
        for extra_p in paragraphs[len(lines):]:
            extra_p._p.getparent().remove(extra_p._p)
        return

    p0 = tf.paragraphs[0]
    if not p0.runs:
        tf.text = str(text)
    else:
        p0.runs[0].text = str(text)
        for extra_p in list(tf.paragraphs[1:]):
            extra_p._p.getparent().remove(extra_p._p)
        for extra_r in list(p0.runs[1:]):
            extra_r._r.getparent().remove(extra_r._r)


def set_text(slide, shape_name: str, text: str) -> None:
    """Escribe `text` en `shape_name`, conservando fuente/tamaño/color del texto de ejemplo
    (edita el run existente, no crea uno nuevo — §G2: la mayoría de los runs de esta plantilla
    no traen `sz`/`solidFill` propios y heredan de layout/master, así que reescribirlos los
    rompería).

    Avisa (no bloquea) si el texto supera `max_chars_approx`, si parece un `repr` de lista de
    Python, o si detecta fallos de marca baratos de comprobar (titular acabado en punto,
    'movistar' en minúscula, raya larga). El criterio de marca en sí vive en
    `movistar-brand-guidelines`, no aquí."""
    shp = _find_shape(slide, shape_name)
    if not shp.has_text_frame:
        raise ValueError(f"la zona {shape_name!r} no admite texto (es "
                         f"{_TYPE_LABEL.get(_element_for(_origin_slide_name(slide), shape_name).get('kind') or '', 'decorativa')})")
    text = str(text)
    _write_text_frame(shp.text_frame, text)
    _touch(slide, shape_name)

    origin = _origin_slide_name(slide)
    el = _element_for(origin, shape_name)
    cap = el.get("max_chars_approx")
    if cap and len(text) > cap:
        src = el.get("capacity_source") or "medida"
        print(f"[deck-qa] '{shape_name}': {len(text)} caracteres supera la capacidad "
              f"orientativa ({cap}, {src}) de esta zona — revisa que no se recorte o encoja "
              f"demasiado.")
    if "['" in text or "', '" in text:
        print(f"[deck-qa] '{shape_name}': el texto parece un repr de lista de Python, no "
              f"texto real: {text[:60]!r}")

    gates = _qa_gates()
    stripped = text.strip()
    if el.get("role") == "title" and stripped.endswith(".") and not stripped.endswith("..."):
        print(f"[deck-qa] '{shape_name}': el titular acaba en punto — los titulares Movistar "
              f"van sin punto final.")
    if gates["movistar_lowercase"].search(text):
        print(f"[deck-qa] '{shape_name}': 'movistar' en minúscula — el nombre de marca se "
              f"escribe 'Movistar'.")
    if gates["em_dash"].search(text):
        print(f"[deck-qa] '{shape_name}': contiene raya larga (—) — revisa si la voz de marca "
              f"de este deck prefiere evitarla.")


def set_texts(slide, values: dict) -> None:
    """Rellena varias zonas de una diapositiva en una sola operación determinista. Es el
    atajo recomendado para rejillas de columnas, comparativas y timelines: mismos gates y
    mismo formato que `set_text()`, una sola llamada.

    Una zona con valor `None` se OMITE (no se escribe la cadena "None"): así se puede pasar el
    fill-spec completo de la diapositiva y dejar fuera las zonas que se rellenan aparte —
    típicamente las de imagen, con `set_image()`."""
    if not isinstance(values, dict) or not values:
        raise ValueError("values debe ser un dict no vacío {shape_name: texto}")
    for shape_name, value in values.items():
        if value is None:
            continue
        set_text(slide, shape_name, str(value))


# ---------------------------------------------------------------------------
# §IMÁGENES — set_image() auto-curativo (§G18)
# ---------------------------------------------------------------------------
_MAX_SANE_CROP = 0.3  # por lado; >0.3 = se pierde >60% de esa dimensión, aviso


def _center_crop_fractions(src_ar: float, dst_ar: float) -> tuple[float, float, float, float]:
    """Fracciones (left, right, top, bottom) para recortar una imagen de aspect ratio
    `src_ar` y que lo visible encaje EXACTO en un hueco de aspect ratio `dst_ar` sin
    deformarse — equivalente a CSS `object-fit: cover`, recorte centrado."""
    if not src_ar or not dst_ar:
        return (0.0, 0.0, 0.0, 0.0)
    ratio = src_ar / dst_ar
    if abs(ratio - 1) < 1e-6:
        return (0.0, 0.0, 0.0, 0.0)
    if ratio > 1:
        f = (1 - 1 / ratio) / 2
        return (f, f, 0.0, 0.0)
    g = (1 - ratio) / 2
    return (0.0, 0.0, g, g)


def _image_aspect(part) -> float | None:
    try:
        w, h = part.image.size
        return w / h if h else None
    except Exception:
        return None


def _warn_crop(shape_name: str, crops, new_ar, dst_ar) -> None:
    worst = max(crops)
    if worst > _MAX_SANE_CROP:
        print(f"[deck-qa] '{shape_name}': recorte del {worst:.0%} en un lado para encajar sin "
              f"deformar (imagen {new_ar:.2f} vs hueco {dst_ar:.2f}) — revisa que no corte el "
              f"sujeto principal (el recorte es centrado, sin detección de sujeto).")


def _blipfill_xml(rid: str, crops: tuple[float, float, float, float]) -> str:
    l, r, t, b = (max(0, min(99000, int(round(v * 100000)))) for v in crops)
    src_rect = (f'<a:srcRect l="{l}" r="{r}" t="{t}" b="{b}"/>'
                if any((l, r, t, b)) else '<a:srcRect/>')
    return (
        '<a:blipFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        f' rotWithShape="1"><a:blip r:embed="{rid}"/>{src_rect}'
        '<a:stretch><a:fillRect/></a:stretch></a:blipFill>')


#: Rellenos que un `blipFill` sustituye cuando se convierte una AUTO_SHAPE en hueco de foto.
_FILL_TAGS = ("a:noFill", "a:solidFill", "a:gradFill", "a:blipFill", "a:pattFill", "a:grpFill")
#: Hijos de `<p:spPr>` que van DESPUÉS del relleno en el esquema de DrawingML. El `blipFill`
#: se inserta antes del primero que exista; si no existe ninguno, al final. Insertarlo en el
#: orden equivocado hace que PowerPoint pida "reparar" el fichero.
_AFTER_FILL_TAGS = ("a:ln", "a:effectLst", "a:effectDag", "a:scene3d", "a:sp3d", "a:extLst")


def _inject_blipfill(shp, rid: str, crops) -> None:
    spPr = shp._element.find(qn("p:spPr"))
    if spPr is None:
        spPr = parse_xml('<p:spPr xmlns:p="http://schemas.openxmlformats.org/'
                         'presentationml/2006/main"/>')
        shp._element.find(qn("p:nvSpPr")).addnext(spPr)
    for tag in _FILL_TAGS:
        for el in spPr.findall(qn(tag)):
            spPr.remove(el)
    blip_fill = parse_xml(_blipfill_xml(rid, crops))
    anchor = None
    for tag in _AFTER_FILL_TAGS:
        found = spPr.find(qn(tag))
        if found is not None:
            anchor = found
            break
    if anchor is not None:
        anchor.addprevious(blip_fill)
    else:
        spPr.append(blip_fill)


_FLAT_BG_STEMS: set | None = None


def _is_flat_background(image_path: str) -> bool:
    """¿Es `image_path` uno de los 12 fondos de COLOR PLANO del banco (`categoria: fondo`)?

    `list_brand_images()` los devuelve mezclados con las 23 fotos reales, y son 12 de 35: coger
    uno por descuido para un hueco de contenido llena la zona con un rectángulo de color y el
    claim "es por todos." — sale un deck aparentemente correcto con una tarjeta publicitaria
    donde debía haber una foto. Encontrado por render en un deck de prueba de esta ronda."""
    global _FLAT_BG_STEMS
    if _FLAT_BG_STEMS is None:
        _FLAT_BG_STEMS = set()
        try:
            for rec in list_brand_images(with_meta=True):
                if rec.get("categoria") == "fondo":
                    _FLAT_BG_STEMS.add(str(rec.get("id") or "").lower())
                    _FLAT_BG_STEMS.add(Path(str(rec.get("source_file") or "")).stem.lower())
        except Exception:
            pass
    return Path(image_path).stem.lower() in _FLAT_BG_STEMS


def set_image(slide, shape_name: str, image_path: str) -> None:
    """Pone `image_path` en la zona de imagen `shape_name`, conservando su posición, tamaño y
    contorno, con RECORTE-PARA-RELLENAR centrado (crop-to-fill, tipo CSS `object-fit: cover`):
    si el aspect ratio no coincide, recorta el eje sobrante en vez de estirar. Avisa si el
    recorte necesario pasa del 30% de un lado.

    **Es auto-curativo** (§G18): en esta plantilla hay tres formas físicas distintas de "hueco
    de foto" y saber de antemano en cuál estás no es un dato estable ni siquiera entre
    hermanos de la misma composición, así que el motor absorbe la diferencia en vez de
    obligarte a preguntar:

      1. Hueco YA poblado (`<p:blipFill>` presente) -> sustituye el blob y recorta.
      2. Placeholder `pic` VACÍO (2 de ellos en `INTERIOR_TXT_2IMG`, defecto del original del
         cliente) -> inserta la foto (`insert_picture`), **restaura el `shape_name`** (la
         inserción sustituye el elemento y el proxy anterior queda inválido) y recorta igual.
      3. AUTO_SHAPE nombrada como zona de imagen y sin relleno de imagen -> le inyecta un
         `<a:blipFill>` con el mismo recorte, preservando geometría, redondeo y contorno.
         **Salvo si tiene una zona de texto encima**: entonces no es un hueco de foto, es una
         TARJETA de color (las 5 `imagen_N` de `INTERIOR_TXT_*_CAPTION_CLASICO`) y meterle una
         foto deja ese texto sin fondo de contraste. Ver `_COLOR_CARD_ZONES`.

    Si la zona no es ninguna de las tres, lanza `ValueError` diciendo qué es en realidad."""
    shp = _find_shape(slide, shape_name)
    if not os.path.isfile(image_path):
        print(f"[deck-qa] '{shape_name}': imagen no encontrada, se omite ({image_path})")
        return

    el0 = _element_for(_origin_slide_name(slide), shape_name)
    if _is_flat_background(image_path) and not el0.get("is_full_bleed"):
        print(f"[deck-qa] '{shape_name}': '{Path(image_path).name}' es uno de los 12 FONDOS de "
              f"color plano del banco (categoria 'fondo'), no una fotografía — en un hueco de "
              f"contenido sale como un rectángulo de color con el claim de marca. Filtra el "
              f"banco con list_brand_images(categoria='personas'|'hogar'|'urbano'|…) o "
              f"list_brand_images(with_meta=True) y descarta categoria='fondo'.")

    dst_ar = (shp.width / shp.height) if (shp.width and shp.height) else None
    blip_fill = shp._element.find(qn("p:blipFill"))

    # -- caso 1: hueco ya poblado (rama de siempre) --------------------------------
    if blip_fill is not None:
        blip = blip_fill.find(qn("a:blip"))
        part, rid = slide.part.get_or_add_image_part(image_path)
        blip.set(qn("r:embed"), rid)
        shp.crop_left = shp.crop_right = shp.crop_top = shp.crop_bottom = 0.0
        new_ar = _image_aspect(part)
        if new_ar and dst_ar:
            crops = _center_crop_fractions(new_ar, dst_ar)
            shp.crop_left, shp.crop_right, shp.crop_top, shp.crop_bottom = crops
            _warn_crop(shape_name, crops, new_ar, dst_ar)
        _touch(slide, shape_name)
        _touch(slide, shape_name, _IMAGES_SET)
        return

    # -- caso 2: placeholder `pic` VACÍO -------------------------------------------
    if hasattr(shp, "insert_picture"):
        pic = shp.insert_picture(image_path)
        pic.name = shape_name  # `insert_picture` sustituye el elemento: el nombre se recupera
        pic.crop_left = pic.crop_right = pic.crop_top = pic.crop_bottom = 0.0
        try:
            w, h = pic.image.size
            new_ar = w / h if h else None
        except Exception:
            new_ar = None
        dst_ar = (pic.width / pic.height) if (pic.width and pic.height) else dst_ar
        if new_ar and dst_ar:
            crops = _center_crop_fractions(new_ar, dst_ar)
            pic.crop_left, pic.crop_right, pic.crop_top, pic.crop_bottom = crops
            _warn_crop(shape_name, crops, new_ar, dst_ar)
        print(f"[mvst] '{shape_name}': placeholder de imagen VACÍO — foto insertada por "
              f"primera vez (§G18, defecto del original del cliente).")
        _touch(slide, shape_name)
        _touch(slide, shape_name, _IMAGES_SET)
        return

    # -- caso 3: AUTO_SHAPE que el cliente maquetó como hueco de foto --------------
    if _is_autoshape_image_zone(shp):
        over = _overlapping_text_zone(slide, shp)
        if over:
            raise ValueError(
                f"'{shape_name}' NO es un hueco de foto aunque se llame así: es una TARJETA de "
                f"color secundario claro con la zona de texto '{over}' ENCIMA, escrita en un "
                f"secundario oscuro. Ponerle una foto deja ese texto sin fondo de contraste — "
                f"el fallo que prohíbe brand/contrast-matrix.md (verificado por render). "
                f"El nombre 'imagen_N' es un artefacto del heurístico de la plantilla.\n"
                f"  · Si querías la tarjeta: no toques '{shape_name}', escribe el contenido en "
                f"'{over}' con set_text().\n"
                f"  · Si de verdad querías una foto a ese tamaño: usa otro arquetipo "
                f"(find_slides(family='INTERIOR', has_image=True)) — o, excepcionalmente, "
                f"remove_shape(s, '{over}') antes de este set_image().")
        part, rid = slide.part.get_or_add_image_part(image_path)
        new_ar = _image_aspect(part)
        crops = (_center_crop_fractions(new_ar, dst_ar) if (new_ar and dst_ar)
                 else (0.0, 0.0, 0.0, 0.0))
        _inject_blipfill(shp, rid, crops)
        if new_ar and dst_ar:
            _warn_crop(shape_name, crops, new_ar, dst_ar)
        print(f"[mvst] '{shape_name}': zona de imagen maquetada como forma de color plano — "
              f"convertida en hueco de foto real (§G18), geometría y contorno intactos.")
        _touch(slide, shape_name)
        _touch(slide, shape_name, _IMAGES_SET)
        return

    el = _element_for(_origin_slide_name(slide), shape_name)
    what = el.get("kind") or ("forma decorativa" if shp.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE
                              else str(shp.shape_type))
    raise ValueError(
        f"la zona {shape_name!r} no es un hueco de foto (es {what}). Llama a fill_spec(s) "
        f"para ver qué zonas admiten imagen en esta diapositiva; si este arquetipo no tiene "
        f"ninguna, usa find_slides(family=…, has_image=True).")


# ---------------------------------------------------------------------------
# §GRÁFICAS Y TABLAS
# ---------------------------------------------------------------------------
#: Títulos de gráfica de EJEMPLO que hay que retirar. El conjunto cerrado anterior se le
#: escapó "Título de la gráfica" (femenino), que es justo el que trae `DATOS_CHART_CLASICO` y
#: llegaba al deck entregado — visto en el render, §G27. Con un patrón deja de depender de que
#: alguien acierte el género y el artículo.
_DEFAULT_CHART_TITLES = {"chart title", "título del gráfico", "titulo del grafico"}
_DEFAULT_CHART_TITLE_RE = re.compile(
    r"^\s*(chart\s+title|t[íi]tulo\s+(de\s+la|del|de)\s+gr[áa]fic[ao])\s*$", re.I)


def _normalise_series(series):
    return list(series.items()) if isinstance(series, dict) else list(series)


def set_chart_data(slide, shape_name: str, categories, series) -> None:
    """Sustituye los datos de UNA gráfica nativa manteniendo su diseño Movistar.

    `series` acepta `{"Nombre": [1, 2]}` o `[("Nombre", [1, 2])]`. Todas las series deben
    tener un valor por categoría. Para varias gráficas de la misma diapositiva (el dashboard
    del clásico trae 6), usa `set_charts_data()`."""
    shp = _find_shape(slide, shape_name)
    if not getattr(shp, "has_chart", False):
        raise ValueError(f"la zona {shape_name!r} no es una gráfica")
    origin = _origin_slide_name(slide)
    el = _element_for(origin, shape_name)
    if el.get("chart_editable") is False:
        raise ValueError(
            f"'{shape_name}' de '{origin}' es una gráfica SIN workbook embebido: "
            f"replace_data() lanzaría. Elige otro arquetipo con "
            f"find_slides(has_chart=True), o inserta una gráfica nueva con la API nativa "
            f"(slide.shapes.add_chart) sobre content_rect(s).")
    labels = [str(value) for value in categories]
    if not labels:
        raise ValueError("categories no puede estar vacío")
    items = _normalise_series(series)
    if not items:
        raise ValueError("series no puede estar vacío")
    n_series = el.get("n_series")
    if n_series and len(items) > n_series:
        print(f"[deck-qa] '{shape_name}': {len(items)} series en una gráfica diseñada para "
              f"{n_series} — las {len(items) - n_series} extra saldrán con la paleta POR "
              f"DEFECTO de Office (azul/naranja/gris), no con la de Movistar. Es un fallo de "
              f"marca silencioso: agrupa los datos en {n_series} series o usa otro arquetipo.")
    # §G26: la gráfica de INTERIOR_CHART es una TARTA. Una tarta enseña la composición de un
    # total; con años por categoría dice «2024 es el 12 % de todos los años», que no significa
    # nada. El catálogo publica `chart_type` y el fill-spec ya lo imprime, pero el aviso aquí es
    # el que salva el deck cuando el modelo rellena de memoria.
    if (el.get("chart_type") in _PART_OF_WHOLE_CHARTS and len(labels) >= 3
            and sum(1 for lab in labels if re.fullmatch(r"(19|20)\d{2}", lab.strip()))
            >= len(labels) - 1):
        print(f"[deck-qa] '{shape_name}': es una gráfica de "
              f"{_CHART_TYPE_LABEL.get(el.get('chart_type'), 'tarta')} (parte de un total) y "
              f"las categorías son AÑOS: una evolución en el tiempo no se lee en una tarta. "
              f"Usa un arquetipo de columnas (find_slides(has_chart=True) → "
              f"INTERIOR_CHART_L23 / DATOS_CHART_CLASICO) o cambia el dato a una composición "
              f"del total (cuota por segmento, reparto por tecnología…).")

    chart_data = CategoryChartData()
    chart_data.categories = labels
    for name, values in items:
        numbers = list(values)
        if len(numbers) != len(labels):
            raise ValueError(f"serie {name!r}: {len(numbers)} valores para {len(labels)} "
                             f"categorías")
        chart_data.add_series(str(name), numbers)
    chart = shp.chart
    chart.replace_data(chart_data)
    # Hallazgo real de QA visual (2026-07-27): algunas gráficas de la plantilla traen un título
    # de ejemplo sin editar ("Chart title", el default de PowerPoint/python-pptx) que el
    # catálogo no rastrea como texto de ejemplo — el gate de save() nunca lo veía y llegaba tal
    # cual al deck (visto en INTERIOR_CHART_L23). Se retira aquí porque ningún arquetipo lo
    # pone a propósito; si algún día quieres un título real, añádelo tras llamar a esto.
    _title_now = chart.chart_title.text_frame.text if chart.has_title else ""
    if chart.has_title and (_title_now.strip().lower() in _DEFAULT_CHART_TITLES
                            or _DEFAULT_CHART_TITLE_RE.match(_title_now)):
        chart.has_title = False
        print(f"[deck-qa] '{shape_name}': título de gráfica de ejemplo sin editar "
              f"({_title_now.strip()!r}) retirado automáticamente (§G27).")
    _touch(slide, shape_name)


def set_charts_data(slide, charts: dict) -> None:
    """Rellena VARIAS gráficas de la misma diapositiva en una llamada:
    `{shape_name: (categorias, series)}`.

    Existe porque `DATOS_DASHBOARD_6CHART_CLASICO` trae 6 gráficas nativas y hacerlo con 6
    llamadas invita a olvidar una — y una gráfica del dashboard sin datos reales entrega los
    del ejemplo, que el gate de texto no puede ver."""
    if not isinstance(charts, dict) or not charts:
        raise ValueError("charts debe ser un dict no vacío {shape_name: (categorias, series)}")
    for shape_name, payload in charts.items():
        try:
            categories, series = payload
        except (TypeError, ValueError):
            raise ValueError(f"'{shape_name}': el valor debe ser la tupla "
                             f"(categorias, series), no {payload!r}")
        set_chart_data(slide, shape_name, categories, series)


#: Tinta legible sobre fondo claro / oscuro (Negro y Blanco Movistar).
_INK_DARK, _INK_LIGHT = "262423", "FFFAF5"


def _hex_luminance(hex_value: str) -> float:
    """Luminancia relativa WCAG de un hex de 6. Solo para decidir tinta clara vs. oscura."""
    def channel(c: float) -> float:
        c /= 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    h = hex_value.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def _theme_hex(slide, token: str) -> str | None:
    """Hex real de un `schemeClr` (`bg1`/`tx1`/`bg2`/`tx2`/`accentN`) en el master de `slide`.

    Resuelve las dos indirecciones de OOXML: el `p:clrMap` del slideMaster (bg1→lt1, tx1→dk1…)
    y el `a:clrScheme` del tema asociado a ESE master — la plantilla tiene dos masters con dos
    temas distintos, así que el del refresh no vale para el clásico."""
    try:
        master = slide.slide_layout.slide_master
        clr_map = master._element.find(qn("p:clrMap"))
        slot = token
        if clr_map is not None and token in clr_map.attrib:
            slot = clr_map.get(token)
        theme_part = next(
            (rel.target_part for rel in master.part.rels.values()
             if not rel.is_external and rel.reltype.endswith("/theme")), None)
        if theme_part is None:
            return None
        scheme = parse_xml(theme_part.blob).find(
            f"{qn('a:themeElements')}/{qn('a:clrScheme')}")
        if scheme is None:
            return None
        node = scheme.find(qn(f"a:{slot}"))
        if node is None:
            return None
        srgb = node.find(qn("a:srgbClr"))
        if srgb is not None:
            return srgb.get("val", "").upper() or None
        sys_clr = node.find(qn("a:sysClr"))
        if sys_clr is not None:
            return (sys_clr.get("lastClr") or "").upper() or None
    except Exception:  # nunca romper un save() por no poder resolver un color
        return None
    return None


def _apply_color_transforms(hex_value: str, node) -> str:
    """Aplica los modificadores de un `a:srgbClr`/`a:schemeClr`: `lumMod`/`lumOff` (en el canal
    L de HSL, como manda DrawingML) y `tint`/`shade`.

    Sin esto, el gris claro de las tablas de esta plantilla —`schemeClr tx1` con
    `lumMod 25% + lumOff 75%`— se lee como Negro Movistar y cualquier decisión de contraste
    sale al revés (bug real de la primera versión de este gate)."""
    import colorsys
    h = hex_value.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    def pct(tag):
        el = node.find(qn(f"a:{tag}"))
        if el is None or not el.get("val"):
            return None
        return int(el.get("val")) / 100000.0
    lum_mod, lum_off, tint, shade = pct("lumMod"), pct("lumOff"), pct("tint"), pct("shade")
    if lum_mod is not None or lum_off is not None:
        hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
        if lum_mod is not None:
            ll *= lum_mod
        if lum_off is not None:
            ll += lum_off
        r, g, b = colorsys.hls_to_rgb(hh, min(max(ll, 0.0), 1.0), ss)
    if tint is not None:
        r, g, b = (c * tint + (1.0 - tint) for c in (r, g, b))
    if shade is not None:
        r, g, b = (c * shade for c in (r, g, b))
    return "".join(f"{int(round(min(max(c, 0.0), 1.0) * 255)):02X}" for c in (r, g, b))


def _resolve_color_el(slide, parent) -> str | None:
    """Hex de la primera especificación de color bajo `parent` (`solidFill`, `tcTxStyle`…).
    Devuelve `None` si no la entiende — un color que no se sabe resolver NO se adivina."""
    if parent is None:
        return None
    srgb = parent.find(qn("a:srgbClr"))
    if srgb is not None and srgb.get("val"):
        return _apply_color_transforms(srgb.get("val").upper(), srgb)
    scheme = parent.find(qn("a:schemeClr"))
    if scheme is not None:
        base = _theme_hex(slide, scheme.get("val", ""))
        return _apply_color_transforms(base, scheme) if base else None
    sys_clr = parent.find(qn("a:sysClr"))
    if sys_clr is not None and sys_clr.get("lastClr"):
        return _apply_color_transforms(sys_clr.get("lastClr").upper(), sys_clr)
    return None


def _cell_fill_hex(slide, cell, fallback_hex: str | None) -> str | None:
    """Fondo EFECTIVO de una celda: su propio relleno sólido si lo tiene; si no, `fallback_hex`
    (el de su banda de estilo o el de la diapositiva). `None` = no se pudo resolver."""
    tc_pr = cell._tc.find(qn("a:tcPr"))
    if tc_pr is not None:
        solid = tc_pr.find(qn("a:solidFill"))
        if solid is not None:
            return _resolve_color_el(slide, solid)
    return fallback_hex.lstrip("#").upper() if fallback_hex else None


#: Precedencia de bandas de un estilo de tabla, de la más específica a la más general.
_TABLE_BANDS = ("firstRow", "lastRow", "firstCol", "lastCol", "wholeTbl")


def _table_style_bands(slide, tbl) -> dict:
    """`{banda: {"ink": token|None, "fill": token|None}}` del estilo de tabla de `tbl`.

    Los tokens son `schemeClr val` tal cual vienen en `ppt/tableStyles.xml`; se resuelven con
    `_theme_hex()` porque cada master tiene su propio tema."""
    out: dict[str, dict] = {}
    try:
        style_id_el = tbl.find(f"{qn('a:tblPr')}/{qn('a:tableStyleId')}")
        if style_id_el is None or not (style_id_el.text or "").strip():
            return out
        style_id = style_id_el.text.strip()
        part = next((p for p in slide.part.package.iter_parts()
                     if str(p.partname).endswith("tableStyles.xml")), None)
        if part is None:
            return out
        root = parse_xml(part.blob)
        style = next((s for s in root.findall(qn("a:tblStyle"))
                      if s.get("styleId") == style_id), None)
        if style is None:
            return out
        for band in _TABLE_BANDS:
            node = style.find(qn(f"a:{band}"))
            if node is None:
                continue
            out[band] = {
                "ink": node.find(qn("a:tcTxStyle")),
                "fill": node.find(f"{qn('a:tcStyle')}/{qn('a:fill')}/{qn('a:solidFill')}"),
            }
    except Exception:  # un estilo de tabla ilegible nunca debe romper un save()
        return {}
    return out


def _bands_for_cell(tbl, row_idx: int, col_idx: int, n_rows: int, n_cols: int) -> list[str]:
    """Bandas del estilo que aplican a una celda, en orden de precedencia."""
    tbl_pr = tbl.find(qn("a:tblPr"))
    flag = (lambda name: tbl_pr is not None and tbl_pr.get(name) == "1")
    bands = []
    if flag("firstRow") and row_idx == 0:
        bands.append("firstRow")
    if flag("lastRow") and row_idx == n_rows - 1:
        bands.append("lastRow")
    if flag("firstCol") and col_idx == 0:
        bands.append("firstCol")
    if flag("lastCol") and col_idx == n_cols - 1:
        bands.append("lastCol")
    bands.append("wholeTbl")
    return bands


def _contrast_ratio(hex_a: str, hex_b: str) -> float:
    la, lb = _hex_luminance(hex_a), _hex_luminance(hex_b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _fix_illegible_cell_text(slide, tbl, table, row_idx, col_idx, bg_hex) -> str | None:
    """Si el texto de una celda va a heredar un color ILEGIBLE, le fija tinta por contraste.

    §G25 — hallazgo real de QA: `Tabla 7` de `INTERIOR_TABLA` (y la `tabla` de
    `DATOS_TABLA_CLASICO`) traen la celda superior izquierda con `<a:noFill/>` y sin ningún
    `rPr`, porque en el diseño del cliente esa esquina va VACÍA. Al escribir ahí —y el propio
    `capability-recipe.md` manda rellenar las 8x7 celdas— el run nuevo no lleva color y hereda
    el de la banda `firstRow` del estilo de tabla, que es `schemeClr lt1` = Blanco Movistar:
    blanco sobre crema, invisible. Verificado en `ppt/tableStyles.xml` (`Medium Style 2 –
    Accent 1`), no solo en el render.

    Solo interviene cuando el contraste heredado es < 2:1, y **solo cambia el color**: tamaño y
    tipografía siguen heredándose del estilo de tabla, como los diseñó el cliente. Devuelve una
    etiqueta para el aviso `[deck-qa]`, o `None` si no había nada que arreglar."""
    cell = table.cell(row_idx, col_idx)
    runs = [run for para in cell.text_frame.paragraphs for para_runs in [para.runs]
            for run in para_runs]
    if not runs:
        return None
    # Un run con color propio ya sabe de qué color va: no se toca.
    if any((run._r.find(qn("a:rPr")) is not None
            and run._r.find(qn("a:rPr")).find(qn("a:solidFill")) is not None)
           for run in runs):
        return None

    n_rows, n_cols = len(table.rows), len(table.columns)
    bands = _table_style_bands(slide, tbl)
    applicable = _bands_for_cell(tbl, row_idx, col_idx, n_rows, n_cols)
    inherited_ink = next(
        (hexv for b in applicable if b in bands
         for hexv in [_resolve_color_el(slide, bands[b]["ink"])] if hexv), None)

    tc_pr = cell._tc.find(qn("a:tcPr"))
    if tc_pr is not None and tc_pr.find(qn("a:noFill")) is not None:
        # `noFill` explícito gana a la banda: la celda deja ver el fondo de la diapositiva.
        effective_bg = (bg_hex or "").lstrip("#").upper() or None
    else:
        band_fill = next(
            (hexv for b in applicable if b in bands
             for hexv in [_resolve_color_el(slide, bands[b]["fill"])] if hexv), None)
        effective_bg = _cell_fill_hex(slide, cell, band_fill or bg_hex)

    if not inherited_ink or not effective_bg:
        return None
    if _contrast_ratio(inherited_ink, effective_bg) >= 2.0:
        return None

    ink = _INK_DARK if _hex_luminance(effective_bg) > 0.5 else _INK_LIGHT
    for run in runs:
        r_el = run._r
        r_pr = r_el.find(qn("a:rPr"))
        if r_pr is None:
            r_pr = parse_xml(
                '<a:rPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
            r_el.insert(0, r_pr)
        r_pr.insert(0, parse_xml(
            '<a:solidFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            f'<a:srgbClr val="{ink}"/></a:solidFill>'))
    return (f"({row_idx},{col_idx}) heredaba #{inherited_ink} sobre #{effective_bg} "
            f"({_contrast_ratio(inherited_ink, effective_bg):.2f}:1) → #{ink}")


def set_table_data(slide, shape_name: str, rows) -> None:
    """Rellena una tabla nativa existente y limpia las celdas de ejemplo sobrantes.

    No crea ni redimensiona tablas: así preserva geometría, bordes, rellenos y tipografía de
    la diapositiva canónica. Los datos deben caber en sus filas/columnas. Si sobran filas o
    columnas, avisa (§G16: quedan en blanco con la banda de color de la plantilla, visible y
    embarazoso en un deck real). El catálogo publica `rows`/`cols` de cada tabla y el
    fill-spec de `use()` los imprime, así que puedes generar el número exacto de celdas."""
    shp = _find_shape(slide, shape_name)
    if not getattr(shp, "has_table", False):
        raise ValueError(f"la zona {shape_name!r} no es una tabla")
    matrix = [list(row) for row in rows]
    if not matrix or not any(matrix):
        raise ValueError("rows debe contener al menos una celda")
    width = max(len(row) for row in matrix)
    table = shp.table
    n_rows, n_cols = len(table.rows), len(table.columns)
    if len(matrix) > n_rows or width > n_cols:
        raise ValueError(f"los datos {len(matrix)}x{width} no caben en la tabla "
                         f"{n_rows}x{n_cols}")
    if len(matrix) < n_rows or width < n_cols:
        print(f"[deck-qa] '{shape_name}': datos {len(matrix)}x{width} en una tabla de "
              f"{n_rows}x{n_cols} — las {n_rows - len(matrix)} fila(s)/{n_cols - width} "
              f"columna(s) sobrantes quedarán en blanco con la banda de color de la plantilla "
              f"(visible en el render, no se redimensiona la tabla). Rellena EXACTAMENTE "
              f"{n_rows}x{n_cols} celdas.")
    origin = _origin_slide_name(slide)
    bg_hex = (_slide_info(origin) or {}).get("bg_hex") if origin else None
    fixed: list[str] = []
    for row_idx in range(len(table.rows)):
        for col_idx in range(len(table.columns)):
            value = matrix[row_idx][col_idx] if (
                row_idx < len(matrix) and col_idx < len(matrix[row_idx])
            ) else ""
            _write_text_frame(table.cell(row_idx, col_idx).text_frame, str(value))
            if str(value).strip():
                detail = _fix_illegible_cell_text(
                    slide, shp.table._tbl, table, row_idx, col_idx, bg_hex)
                if detail:
                    fixed.append(detail)
    if fixed:
        print(f"[deck-qa] '{shape_name}': {len(fixed)} celda(s) habrían quedado INVISIBLES al "
              f"heredar la tinta del estilo de tabla (celdas que la plantilla dejaba vacías, "
              f"§G25); se les ha fijado tinta por contraste, sin tocar tamaño ni tipografía: "
              f"{', '.join(fixed)}.")
    _touch(slide, shape_name)


_HEADER_ROLES = ("title", "subtitle", "kicker", "chapter_name", "chapter_subtitle")


def content_rect(slide) -> tuple[int, int, int, int]:
    """Rectángulo libre `(x, y, w, h)` en EMU bajo la cabecera de `slide`, para insertar una
    tabla o una gráfica con la API NATIVA de python-pptx
    (`slide.shapes.add_table()`/`add_chart()`).

    ⚠️ **Es un último recurso, no parte del flujo normal.** Una gráfica creada con
    `add_chart()` sobre un rectángulo vacío sale con la paleta POR DEFECTO de Office
    (azul/naranja/gris), no con la de Movistar: es un fallo de marca silencioso. Antes de
    llegar aquí, busca un arquetipo que YA traiga la gráfica o la tabla compuesta
    (`find_slides(has_chart=True)` / `has_table=True`) y usa
    `set_chart_data()`/`set_table_data()`. Portado de `repsol-pptx`, donde sí es el camino
    normal porque ningún arquetipo suyo trae gráfica precargada.

    Calcula el borde inferior de las zonas de cabecera presentes y devuelve el área libre por
    debajo, recortando el ancho por el lado donde haya una zona de texto lateral YA poblada
    (los callouts que varios arquetipos traen junto al hueco de datos)."""
    prs = slide.part.package.presentation_part.presentation
    sw, sh = prs.slide_width / 914400 * 2.54, prs.slide_height / 914400 * 2.54
    origin = _origin_slide_name(slide)
    header_names = set()
    if origin:
        for el in _slide_info(origin).get("elements", []):
            if el.get("role") in _HEADER_ROLES:
                header_names.add(el["shape_name"])
    header_bottoms, lefts = [], []
    for shp in slide.shapes:
        base = re.sub(r"_\d+$", "", shp.name)
        if shp.name in header_names or base in ("titulo", "subtitulo", "antetitulo", "frase"):
            header_bottoms.append((shp.top or 0) / 914400 * 2.54
                                  + (shp.height or 0) / 914400 * 2.54)
            lefts.append((shp.left or 0) / 914400 * 2.54)
    header_bottom = max(header_bottoms) if header_bottoms else 3.3
    left = min(lefts) if lefts else 1.15
    top = header_bottom + 0.6
    width = max(6.0, sw - 2 * left)
    height = max(3.0, sh - top - 1.3)
    bottom = top + height

    for shp in slide.shapes:
        base = re.sub(r"_\d+$", "", shp.name)
        if shp.name in header_names or base in ("titulo", "subtitulo", "antetitulo", "frase"):
            continue
        if not getattr(shp, "has_text_frame", False) or not shp.text_frame.text.strip():
            continue
        shp_top = (shp.top or 0) / 914400 * 2.54
        shp_bottom = shp_top + (shp.height or 0) / 914400 * 2.54
        if shp_bottom <= top or shp_top >= bottom:
            continue  # no comparte banda vertical con el área de contenido
        shp_left = (shp.left or 0) / 914400 * 2.54
        shp_right = shp_left + (shp.width or 0) / 914400 * 2.54
        center = sw / 2
        if shp_left >= center:
            width = min(width, max(6.0, shp_left - 0.4 - left))
        elif shp_right <= center:
            new_left = shp_right + 0.4
            width = max(6.0, width - (new_left - left))
            left = new_left
    return Cm(left), Cm(top), Cm(width), Cm(height)


# ---------------------------------------------------------------------------
# §ESCAPES LEGÍTIMOS
# ---------------------------------------------------------------------------
def remove_shape(slide, shape_name: str) -> None:
    """Escapatoria para casos genuinamente excepcionales en los que una zona de una
    diapositiva real no aplica. ÚSALA POCO: el catálogo describe diapositivas reales ya
    diseñadas para llenarse por completo — si una zona no encaja, casi siempre es señal de que
    toca otro arquetipo (`find_slides(...)`), no de vaciar esta."""
    shp = _find_shape(slide, shape_name)
    print(f"[deck-qa] '{shape_name}': eliminado explícitamente con remove_shape() — confirma "
          f"que de verdad no había un arquetipo mejor para este contenido.")
    shp._element.getparent().remove(shp._element)


def confirm_example_text(slide, shape_name: str) -> None:
    """Escapatoria legítima (§G13), hermana de `remove_shape()`: confirma que el texto ACTUAL
    de `shape_name` es CONTENIDO REAL correcto aunque coincida literalmente con el texto de
    ejemplo de la plantilla, para que `save()` no lo trate como "sin reemplazar".

    Caso de uso real: el "02" de un `SEPARADOR_NUMERO_02_CORAL` o la numeración "1./2./3./4./5."
    de `INDICE_SIMPLE` son, por diseño de la plantilla, exactamente el valor correcto — no hay
    "otro" texto que escribir ahí.

    `shape_name="*"` confirma TODAS las zonas de esta diapositiva. Es para los arquetipos con
    decenas de etiquetas de escala idénticas (el planograma del clásico trae 33 celdas
    "D 28.10"), donde enumerarlas una a una es ruido, no rigor. Úsalo con cabeza: en una
    diapositiva de 4 zonas, `"*"` es saltarse el gate."""
    key = id(slide.part.package)
    if shape_name == "*":
        _CONFIRMED_EXAMPLE_TEXT.setdefault(key, set()).add((str(slide.part.partname), "*"))
        origin = _origin_slide_name(slide)
        print(f"[deck-qa] '{origin}': TODAS sus zonas confirmadas como contenido real "
              f"(confirm_example_text(s, \"*\")) — el gate de texto de ejemplo no las mirará.")
        return
    shp = _find_shape(slide, shape_name)
    if not shp.has_text_frame:
        raise ValueError(f"la zona {shape_name!r} no tiene texto")
    _CONFIRMED_EXAMPLE_TEXT.setdefault(key, set()).add((str(slide.part.partname), shape_name))
    print(f"[deck-qa] '{shape_name}': confirmado como contenido real (coincide con el texto de "
          f"ejemplo por diseño de la plantilla, §G13) — no bloqueará save().")


def confirm_example_image(slide, shape_name: str = "*") -> None:
    """Hermana de `confirm_example_text()` para las fotos SEMILLA: confirma que la foto que
    trae la diapositiva canónica es la correcta y no hace falta sustituirla.

    82 zonas de imagen de 35 arquetipos llevan una foto semilla que el build puso para que la
    diapositiva materializada no saliera con un hueco gris. No son banco de marca: un deck que
    clone una de ellas y no llame a `set_image()` entrega esa foto al cliente. `shape_name="*"`
    confirma todas las de esta diapositiva."""
    key = id(slide.part.package)
    if shape_name != "*":
        _find_shape(slide, shape_name)
    _CONFIRMED_EXAMPLE_IMAGE.setdefault(key, set()).add(
        (str(slide.part.partname), shape_name))
    origin = _origin_slide_name(slide)
    print(f"[deck-qa] '{origin}'/{shape_name}: foto semilla confirmada como correcta — no "
          f"aparecerá en el aviso de imagen-semilla de save().")


# ---------------------------------------------------------------------------
# §FOTOGRAFÍA DE MARCA
# ---------------------------------------------------------------------------
# Mantiene el contrato de backend real —`imageryBundleFileId`/`container_upload`— y añade
# validación estricta de `brand: Movistar`. No tocar sin verificar contra sr-agents-api: es la
# interfaz que usa producción hoy.
_IMAGERY_BUNDLE_HINTS = ("movistar-imagery-bundle", "movistar_imagery_bundle", "movistar")
_CACHED_IMAGERY_BUNDLE_DIR: str | None = None


def _normalise_brand(value) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())


def _read_imagery_index(path) -> dict | None:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return None
    return data if _normalise_brand(data.get("brand")) == "movistar" else None


# Umbral de plausibilidad: la foto real más pequeña del banco pesa ~25 KB; un fixture de test
# con imágenes stub (1x1 px) pesa un puñado de bytes. Filtra el falso positivo real de §G15:
# un zip de smoke-test huérfano en /tmp que también declaraba brand=Movistar.
_MIN_PLAUSIBLE_PHOTO_BYTES = 3000


def _zip_movistar_index(zip_path: str):
    import zipfile
    try:
        with zipfile.ZipFile(zip_path) as zf:
            members = zf.namelist()
            names = [n for n in members if n.lower().endswith("imagery-index.json")]
            binaries = {Path(n).stem.lower(): n for n in members
                        if n.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))}
            for name in sorted(names, key=lambda v: (v.count("/"), len(v))):
                data = json.loads(zf.read(name).decode("utf-8"))
                indexed = set()
                for item in data.get("images", []):
                    if item.get("id"):
                        indexed.add(str(item["id"]).lower())
                    if item.get("source_file"):
                        indexed.add(Path(str(item["source_file"])).stem.lower())
                matched = indexed & binaries.keys()
                if _normalise_brand(data.get("brand")) != "movistar" or not matched:
                    continue
                if any(zf.getinfo(binaries[s]).file_size >= _MIN_PLAUSIBLE_PHOTO_BYTES
                       for s in matched):
                    return name, data
    except Exception:
        return None
    return None


def _find_imagery_bundle_zip() -> str | None:
    """Busca el .zip del bundle de imagery inyectado, en las mismas raíces que la plantilla."""
    import glob as _glob
    cands: list[str] = []
    for root in _search_roots():
        cands += _glob.glob(os.path.join(root, "**", "*.zip"), recursive=True)
    ranked = sorted(set(cands), key=lambda path: (
        0 if os.path.basename(path).lower() == "movistar-imagery-bundle.zip" else
        1 if any(h in os.path.basename(path).lower() for h in _IMAGERY_BUNDLE_HINTS) else 2,
        os.path.basename(path).lower(), path,
    ))
    for path in ranked:
        if _zip_movistar_index(path):
            return path
    return None


def _extract_imagery_bundle() -> str | None:
    """Descomprime (una sola vez por turno, cacheado) el bundle plano de imagery inyectado."""
    global _CACHED_IMAGERY_BUNDLE_DIR
    if _CACHED_IMAGERY_BUNDLE_DIR and os.path.isdir(_CACHED_IMAGERY_BUNDLE_DIR):
        return _CACHED_IMAGERY_BUNDLE_DIR
    zip_path = _find_imagery_bundle_zip()
    if not zip_path:
        return None
    import tempfile
    import zipfile
    try:
        out_dir = tempfile.mkdtemp(prefix="mvst_imagery_bundle_")
        with zipfile.ZipFile(zip_path) as zf:
            if not _zip_movistar_index(zip_path):
                raise ValueError("imagery-index.json no declara brand=Movistar")
            zf.extractall(out_dir)
        _CACHED_IMAGERY_BUNDLE_DIR = out_dir
        return out_dir
    except Exception as e:
        print(f"[mvst] no se pudo descomprimir el bundle de imagery ({zip_path}): {e}")
        return None


def _find_imagery_index() -> str | None:
    """Localiza exclusivamente un índice cuyo campo `brand` sea Movistar."""
    import glob as _glob
    direct = (_SKILL_DIR.parent / "movistar-brand-guidelines-v1" / "imagery"
              / "imagery-index.json")
    if direct.is_file() and _read_imagery_index(direct):
        return str(direct)
    for base in _search_roots() + [str(_SKILL_DIR.parent)]:
        hits = _glob.glob(f"{base}/**/movistar-brand-guidelines*/imagery/imagery-index.json",
                          recursive=True)
        for hit in sorted(hits):
            if _read_imagery_index(hit):
                return hit
    bundle_dir = _extract_imagery_bundle()
    if bundle_dir:
        hits = _glob.glob(os.path.join(bundle_dir, "**", "imagery-index.json"), recursive=True)
        for hit in sorted(hits, key=lambda p: (p.count(os.sep), len(p))):
            if _read_imagery_index(hit):
                return hit
    return None


def list_brand_images(*, with_meta: bool = False, momento_dia=None, categoria=None,
                      mood=None, fuente=None, solo_oficial: bool = False) -> list:
    """Fotos de marca montadas en el sandbox (skill `movistar-brand-guidelines`).

    Sin argumentos -> lista de RUTAS ABSOLUTAS de los ficheros que EXISTEN de verdad;
    úsala para elegir imágenes antes de pasarlas a `set_image()`. Nunca construyas la ruta a
    mano: resuelve tanto el banco bundleado en la skill como el bundle plano inyectado por
    `container_upload`.

    `with_meta=True` -> lista de dicts cruzando `imagery/imagery-index.json`:
    `{path, id, source_file, momento_dia, mood, categoria, tags, usos_recomendados,
    usos_evitar, reglas, fuente, exists}`.

    Filtros (solo con metadatos): `momento_dia`, `categoria`, `mood`, `fuente`,
    `solo_oficial`. Respeta SIEMPRE las `reglas` por entrada y las `reglas_globales` del
    índice.

    ⚠️ **12 de las 35 entradas son `categoria: 'fondo'`**: fondos de COLOR PLANO con el claim
    de marca, de uso muy acotado, no fotografía. Sin filtrar, un tercio de la lista no vale
    para un hueco de contenido. Filtra por `categoria` (`personas`, `hogar`, `urbano`,
    `paisaje`, `deporte`, `producto`, `conectividad`) o descarta `'fondo'` a mano;
    `set_image()` avisa si se te cuela uno en una zona que no es a sangre. El índice validado como Movistar es la única autoridad: solo se recorren sus
    entradas `images`, nunca logos ni fotografía de otra marca."""
    import glob as _glob
    exts = (".jpg", ".jpeg", ".png", ".webp")
    index_path = _find_imagery_index()
    if not index_path:
        return []
    idx = _read_imagery_index(index_path)
    if not idx:
        print(f"[mvst] índice rechazado: brand distinto de Movistar ({index_path})")
        return []
    files = []
    local_root = os.path.join(os.path.dirname(index_path), "assets", "imagery")
    if os.path.isdir(local_root):
        files += _glob.glob(os.path.join(local_root, "**", "*"), recursive=True)
    bundle_dir = _extract_imagery_bundle()
    if bundle_dir:
        files += _glob.glob(os.path.join(bundle_dir, "**", "*"), recursive=True)
    files = sorted({p for p in files if p.lower().endswith(exts) and os.path.isfile(p)})

    img_dir = os.path.join(os.path.dirname(index_path), "assets", "imagery")
    by_stem = {}
    for p in files:
        by_stem.setdefault(os.path.splitext(os.path.basename(p))[0].lower(), p)
    recs = []
    for e in idx.get("images", []):
        sf = e.get("source_file", "")
        nested_path = os.path.join(img_dir, sf) if sf else ""
        stem_key = (e.get("id") or os.path.splitext(os.path.basename(sf))[0]).lower()
        flat_path = by_stem.get(stem_key)
        if nested_path and os.path.exists(nested_path):
            path = nested_path
        elif flat_path:
            path = flat_path
        else:
            path = nested_path
        rec = {
            "path": path, "id": e.get("id"), "source_file": sf,
            "momento_dia": e.get("momento_dia"), "mood": e.get("mood"),
            "categoria": e.get("categoria"), "tags": e.get("tags", []),
            "usos_recomendados": e.get("usos_recomendados", []),
            "usos_evitar": e.get("usos_evitar", []), "reglas": e.get("reglas", []),
            "fuente": e.get("fuente"), "exists": bool(path) and os.path.exists(path),
        }
        if momento_dia is not None and rec["momento_dia"] != momento_dia:
            continue
        if categoria is not None and rec["categoria"] != categoria:
            continue
        if mood is not None and rec["mood"] != mood:
            continue
        if fuente is not None and rec["fuente"] != fuente:
            continue
        if solo_oficial and rec["fuente"] != "oficial-movistar-2025":
            continue
        recs.append(rec)
    recs.sort(key=lambda r: (r.get("source_file") or ""))
    return recs if with_meta else [r["path"] for r in recs if r["exists"]]


# ---------------------------------------------------------------------------
# §GATES DE TEXTO DE EJEMPLO, IMAGEN SEMILLA Y ANTI-VACÍO
# ---------------------------------------------------------------------------
def _norm_ws(text) -> str:
    return " ".join(str(text).split())


def _generated_slides(deck):
    """`[(n, slide, arquetipo)]` de las diapositivas CREADAS con use() (no las canónicas)."""
    originals = _ORIGINALS_BY_DECK.get(id(deck), set())
    out = []
    n = 0
    for slide in deck.slides:
        if slide.part.partname in originals:
            continue
        n += 1
        out.append((n, slide, _origin_slide_name(slide)))
    return out


def _confirmed(registry: dict, slide, shape_name: str) -> bool:
    entries = registry.get(id(slide.part.package), set())
    part = str(slide.part.partname)
    return (part, shape_name) in entries or (part, "*") in entries


def _zones_with_example_text(deck) -> tuple[dict, dict]:
    """`(bloqueantes, avisos)`, ambos `{«diapo N (ARQUETIPO)»: [descripción de zona]}`.

    Reformado en la v4 sobre `example_text_kind` del catálogo, porque a 156 arquetipos las
    tres clases de texto de ejemplo necesitan tratos distintos:

    - `disenado` (286 zonas): lo escribió el diseñador del cliente. **BLOQUEA** si sigue ahí.
    - `generico` (355 zonas): lo generó el build al materializar las 82 diapositivas del
      clásico. **BLOQUEA** si sigue ahí **y también si la zona quedó VACÍA** — con 82
      diapositivas materializadas el modelo tiende a borrar el run en vez de rellenarlo, y el
      gate de la v3 (comparación literal contra el ejemplo) dejaba pasar la caja vacía.
    - `numerico` (84 zonas): una cifra, un "01", un "%". **Solo AVISA**: con 42 separadores en
      el catálogo, bloquear obligaría a 4-6 `confirm_example_text()` por deck y cada olvido
      cuesta una ronda entera dentro de los 20 minutos. El valor real coincide con el de
      ejemplo por diseño en la mayoría de los casos (§G13).

    Se EXCLUYE `kind: "chrome"` (el número de página: campo dinámico de PowerPoint, su texto
    cacheado nunca es un defecto). Una zona borrada con `remove_shape()` no aparece, y una
    confirmada con `confirm_example_text()` tampoco.
    """
    blocking: dict = {}
    warning: dict = {}
    for n, slide, origin in _generated_slides(deck):
        if origin is None:
            continue
        shapes = {s.name: s for s in _iter_shapes_recursive(slide.shapes)}
        label = f"diapo {n} ({origin})"
        for el in _slide_info(origin).get("elements", []):
            if el.get("kind") != "text":
                continue
            kind = el.get("example_text_kind")
            example = el.get("example_text")
            if not example or kind is None:
                continue
            name = el["shape_name"]
            if _confirmed(_CONFIRMED_EXAMPLE_TEXT, slide, name):
                continue
            shp = shapes.get(name)
            if shp is None or not shp.has_text_frame:
                continue  # eliminada con remove_shape() — escape legítimo
            current = _norm_ws(shp.text_frame.text)
            same = current == _norm_ws(example)
            empty = current == ""
            if not (same or empty):
                continue
            preview = _norm_ws(example)
            if len(preview) > 42:
                preview = preview[:39] + "…"
            reason = "VACÍA" if empty else f"«{preview}»"
            row = f"'{name}' ({el.get('role') or 'texto'}): {reason}"
            if kind == "numerico":
                warning.setdefault(label, []).append(row)
            elif kind == "generico":
                blocking.setdefault(label, []).append(row)
            elif same:  # disenado
                blocking.setdefault(label, []).append(row)
            else:       # disenado y vacía: el diseñador la calibró, vaciarla es un defecto
                blocking.setdefault(label, []).append(row)
    return blocking, warning


def _zones_with_seed_image(deck) -> dict:
    """`{«diapo N (ARQUETIPO)»: [shape_name]}` de las zonas de imagen SEMILLA que nadie
    sustituyó ni confirmó.

    82 zonas de 35 arquetipos llevan una foto que el build puso al materializar la
    diapositiva, para que no saliera con un hueco gris. No son banco de marca: entregarlas es
    entregar la foto de otro. Se detecta por registro (`set_image()` marca la zona), no
    comparando blobs: es determinista y no depende de que la foto elegida sea distinta.

    ⚠️ En 4.0.0 esto es **AVISO**, no gate duro (`qa_gates.seed_image_gate`): Movistar es la
    única marca en producción y un script guardado en SuperStudio que hoy entrega pasaría a
    fallar de golpe. Sube a `block` en 4.1.0."""
    out: dict = {}
    for n, slide, origin in _generated_slides(deck):
        if origin is None:
            continue
        label = f"diapo {n} ({origin})"
        for el in _slide_info(origin).get("elements", []):
            if el.get("kind") not in ("image", "background") or not el.get("seeded"):
                continue
            name = el["shape_name"]
            if _is_touched(slide, name, _IMAGES_SET):
                continue
            if _confirmed(_CONFIRMED_EXAMPLE_IMAGE, slide, name):
                continue
            if not any(s.name == name for s in _iter_shapes_recursive(slide.shapes)):
                continue  # eliminada con remove_shape()
            out.setdefault(label, []).append(f"'{name}' ({el.get('seed_asset') or 'semilla'})")
    return out


def _underfilled_slides(deck) -> list[str]:
    """Diapositivas cuyo ratio de zonas atendidas baja de `qa_gates.min_filled_ratio`.

    Mecaniza la regla ANTI-VACÍO, que hasta ahora solo estaba escrita en prosa en el
    `SKILL.md`: cada diapositiva real está diseñada para llenarse ENTERA, y si te sobra una
    zona es señal de que toca otro arquetipo. Cuenta como "atendida" cualquier zona de
    texto/imagen/gráfica/tabla que haya recibido una llamada del motor, o que traiga contenido
    distinto del ejemplo, o que se haya confirmado/eliminado explícitamente.

    Es AVISO, no gate: no hay forma fiable de distinguir un vacío por descuido de un vacío
    deliberado, y bloquear por esto castigaría decisiones legítimas."""
    gates = _qa_gates()
    threshold = gates["min_filled_ratio"]
    warns: list[str] = []
    for n, slide, origin in _generated_slides(deck):
        if origin is None:
            continue
        info = _slide_info(origin)
        shapes = {s.name: s for s in _iter_shapes_recursive(slide.shapes)}
        total = filled = 0
        for el in info.get("elements", []):
            kind = el.get("kind")
            if kind not in ("text", "image", "background", "chart", "table"):
                continue
            name = el["shape_name"]
            if name not in shapes:
                continue  # eliminada con remove_shape(): no cuenta ni a favor ni en contra
            total += 1
            if (_is_touched(slide, name, _TOUCHED)
                    or _confirmed(_CONFIRMED_EXAMPLE_TEXT, slide, name)
                    or _confirmed(_CONFIRMED_EXAMPLE_IMAGE, slide, name)):
                filled += 1
            elif kind == "text":
                current = _norm_ws(shapes[name].text_frame.text)
                if current and current != _norm_ws(el.get("example_text") or ""):
                    filled += 1
        if total >= 3 and filled / total < threshold:
            blocks = _blocks_of(info)
            extra = (f" · la maqueta tiene {blocks} bloques "
                     f"{(info.get('n_items') or {}).get('eje')}" if blocks else "")
            warns.append(
                f"diapo {n} ({origin}): solo {filled}/{total} zonas rellenadas "
                f"({filled/total:.0%} < {threshold:.0%}){extra} — una diapositiva real a medio "
                f"llenar se ve ROTA, no minimalista. Rellena el resto o cambia de arquetipo "
                f"(find_slides(family='{info['family']}', n_items=…)).")
    return warns


# ---------------------------------------------------------------------------
# §QA DE COMPOSICIÓN DEL DECK
# ---------------------------------------------------------------------------
def _chapter_color_warnings(dividers: list[tuple[int, str]]) -> list[str]:
    """Coherencia del color de capítulo entre los separadores del deck.

    Con 42 separadores en el catálogo es el error de marca más probable, y el dato para
    detectarlo ya existía (`variant.value`/`bg_semantic` del catálogo + `chapter_color_system`
    de `brand-config.json`) sin que nadie lo usara. Tres reglas:

      1. El mismo color para DOS capítulos distintos (habiendo más de un color en juego): el
         lector deja de poder atribuir una sección a su capítulo. Un deck monocolor deliberado
         no dispara nada.
      2. Un color de fondo fuera de los que la plantilla ofrece para un separador.
      3. Desviación de `by_chapter` **solo si el deck ya lo está siguiendo** (la mitad o más de
         los separadores casan): así se caza el deck que acertó 3 de 4 sin dar la lata al que
         tiene su propio esquema.
    """
    if len(dividers) < 2:
        return []
    system = brand_config().get("chapter_color_system") or {}
    by_chapter = system.get("by_chapter") or {}
    allowed = set(system.get("allowed") or [])
    warns: list[str] = []

    colors = [c for _, c in dividers if c]
    if len(set(colors)) > 1:
        for color, count in Counter(colors).items():
            if count > 1:
                where = [str(i) for i, c in dividers if c == color]
                warns.append(
                    f"color de capítulo {color} repetido en los separadores de las diapos "
                    f"{', '.join(where)}: con varios colores en juego, repetir uno impide "
                    f"atribuir cada sección a su capítulo. Usa un color por capítulo "
                    f"(find_slides(role_in_deck='divider', variant='…')) o el MISMO en todos.")
    if allowed:
        for idx, color in dividers:
            if color and color not in allowed:
                warns.append(f"diapo {idx}: fondo de separador {color}, fuera del sistema de "
                             f"capítulos declarado ({' · '.join(sorted(allowed))}).")

    expected = [by_chapter.get(f"{i + 1:02d}") for i in range(len(dividers))]
    pairs = [(i, c, e) for (i, c), e in zip(dividers, expected) if e]
    if pairs:
        matches = sum(1 for _, c, e in pairs if c == e)
        if matches and matches >= len(pairs) / 2:
            for idx, color, exp in pairs:
                if color != exp:
                    warns.append(
                        f"diapo {idx}: este deck sigue el sistema de capítulos declarado "
                        f"({matches}/{len(pairs)} aciertos) pero aquí el color es {color} y el "
                        f"capítulo corresponde a {exp} — usa "
                        f"find_slides(role_in_deck='divider', variant='{exp}').")
    return warns


def _master_share_warnings(names: list[str]) -> list[str]:
    """Aviso si un sistema de diseño queda como RESIDUO minoritario del deck.

    Un deck 50/50 es una decisión (el usuario pidió mezclar); un deck con 1 de 14
    diapositivas del otro master es un descuido, y se ve: son dos lenguajes visuales
    distintos. Por debajo de `qa_gates.min_master_share` se avisa y se propone el hermano
    equivalente del sistema dominante, resuelto por `composition_id`."""
    slides = catalog()["slides"]
    systems = [slides[n]["system"] for n in names if n]
    if len(set(systems)) < 2:
        return []
    total = len(systems)
    counts = Counter(systems)
    (dominant, dcount), (minor, mcount) = counts.most_common(2)
    share = mcount / total
    if share >= _qa_gates()["min_master_share"]:
        return []
    dom_label = _SYSTEM_LABEL.get(dominant, dominant)
    lines = [f"mezcla de sistemas: {mcount}/{total} diapositivas ({share:.0%}) son del sistema "
             f"'{_SYSTEM_LABEL.get(minor, minor)}' y el resto de '{dom_label}'. Son dos "
             f"lenguajes visuales distintos y a ese peso parece un residuo, no una decisión "
             f"(un deck 50/50 no dispara este aviso). Sustitutos equivalentes:"]
    fallback = f"(sin equivalente directo; usa find_slides(family=…, master='{dom_label}'))"
    for idx, name in enumerate(names, start=1):
        if not name or slides[name]["system"] != minor:
            continue
        twin = _cross_system_twin(name)
        lines.append(f"   diapo {idx}: {name} → {twin or fallback}")
    return ["\n".join(lines)]


def verify_deck(deck) -> list[str]:
    """Avisos de composición del deck TERMINADO (tras los `use()` necesarios, antes o después
    de `save()`; ignora las canónicas originales y evalúa solo las copias). NO bloquea: son
    señales para revisar antes de entregar.

    Comprueba: apertura/cierre, monotonía (3 seguidas iguales), arquetipo dominante,
    **composición dominante** (el gate que de verdad importa a 156 arquetipos: seis nombres
    distintos de `INTERIOR_TXT_*` pueden verse casi iguales y pasar un check de nombres),
    exceso de divisores, mezcla residual de los dos sistemas de diseño, coherencia del color
    de capítulo, y relleno de cada diapositiva (ANTI-VACÍO)."""
    cat = catalog()["slides"]
    names = [origin for _, _, origin in _generated_slides(deck)]
    n = len(names)
    if n == 0:
        return ["El deck no tiene ninguna diapositiva — llama a use() al menos una vez."]

    warns: list[str] = []
    first_role = cat.get(names[0], {}).get("role_in_deck") if names[0] else None
    if first_role not in ("cover", "legal"):
        warns.append(f"La primera diapositiva ({names[0]!r}) no es portada — un deck abre con "
                     f"PORTADA_* (o AVISO_CONFIDENCIALIDAD si lo requiere).")
    last_role = cat.get(names[-1], {}).get("role_in_deck") if names[-1] else None
    if last_role != "closing":
        warns.append(f"La última diapositiva ({names[-1]!r}) no es de cierre — considera "
                     f"CIERRE_M o find_slides(role_in_deck='closing').")
    for i in range(max(0, n - 2)):
        if names[i] and names[i] == names[i + 1] == names[i + 2]:
            warns.append(f"3 diapositivas seguidas del mismo arquetipo ({names[i]!r}) en las "
                         f"posiciones {i+1}-{i+3} — monotonía visual.")

    gates = _qa_gates()
    if n >= 6:
        counts = Counter(x for x in names if x)
        dominant, dcount = counts.most_common(1)[0]
        if dcount / n > gates["max_dominant_slide_ratio"]:
            warns.append(f"'{dominant}' es {dcount}/{n} ({dcount/n:.0%}) del deck, por encima "
                         f"del {gates['max_dominant_slide_ratio']:.0%} — poca variedad.")
        comps = Counter(cat[x]["composition_id"] for x in names if x)
        comp, ccount = comps.most_common(1)[0]
        if ccount / n > gates["max_dominant_composition_ratio"]:
            members = [x for x in names if x and cat[x]["composition_id"] == comp]
            warns.append(
                f"la MAQUETA '{comp}' es {ccount}/{n} ({ccount/n:.0%}) del deck, por encima "
                f"del {gates['max_dominant_composition_ratio']:.0%} "
                f"(`max_dominant_composition_ratio`). Los nombres pueden ser distintos "
                f"({' · '.join(sorted(set(members))[:4])}) pero el cliente ve la misma página "
                f"repetida: es lo que mide este gate y no el de nombres.")

    n_dividers = sum(1 for x in names if x and cat.get(x, {}).get("role_in_deck") == "divider")
    if n_dividers and n_dividers / n > gates["max_divider_ratio"]:
        warns.append(f"{n_dividers}/{n} diapositivas son divisores "
                     f"({n_dividers/n:.0%} > {gates['max_divider_ratio']:.0%}) — probablemente "
                     f"sobran secciones.")

    warns += _master_share_warnings(names)
    dividers = [(i, _color_token(cat[x])) for i, x in enumerate(names, start=1)
                if x and cat[x]["role_in_deck"] == "divider"]
    warns += _chapter_color_warnings(dividers)
    warns += _underfilled_slides(deck)
    seeds = _zones_with_seed_image(deck)
    if seeds:
        total = sum(len(v) for v in seeds.values())
        block = _qa_gates()["seed_image_gate"] == "block"
        head = (f"{total} zona(s) de imagen conservan la foto SEMILLA de la plantilla (no es "
                f"banco de marca: se entregaría la foto de otro). Sustitúyelas con set_image() "
                f"—list_brand_images() da el banco real— o confírmalas con "
                f"confirm_example_image(s).")
        warns.append(head + ("" if block else " [aviso en 4.0.0, gate duro en 4.1.0]") + "\n"
                     + "\n".join(f"   {k}: {', '.join(v)}" for k, v in seeds.items()))
    _, numeric = _zones_with_example_text(deck)
    if numeric:
        warns.append("zonas numéricas que conservan su valor de ejemplo (normalmente correcto "
                     "por diseño, §G13 — revisa que el número sea el del capítulo real):\n"
                     + "\n".join(f"   {k}: {', '.join(v)}" for k, v in numeric.items()))
    return warns


# ---------------------------------------------------------------------------
# §GUARDADO
# ---------------------------------------------------------------------------
def outputs_dir() -> str:
    """Directorio que el runtime captura como salida (skills -> /files/output)."""
    def _usable(path: str) -> str | None:
        try:
            candidate = Path(path).expanduser()
            candidate.mkdir(parents=True, exist_ok=True)
            return (str(candidate.resolve())
                    if candidate.is_dir() and os.access(candidate, os.W_OK) else None)
        except OSError:
            return None
    for ev in ("OUTPUT_DIR", "ANTHROPIC_OUTPUT_DIR"):
        v = os.environ.get(ev)
        if v:
            usable = _usable(v)
            if usable:
                return usable
    candidates = [] if os.name == "nt" else ["/files/output", "/mnt/user-data/outputs"]
    for directory in candidates:
        if os.path.isdir(directory):
            usable = _usable(directory)
            if usable:
                return usable
    return str(Path.cwd().resolve())


def save(deck, out_path: str, *, run_qa: bool = True) -> str:
    """GATE DURO primero: si alguna zona de texto conserva el texto de ejemplo de la plantilla
    —o quedó VACÍA una zona que el build había rellenado— lanza `RuntimeError` SIN guardar. El
    informe va **agrupado por diapositiva**, que es como se corrige. Después elimina las 156
    diapositivas canónicas de ejemplo (nunca deben llegar al entregable), guarda, y corre
    `finalize_pptx` + `verify_pptx` (gate duro de integridad OPC, §G5/§G6) + `verify_deck`
    (avisos de composición, no bloqueante).

    El deck sigue en memoria si el gate falla: corrige y vuelve a llamar a `save()`."""
    blocking, _ = _zones_with_example_text(deck)
    if blocking:
        total = sum(len(v) for v in blocking.values())
        lines = []
        for label, rows in blocking.items():
            lines.append(f"  {label}:")
            lines += [f"     - {r}" for r in rows]
        raise RuntimeError(
            f"El deck NO se guarda: {total} zona(s) de texto en {len(blocking)} diapositiva(s) "
            f"conservan el texto de ejemplo de la plantilla o quedaron vacías — llegarían al "
            f"cliente tal cual:\n" + "\n".join(lines) + "\n"
            "Remedio: escribe el contenido real con set_text()/set_texts()/set_page_header(). "
            "Si el valor real coincide con el de ejemplo por diseño (el número de un "
            "separador, la numeración de un índice), confírmalo con "
            "confirm_example_text(slide, shape_name) — o con "
            "confirm_example_text(slide, \"*\") si la diapositiva trae decenas de etiquetas de "
            "escala idénticas. Solo si la zona de verdad no aplica (excepcional), elimínala con "
            "remove_shape(slide, shape_name).")

    original_partnames = _ORIGINALS_BY_DECK.get(id(deck), set())
    xml_slides = deck.slides._sldIdLst
    to_remove = [el for slide, el in zip(deck.slides, list(xml_slides))
                 if slide.part.partname in original_partnames]
    for el in to_remove:
        rid = el.get(qn("r:id"))
        deck.part.drop_rel(rid)
        xml_slides.remove(el)
    if len(list(xml_slides)) == 0:
        raise RuntimeError("El deck no tiene ninguna diapositiva generada (no llamaste a use() "
                           "nunca). No se guarda un .pptx vacío.")

    requested = Path(out_path).expanduser()
    target = (requested if requested.is_absolute() or requested.parent != Path(".")
              else Path(outputs_dir()) / requested.name)
    target.parent.mkdir(parents=True, exist_ok=True)
    out_path = str(target.resolve())
    deck.save(out_path)
    if run_qa:
        subprocess.run([sys.executable, str(_SCRIPTS / "finalize_pptx.py"), out_path],
                       check=True)
        r = subprocess.run([sys.executable, str(_SCRIPTS / "verify_pptx.py"), out_path])
        if r.returncode != 0:
            raise RuntimeError("verify_pptx falló: corrige los defectos antes de entregar.")
        try:
            warns = verify_deck(deck)
        except Exception as e:
            warns = []
            print(f"[deck-qa] no se pudo evaluar la composición: {e}")
        if warns:
            print(f"[deck-qa] {len(warns)} aviso(s) de composición:")
            for w in warns:
                print("   -", w)
    return out_path


if __name__ == "__main__":  # pragma: no cover — diagnóstico rápido del motor
    cat = catalog()
    print(f"mvst_pptx v{__version__} · catálogo v{cat['catalog_version']} · "
          f"{cat['n_slides']} arquetipos · {len(cat['compositions'])} composiciones · "
          f"{len(cat['masters'])} sistemas")
    for fam, info in families().items():
        print(f"  {fam:<12} {info['n']:>3} arquetipos · {info['compositions']:>3} maquetas "
              f"· [C] {info['default']}")
