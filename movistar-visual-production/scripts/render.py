#!/usr/bin/env python3
"""
render.py: renderiza una pieza HTML (o SVG) a PNG para el bucle de verificacion visual.

El Art Director DEBE mirar el PNG resultante antes de entregar: es la unica forma
de detectar solapes de texto, jerarquia rota o composicion no-Movistar.

Backends, en orden de preferencia:
  1. playwright (python) si esta instalado
  2. chromium / chrome headless si esta en PATH
Si ninguno esta disponible, instala uno:
  pip install playwright --break-system-packages && python3 -m playwright install chromium

Uso:
  python3 scripts/render.py -i pieza.html -o pieza.png --width 1080 --height 1080
  python3 scripts/render.py -i email.html -o email.png --width 600            # altura = pagina completa
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def render_playwright(html: Path, out: Path, width: int, height: int | None) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height or 800})
        page.goto(html.resolve().as_uri())
        page.wait_for_timeout(500)  # fuentes embebidas
        page.screenshot(path=str(out), full_page=(height is None))
        browser.close()
    return True


def render_chrome(html: Path, out: Path, width: int, height: int | None) -> bool:
    exe = next((shutil.which(c) for c in
                ("chromium", "chromium-browser", "google-chrome", "chrome")
                if shutil.which(c)), None)
    if not exe:
        return False
    size = f"{width},{height or 1600}"
    cmd = [exe, "--headless=new", "--disable-gpu", "--no-sandbox",
           f"--screenshot={out.resolve()}", f"--window-size={size}",
           "--hide-scrollbars", html.resolve().as_uri()]
    subprocess.run(cmd, check=True, capture_output=True, timeout=60)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True)
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=None,
                    help="Si se omite, captura la pagina completa")
    args = ap.parse_args()

    html, out = Path(args.input), Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    for backend in (render_playwright, render_chrome):
        try:
            if backend(html, out, args.width, args.height):
                print(f"OK: {out} ({out.stat().st_size // 1024} KB)")
                return
        except Exception as e:
            print(f"AVISO: {backend.__name__} fallo: {e}", file=sys.stderr)

    sys.exit("ERROR: ningun backend de render disponible. Instala playwright:\n"
             "  pip install playwright --break-system-packages && python3 -m playwright install chromium")


if __name__ == "__main__":
    main()
