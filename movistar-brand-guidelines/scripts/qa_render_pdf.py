#!/usr/bin/env python3
"""
qa_render_pdf.py — Render de un PDF a PNG (uno por página) para QA POR VISIÓN.

Hermano de `alhambra-pptx-v1/scripts/qa_render.py` (que hace lo mismo para `.pptx`), pero para el
camino de PDF de esta skill (la skill prebuilt `pdf` / reportlab, ver SKILL.md §"Generar un PDF con
la skill prebuilt pdf"). A diferencia de un artifact HTML —que NO se renderiza en el sandbox y por
eso solo tiene el gate estático `lint_artifact.py`— un PDF SÍ se puede rasterizar en el sandbox, así
que aquí el modelo puede "mirar" cada página y revisar composición (desbordes, solapes, texto sobre
foto sin contraste, número sobre el logo, página vacía) ANTES de entregar. Complementa a
`lint_pdf.py` (gate determinista sobre el texto), no lo sustituye.

Este QA nació de un fallo real: un tracking (`Tc`) que se filtraba del titular al cuerpo desbordaba
el texto fuera de su columna sin lanzar ningún error — invisible para un linter de texto, evidente
en el render. Ese leak ya está corregido en `*_pdf_helpers.py::tracked_text`; este render es la red
que lo habría atrapado.

Uso:
    from qa_render_pdf import render
    pngs = render("/files/output/historia-alhambra.pdf")
    # abre cada PNG con visión; si hay defecto, corrige y regenera.

Degrada sin romper (mismo principio que qa_render.py): si no hay ningún rasterizador disponible
(pdftoppm de poppler, ni PyMuPDF), render() devuelve [] y debes entregar el PDF con el qa_flag
"qa_sin_render" — nunca revienta por falta de herramientas.
"""
from __future__ import annotations
import glob
import os
import shutil
import subprocess
import tempfile


def _have(tool: str) -> bool:
    return shutil.which(tool) is not None


def _render_poppler(pdf_path: str, work: str, dpi: int) -> list[str]:
    prefix = os.path.join(work, "page")
    try:
        subprocess.run(
            ["pdftoppm", "-png", "-r", str(dpi), pdf_path, prefix],
            check=True, timeout=240,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        print(f"[qa_render_pdf] fallo pdftoppm: {e}")
        return []
    return sorted(glob.glob(prefix + "*.png"))


def _render_pymupdf(pdf_path: str, work: str, dpi: int) -> list[str]:
    try:
        import fitz  # PyMuPDF
    except Exception:
        return []
    try:
        doc = fitz.open(pdf_path)
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        out = []
        for i in range(doc.page_count):
            png = os.path.join(work, f"page-{i + 1:02d}.png")
            doc[i].get_pixmap(matrix=mat).save(png)
            out.append(png)
        return out
    except Exception as e:
        print(f"[qa_render_pdf] fallo PyMuPDF: {e}")
        return []


def render(pdf_path: str, dpi: int = 110, outdir: str | None = None) -> list[str]:
    """PDF -> PNG por página. Devuelve rutas PNG ordenadas, o [] si no hay rasterizador (degrada
    sin romper). Intenta primero poppler (pdftoppm), luego PyMuPDF (fitz) — el que esté."""
    if not pdf_path or not os.path.isfile(pdf_path):
        print(f"[qa_render_pdf] no existe el PDF: {pdf_path!r}")
        return []

    work = outdir or tempfile.mkdtemp(prefix="qa_pdf_")
    os.makedirs(work, exist_ok=True)

    pngs: list[str] = []
    if _have("pdftoppm"):
        pngs = _render_poppler(pdf_path, work, dpi)
    if not pngs:
        pngs = _render_pymupdf(pdf_path, work, dpi)

    if not pngs:
        print("[qa_render_pdf] sin rasterizador (pdftoppm/PyMuPDF) - sin QA por visión "
              "(qa_flag: qa_sin_render)")
        return []
    print(f"[qa_render_pdf] {len(pngs)} PNG(s) generados en {work}")
    return pngs


if __name__ == "__main__":
    import sys
    for p in render(sys.argv[1] if len(sys.argv) > 1 else ""):
        print(p)
