#!/usr/bin/env python3
"""
verify_pptx.py — Validación OPC DETERMINISTA de un .pptx ANTES de empaquetar/entregar.

Por qué existe: PowerPoint rechaza ("encontró un problema con el contenido" / "Reparar")
paquetes que python-pptx y `unzip` aceptan. Los fallos reales observados en producción:

  1. Referencias `r:id` COLGANTES en ppt/presentation.xml (slideMaster/notesMaster/
     handoutMaster/fonts) cuando el código reescribe presentation.xml.rels desde cero al
     borrar slides. → quita TODO menos las slides; PowerPoint rechaza.
  2. notesSlides HUÉRFANAS (su slide ya no existe).
  3. docProps/app.xml con <Slides> distinto del nº real de <p:sldId>.
  4. Cualquier .rels apuntando a una parte inexistente.
  5. Overrides de [Content_Types].xml a partes inexistentes / sin cobertura de partes.
  6. notesSlide COMPARTIDA por 2+ slides. Cada notesSlideN.xml trae su PROPIA relación de
     vuelta a su slide padre (tipo `.../relationships/slide`) — si dos slides distintas
     también se relacionan con ese mismo notesSlide (típico al clonar una slide sin excluir
     su relación notesSlide), esa notesSlide "resucita" al slide original que ya se había
     borrado de sldIdLst: python-pptx lo vuelve a considerar alcanzable y lo re-empaqueta.
     Encontrado en producción real (alhambra-pptx, motor de clonado de slides), portado a
     san-miguel-pptx (2026-07-21) y de ahí aquí (2026-07-23, rediseño a modelo de clonado
     de slides) porque `mvst_pptx.py` clona slides con el mismo mecanismo (`use()`/
     `_duplicate_slide()`) y por tanto puede reproducir el mismo bug.
  7. Partes `ppt/slides/slideN.xml` físicamente presentes en el zip pero NO referenciadas
     por ningún `<p:sldId>` de presentation.xml — síntoma del mismo problema que 6 (o de
     cualquier borrado de slide incompleto): no siempre invalida el fichero por sí solo,
     pero es la señal de alarma que en la práctica coincidió exactamente con 6.

Los tres siguientes se añadieron con el rebuild BI-MASTER (v4.0.0, `opc_merge.py`), porque
fusionar dos paquetes reales abre fallos que ninguno de los anteriores veía:

  8. Identificadores DUPLICADOS o fuera de rango: `<p:sldId>`, `<p:sldMasterId>` y
     `<p:sldLayoutId>`. Los dos ficheros del cliente usaban el MISMO rango de `sldId`
     (2147483516-2147483572), así que un merge ingenuo produce ids repetidos: PowerPoint
     "repara" el fichero perdiendo diapositivas y no da ninguna pista de por qué. Se validan
     además los rangos legales de ECMA-376 §19.7 (`ST_SlideId` 256..2147483647;
     `ST_SlideMasterId`/`ST_SlideLayoutId` >= 2147483648) y la no-colisión entre master y
     layout, que comparten rango.
  9. Cobertura COMPLETA de `[Content_Types].xml`: toda parte del zip tiene un `Default` por
     extensión o un `Override` explícito. El fallo real: `[Content_Types].xml` del v9 no
     declara `Default Extension="jpg"` y el refresh aporta 7 `.jpg` — PowerPoint pide
     "Reparar" sin más diagnóstico.
 10. TODO atributo del espacio de nombres de relaciones (`r:id`, `r:embed`, `r:link`,
     `r:pict`, `r:href`, y `r:dm`/`r:lo`/`r:qs`/`r:cs` de `<c:chart>`/`<c:externalData>`)
     resuelve a un `Id` presente en el `.rels` de ESA MISMA parte. Un remapeo de fusión que
     solo cubra `id/embed/link` rompe los charts en silencio: el fichero abre, pero el
     gráfico aparece vacío o con los datos de otro.

Uso:
    python scripts/verify_pptx.py <archivo.pptx>

Sale con código 0 si TODO es válido; 1 si hay algún defecto (imprime el detalle).
Ejecútalo SIEMPRE antes de emitir OUTPUT_FILE. Si falla, ARREGLA y vuelve a validar.
NO entregues un .pptx que no pase esta verificación.
"""
import sys
import re
import posixpath
import zipfile
from xml.dom.minidom import parseString


def _resolve(base_part_dir: str, target: str) -> str:
    """Resuelve un Target de .rels (relativo a la carpeta de la parte) a ruta normalizada."""
    if target.startswith("/"):
        return target.lstrip("/")
    parts = (base_part_dir + "/" + target).split("/") if base_part_dir else target.split("/")
    out = []
    for p in parts:
        if p == "..":
            if out:
                out.pop()
        elif p not in ("", "."):
            out.append(p)
    return "/".join(out)


def verify(path: str) -> list:
    errors = []
    try:
        z = zipfile.ZipFile(path)
    except Exception as e:
        return [f"No es un ZIP/OPC válido: {e}"]

    names = set(z.namelist())

    # 0. Partes core
    for core in ("[Content_Types].xml", "ppt/presentation.xml", "ppt/_rels/presentation.xml.rels"):
        if core not in names:
            errors.append(f"Falta parte core: {core}")
    if errors:
        return errors

    # XML bien formado en todas las partes .xml/.rels
    for n in names:
        if n.endswith(".xml") or n.endswith(".rels"):
            try:
                parseString(z.read(n))
            except Exception as e:
                errors.append(f"XML malformado en {n}: {str(e)[:120]}")

    # 1+4. Cada .rels: targets internos resuelven; ids no duplicados
    rels_ids = {}  # part -> set(Id)
    for n in names:
        if not n.endswith(".rels"):
            continue
        data = z.read(n).decode("utf-8", "replace")
        base_dir = posixpath.dirname(posixpath.dirname(n))  # carpeta de la parte dueña
        ids = re.findall(r'Id="([^"]+)"', data)
        for i in set(ids):
            if ids.count(i) > 1:
                errors.append(f"Id de relación duplicado '{i}' en {n}")
        # mapear part dueña -> sus Ids
        owner = posixpath.join(base_dir, posixpath.basename(n)[:-5]) if base_dir else posixpath.basename(n)[:-5]
        rels_ids[owner] = set(ids)
        for m in re.finditer(r"<Relationship\b[^>]*?/>", data):
            tag = m.group(0)
            if 'TargetMode="External"' in tag:
                continue
            tm = re.search(r'Target="([^"]+)"', tag)
            if not tm:
                continue
            resolved = _resolve(base_dir, tm.group(1))
            if resolved not in names:
                errors.append(f"Rel rota en {n}: Target='{tm.group(1)}' -> {resolved} (no existe)")

    # 1b. <p:ph> con type INVÁLIDO por esquema (causa #1: PowerPoint rechaza el fichero entero).
    # type debe ser un enum (ctrTitle/subTitle/title/body/pic/chart/tbl/...) SIN coma ni idx
    # dentro. El idx va como atributo separado: <p:ph type="body" idx="1"/>. El bug típico de la
    # construcción manual es <p:ph type="body,idx:1"/> (XML bien formado pero esquema inválido).
    VALID_PH_TYPES = {
        "title", "body", "ctrTitle", "subTitle", "dt", "sldNum", "ftr", "hdr",
        "obj", "chart", "tbl", "clipArt", "dgm", "media", "sldImg", "pic",
    }
    for n in names:
        if not re.match(r"ppt/slides/slide\d+\.xml$", n):
            continue
        xml = z.read(n).decode("utf-8", "replace")
        for ph in re.findall(r"<p:ph\b[^>]*>", xml):
            tm = re.search(r'type="([^"]*)"', ph)
            if tm and tm.group(1) not in VALID_PH_TYPES:
                errors.append(f"{n}: <p:ph> con type INVALIDO '{tm.group(1)}' "
                              f"(usa type=\"<enum>\" idx=\"<n>\" como atributos separados)")

    # 2. notesSlides huérfanas
    existing_slides = {n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)}
    for n in names:
        m = re.match(r"ppt/notesSlides/_rels/notesSlide(\d+)\.xml\.rels$", n)
        if not m:
            continue
        data = z.read(n).decode("utf-8", "replace")
        sm = re.search(r'Target="\.\./slides/(slide\d+\.xml)"', data)
        if sm and f"ppt/slides/{sm.group(1)}" not in existing_slides:
            errors.append(f"notesSlide huérfana: notesSlide{m.group(1)} apunta a {sm.group(1)} inexistente")

    # 3. r:id de presentation.xml deben existir en presentation.xml.rels
    pres = z.read("ppt/presentation.xml").decode("utf-8", "replace")
    pres_ids = rels_ids.get("ppt/presentation.xml", set())
    for rid in set(re.findall(r'r:(?:id|embed|link)="([^"]+)"', pres)):
        if rid not in pres_ids:
            errors.append(f"presentation.xml referencia r:id '{rid}' que NO está en presentation.xml.rels")

    # 5. docProps/app.xml <Slides> == nº de <p:sldId>
    n_sld = len(re.findall(r"<p:sldId\b", pres))
    if "docProps/app.xml" in names:
        app = z.read("docProps/app.xml").decode("utf-8", "replace")
        ms = re.search(r"<Slides>(\d+)</Slides>", app)
        if ms and int(ms.group(1)) != n_sld:
            errors.append(f"docProps/app.xml <Slides>={ms.group(1)} != nº real de slides ({n_sld})")

    # 6b. notesSlide compartida por 2+ slides (ver docstring, defecto real de producción)
    notes_targets = {}  # notesSlideN.xml (ruta resuelta) -> [slides que se relacionan con ella]
    for n in names:
        m = re.match(r"ppt/slides/_rels/(slide\d+\.xml)\.rels$", n)
        if not m:
            continue
        base_dir = "ppt/slides"
        data = z.read(n).decode("utf-8", "replace")
        for rm in re.finditer(r'<Relationship\b[^>]*Type="[^"]*?/notesSlide"[^>]*/>', data):
            tm = re.search(r'Target="([^"]+)"', rm.group(0))
            if tm:
                resolved = _resolve(base_dir, tm.group(1))
                notes_targets.setdefault(resolved, []).append(f"ppt/slides/{m.group(1)}")
    for target, owners in notes_targets.items():
        if len(owners) > 1:
            errors.append(f"notesSlide compartida: {target} referenciada por {len(owners)} slides {owners} "
                           f"(cada notesSlide debe pertenecer a una única slide)")

    # 6c. chart COMPARTIDO por 2+ slides (§G34). Hermano del check de arriba, y del mismo tipo de
    #     defecto: una parte con estado propio que acaba compartida entre clones. Un `chartN.xml`
    #     lleva sus DATOS dentro, así que si dos diapositivas apuntan al mismo, la segunda llamada
    #     a `set_chart_data()` destruye los números de la primera EN SILENCIO — el deck se entrega
    #     con las dos gráficas mostrando los datos de la última. Compartir un media part de imagen
    #     sí es correcto (blob de solo lectura); compartir una gráfica nunca lo es.
    chart_targets = {}
    for n in names:
        m = re.match(r"ppt/slides/_rels/(slide\d+\.xml)\.rels$", n)
        if not m:
            continue
        data = z.read(n).decode("utf-8", "replace")
        for rm in re.finditer(r'<Relationship\b[^>]*Type="[^"]*?/chart"[^>]*/>', data):
            tm = re.search(r'Target="([^"]+)"', rm.group(0))
            if tm:
                resolved = _resolve("ppt/slides", tm.group(1))
                chart_targets.setdefault(resolved, []).append(f"ppt/slides/{m.group(1)}")
    for target, owners in chart_targets.items():
        if len(owners) > 1:
            errors.append(
                f"chart compartido: {target} referenciada por {len(owners)} slides {owners} — "
                f"cada gráfica lleva sus propios datos, así que set_chart_data() en una "
                f"sobrescribiría los datos de la otra sin avisar (§G34)"
            )

    # 7. slides físicamente presentes pero no alcanzables desde presentation.xml (huérfanas)
    referenced_slide_targets = set()
    pres_rels_data = ""
    if "ppt/_rels/presentation.xml.rels" in names:
        pres_rels_data = z.read("ppt/_rels/presentation.xml.rels").decode("utf-8", "replace")
        for rm in re.finditer(r'<Relationship\b[^>]*Type="[^"]*?/slide"[^>]*/>', pres_rels_data):
            tm = re.search(r'Target="([^"]+)"', rm.group(0))
            if tm:
                referenced_slide_targets.add(_resolve("ppt", tm.group(1)))
    physical_slides = {n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)}
    orphaned = physical_slides - referenced_slide_targets
    if orphaned:
        errors.append(f"{len(orphaned)} parte(s) ppt/slides/*.xml presentes en el zip pero NO "
                       f"referenciadas desde presentation.xml (huérfanas): {sorted(orphaned)}")

    # 6/9. Content_Types: Overrides a partes existentes + cobertura de TODAS las partes.
    # (Los PartName se normalizan sin la barra inicial: hay paquetes en circulación que la
    # omiten — es inválido por spec, pero no debe provocar un falso positivo de cobertura.)
    ct = z.read("[Content_Types].xml").decode("utf-8", "replace")
    defaults = {e.lower() for e in re.findall(r'<Default\b[^>]*?\sExtension="([^"]+)"', ct)}
    overrides = {p.lstrip("/") for p in re.findall(r'<Override\b[^>]*?\sPartName="([^"]+)"', ct)}
    for ov in sorted(overrides):
        if ov not in names:
            errors.append(f"Content_Types Override a parte inexistente: /{ov}")
    for n in sorted(names):
        if n.endswith("/") or n == "[Content_Types].xml":
            continue
        ext = n.rsplit(".", 1)[-1].lower() if "." in n else ""
        if ext not in defaults and n not in overrides:
            errors.append(
                f"Parte sin cobertura en Content_Types: {n} "
                f"(ni Default Extension=\"{ext}\" ni Override explicito)"
            )

    # 8. Identificadores unicos y dentro de rango (ECMA-376 19.7). Fallo #1 de una fusion de
    # dos paquetes: ambos originales usaban el mismo rango de sldId.
    errors.extend(_check_ids(z, names, pres))

    # 10. Todo atributo de la namespace de relaciones resuelve en el .rels de SU parte.
    errors.extend(_check_rel_refs(z, names, rels_ids))

    return errors


# --- helpers de los checks 8 y 10 (rebuild bi-master) ----------------------------------
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

# Rangos legales. sldId es el unico que NO vive en el espacio alto.
SLD_ID_MIN, SLD_ID_MAX = 256, 2147483647
HIGH_ID_MIN, HIGH_ID_MAX = 2147483648, 4294967295


def _ids_of(xml: str, tag: str) -> list:
    """Valores de @id de todos los <p:TAG .../> del XML, en orden de documento."""
    out = []
    for m in re.finditer(r"<p:%s\b[^>]*>" % tag, xml):
        im = re.search(r'\sid="(\d+)"', m.group(0))
        if im:
            out.append(int(im.group(1)))
    return out


def _dupes(values) -> list:
    seen, dup = set(), []
    for v in values:
        if v in seen and v not in dup:
            dup.append(v)
        seen.add(v)
    return dup


def _check_ids(z, names, pres) -> list:
    errors = []

    sld_ids = _ids_of(pres, "sldId")
    master_ids = _ids_of(pres, "sldMasterId")

    layout_ids = []          # (id, parte) para poder senalar donde esta el duplicado
    for n in sorted(names):
        if not re.match(r"ppt/slideMasters/slideMaster\d+\.xml$", n):
            continue
        xml = z.read(n).decode("utf-8", "replace")
        for lid in _ids_of(xml, "sldLayoutId"):
            layout_ids.append((lid, n))

    for label, values in (("sldId", sld_ids), ("sldMasterId", master_ids),
                          ("sldLayoutId", [i for i, _ in layout_ids])):
        d = _dupes(values)
        if d:
            errors.append(
                f"{label} DUPLICADO(S) {d} — PowerPoint 'repara' el fichero y pierde partes "
                f"(sintoma clasico de fusionar dos paquetes sin renumerar)"
            )

    for i in sld_ids:
        if not (SLD_ID_MIN <= i <= SLD_ID_MAX):
            errors.append(f"sldId {i} fuera del rango legal [{SLD_ID_MIN}, {SLD_ID_MAX}]")
    for i in master_ids:
        if not (HIGH_ID_MIN <= i <= HIGH_ID_MAX):
            errors.append(f"sldMasterId {i} fuera del rango legal [{HIGH_ID_MIN}, {HIGH_ID_MAX}]")
    for i, part in layout_ids:
        if not (HIGH_ID_MIN <= i <= HIGH_ID_MAX):
            errors.append(f"sldLayoutId {i} ({part}) fuera del rango legal "
                          f"[{HIGH_ID_MIN}, {HIGH_ID_MAX}]")

    cross = sorted(set(master_ids) & {i for i, _ in layout_ids})
    if cross:
        errors.append(f"sldMasterId y sldLayoutId comparten identificador(es) {cross} "
                      f"(ambos viven en el mismo rango; deben ser unicos entre si)")
    return errors


def _check_rel_refs(z, names, rels_ids) -> list:
    """Cada r:* de cada parte debe existir en el .rels de esa misma parte.

    Se resuelve el PREFIJO real ligado a la namespace de relaciones en cada documento (casi
    siempre 'r', pero no es obligatorio) en vez de asumirlo, y se aceptan TODOS los nombres
    locales — no solo id/embed/link — para cubrir r:dm/lo/qs/cs de los graficos.
    """
    errors = []
    for n in sorted(names):
        if not n.endswith(".xml") or n.endswith(".rels"):
            continue
        xml = z.read(n).decode("utf-8", "replace")
        prefixes = set(re.findall(
            r'xmlns:([A-Za-z_][\w.\-]*)="%s"' % re.escape(REL_NS), xml))
        if not prefixes:
            continue
        ids = rels_ids.get(n, set())
        pat = re.compile(r'\b(?:%s):([A-Za-z_][\w.\-]*)="([^"]*)"'
                         % "|".join(sorted(re.escape(p) for p in prefixes)))
        bad = {}
        for local, value in pat.findall(xml):
            if not value or value in ids:
                continue
            bad.setdefault(f"{local}={value}", 0)
            bad[f"{local}={value}"] += 1
        for ref, count in sorted(bad.items()):
            errors.append(
                f"{n}: r:{ref} no existe en su propio .rels"
                + (f" (x{count})" if count > 1 else "")
            )
    return errors


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # consolas no-UTF8 (Windows cp1252)
    except Exception:
        pass
    if len(sys.argv) != 2:
        print("Uso: python scripts/verify_pptx.py <archivo.pptx>", file=sys.stderr)
        sys.exit(2)
    errors = verify(sys.argv[1])
    if errors:
        print(f"[FAIL] verify_pptx: {len(errors)} defecto(s) - NO entregar:")
        for e in errors:
            print("   -", e)
        sys.exit(1)
    print("[OK] verify_pptx: OPC valido (sin refs colgantes, rels resueltas, app.xml coherente).")
    sys.exit(0)


if __name__ == "__main__":
    main()
