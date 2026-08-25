#!/usr/bin/env python3
"""Render PPTX→PDF→PNG para QA visual, con soporte Windows/Linux/macOS."""
from __future__ import annotations

import glob
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def _soffice() -> str | None:
    exe = shutil.which("soffice") or shutil.which("soffice.exe")
    if exe:
        return exe
    for candidate in (
        "/usr/bin/soffice", "/usr/local/bin/soffice", "/opt/libreoffice/program/soffice",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ):
        if os.path.isfile(candidate):
            return candidate
    return None


def _fitz():
    try:
        import fitz
        return fitz
    except Exception:
        return None


def _raster_fitz(fitz, pdf: str, work: str, dpi: int) -> list[str]:
    result = []
    try:
        doc = fitz.open(pdf)
        try:
            for index, page in enumerate(doc, 1):
                pixmap = page.get_pixmap(dpi=dpi)
                path = os.path.join(work, f"slide-{index:02d}.png")
                pixmap.save(path)
                result.append(path)
        finally:
            doc.close()
    except Exception as exc:
        print(f"[qa_render] fallo fitz al rasterizar: {exc}")
        return []
    return sorted(result)


def _raster_pdftoppm(pdf: str, work: str, dpi: int) -> list[str]:
    prefix = os.path.join(work, "slide")
    try:
        subprocess.run(
            ["pdftoppm", "-png", "-r", str(dpi), pdf, prefix], check=True, timeout=240,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        print(f"[qa_render] fallo pdftoppm: {exc}")
        return []
    return sorted(glob.glob(prefix + "*.png"))


def render(pptx_path: str, dpi: int = 110, outdir: str | None = None) -> list[str]:
    """Devuelve un PNG por slide, o [] si faltan las dependencias de render."""
    if not pptx_path or not os.path.isfile(pptx_path):
        print(f"[qa_render] no existe el .pptx: {pptx_path!r}")
        return []
    soffice, fitz = _soffice(), _fitz()
    have_ppm = shutil.which("pdftoppm") is not None
    if not soffice or not (fitz or have_ppm):
        print("[qa_render] soffice/(fitz|pdftoppm) no disponibles -> qa_flag: qa_sin_render")
        return []
    work = outdir or tempfile.mkdtemp(prefix="qa_")
    os.makedirs(work, exist_ok=True)
    base = os.path.splitext(os.path.basename(pptx_path))[0]
    profile = os.path.join(work, "lo_profile")
    try:
        subprocess.run(
            [soffice, "-env:UserInstallation=" + Path(profile).as_uri(), "--headless",
             "--convert-to", "pdf", "--outdir", work, pptx_path],
            check=True, timeout=240, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        print(f"[qa_render] fallo soffice: {exc}")
        return []
    pdf = os.path.join(work, base + ".pdf")
    if not os.path.isfile(pdf):
        pdfs = sorted(glob.glob(os.path.join(work, "*.pdf")), key=os.path.getmtime)
        if not pdfs:
            print("[qa_render] no se generó PDF")
            return []
        pdf = pdfs[-1]
    pngs = _raster_fitz(fitz, pdf, work, dpi) if fitz else []
    if not pngs and have_ppm:
        pngs = _raster_pdftoppm(pdf, work, dpi)
    rasterizer = "fitz" if fitz and pngs else "pdftoppm" if pngs else "ninguno"
    print(f"[qa_render] {len(pngs)} PNG(s) generados en {work} ({rasterizer})")
    return pngs


if __name__ == "__main__":
    import sys
    for path in render(sys.argv[1] if len(sys.argv) > 1 else ""):
        print(path)
