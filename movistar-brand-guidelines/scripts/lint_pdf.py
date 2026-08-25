#!/usr/bin/env python3
"""lint_pdf.py — gate determinista de QA de MARCA para un PDF (skill prebuilt `pdf` / reportlab).

Hermano de `lint_artifact.py` (que hace lo propio para artifacts HTML/React), pero para el camino
de PDF de esta skill — ver SKILL.md §"Generar un PDF con la skill prebuilt pdf". Extrae el texto
visible del PDF y aplica las reglas de MARCA de texto de esta skill (las mismas del
`lint_artifact.py` de al lado — se importan de ahí para tener UNA sola fuente de verdad, sin
duplicar los regex ni arriesgar que deriven). No renderiza: para la revisión de composición por
visión está `qa_render_pdf.py`, que complementa a este (uno mira el texto, el otro la maqueta).

Motivación real: este QA nació de dos defectos encontrados generando un PDF de historia de marca —
(1) un tracking (`Tc`) que se filtraba del titular al cuerpo desbordaba el texto sin lanzar error
(lo atrapa `qa_render_pdf.py`; el leak ya está corregido en `*_pdf_helpers.py::tracked_text`), y
(2) el nombre de marca escrito en CAJA ALTA en un titular (lo atrapa este linter). Ambos son fallos
silenciosos, justo lo que el patrón "gate mecánico" de esta skill existe para evitar.

⚠️ Límite conocido y mitigado: el texto dibujado con tracking abierto (`setCharSpace`, típico de
titulares/claim) se extrae a menudo con ESPACIOS entre letras ("D E A L H A M B R A"), porque el
extractor interpreta el hueco entre glifos como separación de palabra. Por eso, además de revisar
línea a línea (fiable para el cuerpo, sin tracking), este linter revisa también un flujo con TODO
el espaciado colapsado, donde un token prohibido en caja alta (p.ej. "ALHAMBRA") vuelve a ser
contiguo. Aun así, para composición fina fíate del render (`qa_render_pdf.py`), no solo del texto.

Degrada sin romper: si no hay ninguna librería de extracción (pdfplumber/pypdf/PyMuPDF), devuelve un
único WARN en vez de reventar (mismo principio que `qa_render_pdf.py` y `qa_render.py`).

Uso:
    python3 lint_pdf.py archivo.pdf        # CLI: imprime hallazgos, exit code 1 si hay FAIL
    from lint_pdf import lint               # librería: lint("archivo.pdf") -> list[Finding]
"""
from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass

# Reutiliza los regex de MARCA del linter de artifacts de ESTA misma skill (única fuente de verdad).
# Su import es idéntico en las 4 marcas; los nombres concretos de regex que se usan viven abajo, en
# la sección "REGLAS DE TEXTO POR MARCA" (lo único que difiere entre marcas en este fichero).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint_artifact as _la  # noqa: E402


@dataclass
class Finding:
    rule: str
    severity: str  # "FAIL" | "WARN"
    detail: str
    snippet: str = ""

    def to_dict(self) -> dict:
        return {"rule": self.rule, "severity": self.severity, "detail": self.detail, "snippet": self.snippet}


# -- Extracción de texto del PDF (pdfplumber → pypdf → PyMuPDF; degrada a None) -------------------
def _extract_pdf_text(pdf_path: str) -> "list[str] | None":
    """Devuelve las líneas de texto visible del PDF (stripped, sin vacías), o None si no hay ninguna
    librería de extracción disponible. Prueba pdfplumber, luego pypdf, luego PyMuPDF (fitz) — el
    primero que esté. No revienta: cualquier fallo de una librería concreta cae a la siguiente."""
    raw = None
    # 1) pdfplumber
    try:
        import pdfplumber
        parts = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                parts.append(page.extract_text() or "")
        raw = "\n".join(parts)
    except Exception:
        raw = None
    # 2) pypdf
    if raw is None:
        try:
            from pypdf import PdfReader
            reader = PdfReader(pdf_path)
            raw = "\n".join((pg.extract_text() or "") for pg in reader.pages)
        except Exception:
            raw = None
    # 3) PyMuPDF
    if raw is None:
        try:
            import fitz
            doc = fitz.open(pdf_path)
            raw = "\n".join(doc[i].get_text() for i in range(doc.page_count))
        except Exception:
            raw = None
    if raw is None:
        return None
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


# ─────────────────────────────────────────────────────────────────────────────────────────────
# ── REGLAS DE TEXTO POR MARCA — lo ÚNICO que difiere entre las 4 skills. Todo lo demás de este
#    fichero (extracción, Finding, orquestación, main) es idéntico byte a byte.
# ─────────────────────────────────────────────────────────────────────────────────────────────
def brand_text_findings(lines: "list[str]", collapsed: str) -> "list[Finding]":
    """Reglas de MARCA de Movistar reutilizadas de lint_artifact (solo texto visible). FAIL: em-dash
    "\u2014" (regla n\u00ba1) y "movistar" con m min\u00fascula (principio 1). WARN: "!"/"?" de cierre sin su
    signo de apertura RAE. El em-dash se busca tambi\u00e9n en el flujo colapsado (por si un titular con
    tracking se extrae con las letras/signos separados)."""
    out: list[Finding] = []
    joined = " ".join(lines)
    if _la._EMDASH_RE.search(joined) or _la._EMDASH_RE.search(collapsed):
        snippet = next((ln for ln in lines if _la._EMDASH_RE.search(ln)), "\u2014")
        out.append(Finding("em_dash", "FAIL",
                            'Em-dash "\u2014" en el copy \u2014 Movistar no lo usa; usa comas, dos puntos o '
                            "frases cortas (SKILL.md regla n\u00ba1, brand/copywriting.md \u00a71.3).",
                            snippet[:80]))
    seen_lower = False
    for ln in lines:
        if not seen_lower and _la._MOVISTAR_LOWER_RE.search(ln):
            seen_lower = True
            out.append(Finding("marca_m_minuscula", "FAIL",
                                '"movistar" con "m" min\u00fascula \u2014 la M de Movistar va SIEMPRE en '
                                "may\u00fascula (brand/copywriting.md \u00a71.3 principio 1).", ln[:80]))
        if "!" in ln and "\u00a1" not in ln:
            out.append(Finding("exclamacion_sin_apertura", "WARN",
                                'Signo "!" de cierre sin su "\u00a1" de apertura \u2014 Movistar sigue la '
                                "RAE (apertura + cierre). Conf\u00edrmalo si el texto se parte entre "
                                "l\u00edneas.", ln[:80]))
        if "?" in ln and "\u00bf" not in ln:
            out.append(Finding("interrogacion_sin_apertura", "WARN",
                                'Signo "?" de cierre sin su "\u00bf" de apertura \u2014 Movistar sigue la '
                                "RAE (apertura + cierre). Conf\u00edrmalo si el texto se parte entre "
                                "l\u00edneas.", ln[:80]))
    return out
# ─────────────────────────────────────────────────────────────────────────────────────────────
# ── FIN REGLAS DE TEXTO POR MARCA
# ─────────────────────────────────────────────────────────────────────────────────────────────


# -- Orquestación (idéntica entre marcas) --------------------------------------------------------
def lint(pdf_path: str) -> "list[Finding]":
    lines = _extract_pdf_text(pdf_path)
    if lines is None:
        return [Finding("pdf_sin_extractor", "WARN",
                        "No hay librería para extraer texto del PDF (pdfplumber/pypdf/PyMuPDF) — no "
                        "se pudo lintar el texto. Revisa a mano o usa qa_render_pdf.py para QA por "
                        "visión.", "")]
    collapsed = re.sub(r"\s+", "", " ".join(lines))
    return brand_text_findings(lines, collapsed)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) != 2:
        print("Uso: python3 lint_pdf.py <fichero.pdf>", file=sys.stderr)
        return 2
    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"No existe: {path}", file=sys.stderr)
        return 2
    findings = lint(path)
    fails = [f for f in findings if f.severity == "FAIL"]
    warns = [f for f in findings if f.severity == "WARN"]
    if not findings:
        print("[lint_pdf] OK — sin hallazgos.")
        return 0
    print(f"[lint_pdf] {len(fails)} FAIL, {len(warns)} WARN\n")
    for f in fails + warns:
        print(f"[{f.severity}] {f.rule}: {f.detail}")
        if f.snippet:
            print(f"   snippet: {f.snippet!r}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
