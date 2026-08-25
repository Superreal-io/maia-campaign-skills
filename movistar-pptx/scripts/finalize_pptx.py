#!/usr/bin/env python3
"""
finalize_pptx.py — Paso FINAL tras `prs.save()`, antes de entregar.

python-pptx NO actualiza docProps/app.xml al guardar, así que <Slides>, el par
"Títulos de diapositiva" y <TitlesOfParts> quedan desfasados respecto al deck real. PowerPoint
muestra "Reparar" ante ese desajuste (Bug A histórico de la skill). Este script los regenera de
forma determinista a partir del estado real del paquete (sin tocar nada estructural del OOXML).

Hace, sobre el .pptx ya guardado por python-pptx:
  - <Slides> = nº real de <p:sldId> en ppt/presentation.xml.
  - <Notes>  = nº real de notesSlides.
  - HeadingPairs "Títulos de diapositiva" i4 = nº de slides.
  - <TitlesOfParts> = [entradas no-slide (fuentes+tema) existentes] + [títulos reales por slide].
  - Conserva el resto de app.xml intacto.

Uso:  python scripts/finalize_pptx.py <archivo.pptx>
Reescribe el .pptx in place. Después ejecuta verify_pptx.py.
"""
import sys
import re
import zipfile
import shutil
import tempfile
import os
from xml.sax.saxutils import escape


def _slide_order_and_titles(z):
    """Devuelve [titulo_por_slide] en el orden de sldIdLst."""
    pres = z.read("ppt/presentation.xml").decode("utf-8", "replace")
    rels = z.read("ppt/_rels/presentation.xml.rels").decode("utf-8", "replace")
    relmap = dict(re.findall(r'Id="([^"]+)"[^>]*?Target="([^"]+)"', rels))
    rids = re.findall(r'<p:sldId\b[^>]*r:id="([^"]+)"', pres)
    titles = []
    for rid in rids:
        tgt = relmap.get(rid, "")
        part = "ppt/" + tgt.replace("../", "") if tgt else None
        title = " "
        if part and part in z.namelist():
            sxml = z.read(part).decode("utf-8", "replace")
            # primer placeholder title/ctrTitle -> su texto concatenado
            for sp in re.findall(r"<p:sp>.*?</p:sp>", sxml, re.S):
                phm = re.search(r'<p:ph\b[^>]*type="(title|ctrTitle)"', sp)
                if phm:
                    txt = "".join(re.findall(r"<a:t>(.*?)</a:t>", sp, re.S))
                    if txt.strip():
                        title = txt.strip()
                    break
        titles.append(title)
    return titles


def finalize(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    if "docProps/app.xml" not in names:
        z.close()
        return  # nada que hacer
    titles = _slide_order_and_titles(z)
    n_slides = len(titles)
    n_notes = len([n for n in names if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", n)])
    app = z.read("docProps/app.xml").decode("utf-8", "replace")
    data = {n: z.read(n) for n in names}
    z.close()

    # <Slides> y <Notes>
    app = re.sub(r"<Slides>\d+</Slides>", f"<Slides>{n_slides}</Slides>", app)
    if "<Notes>" in app:
        app = re.sub(r"<Notes>\d+</Notes>", f"<Notes>{n_notes}</Notes>", app)

    # HeadingPairs: leer pares (label, count); detectar el de "diapositiva"/"Slide"
    hp = re.search(r"<HeadingPairs>.*?</HeadingPairs>", app, re.S)
    leading = 0
    if hp:
        variants = re.findall(r"<vt:variant>(.*?)</vt:variant>", hp.group(0), re.S)
        labels, counts = [], []
        for v in variants:
            lm = re.search(r"<vt:lpstr>(.*?)</vt:lpstr>", v, re.S)
            im = re.search(r"<vt:i4>(\d+)</vt:i4>", v)
            if lm is not None:
                labels.append(lm.group(1))
            elif im is not None:
                counts.append(int(im.group(1)))
        # sumar counts cuyo label NO es de slides
        new_counts = []
        for lbl, cnt in zip(labels, counts):
            if "diapositiva" in lbl.lower() or "slide" in lbl.lower():
                new_counts.append(n_slides)
            else:
                new_counts.append(cnt)
                leading += cnt
        # reconstruir HeadingPairs preservando labels
        pairs = "".join(
            f"<vt:variant><vt:lpstr>{escape(lbl)}</vt:lpstr></vt:variant>"
            f"<vt:variant><vt:i4>{cnt}</vt:i4></vt:variant>"
            for lbl, cnt in zip(labels, new_counts)
        )
        new_hp = f'<HeadingPairs><vt:vector size="{len(labels)*2}" baseType="variant">{pairs}</vt:vector></HeadingPairs>'
        app = app[: hp.start()] + new_hp + app[hp.end():]

    # TitlesOfParts: [leading lpstr existentes] + [titulos de slide]
    top = re.search(r"<TitlesOfParts>.*?</TitlesOfParts>", app, re.S)
    if top:
        existing = re.findall(r"<vt:lpstr>(.*?)</vt:lpstr>", top.group(0), re.S)
        head = existing[:leading]
        entries = head + titles
        body = "".join(f"<vt:lpstr>{escape(t)}</vt:lpstr>" for t in entries)
        new_top = f'<TitlesOfParts><vt:vector size="{len(entries)}" baseType="lpstr">{body}</vt:vector></TitlesOfParts>'
        app = app[: top.start()] + new_top + app[top.end():]

    data["docProps/app.xml"] = app.encode("utf-8")

    # reescribir el .pptx (Content_Types primero)
    items = sorted(data.items(), key=lambda kv: kv[0] != "[Content_Types].xml")
    fd, tmp = tempfile.mkstemp(suffix=".pptx")
    os.close(fd)
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for n, b in items:
            out.writestr(n, b)
    shutil.move(tmp, path)
    print(f"[finalize] app.xml actualizado: Slides={n_slides} Notes={n_notes} titulos={n_slides}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python scripts/finalize_pptx.py <archivo.pptx>", file=sys.stderr)
        sys.exit(2)
    finalize(sys.argv[1])
