"""Padroniza as tabelas do Documento Técnico Final com os demais documentos da equipe.

Cabeçalho vermelho-escuro (#A52A2A) com texto branco em negrito e centralizado,
grade completa em todas as células, corpo em 10 pt e espaçamento simples.
Uso: python src/formatar_tabelas.py   (depois converta para PDF no Word ou LibreOffice)
"""
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ARQ = Path(__file__).resolve().parents[1] / "docs/TED04_Documento_Tecnico_Final_v4.0.docx"
COR = "A52A2A"


def bordas_tabela(tbl):
    tblPr = tbl._tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    b = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{lado}")
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:space"), "0"); e.set(qn("w:color"), "000000")
        b.append(e)
    tblPr.append(b)


def limpa_celula(tc):
    tcPr = tc.get_or_add_tcPr()
    for tag in ("w:tcBorders", "w:shd"):
        for old in tcPr.findall(qn(tag)):
            tcPr.remove(old)
    return tcPr


def sombreia(tcPr):
    s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), COR)
    tcPr.append(s)


def repete_cabecalho(row):
    trPr = row._tr.get_or_add_trPr()
    if trPr.find(qn("w:tblHeader")) is None:
        e = OxmlElement("w:tblHeader"); e.set(qn("w:val"), "true"); trPr.append(e)


d = Document(ARQ)
for t in d.tables:
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    bordas_tabela(t)
    for ri, row in enumerate(t.rows):
        for cell in row.cells:
            tcPr = limpa_celula(cell._tc)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for p in cell.paragraphs:
                pf = p.paragraph_format
                pf.line_spacing = 1.0; pf.space_before = Pt(0); pf.space_after = Pt(0); pf.first_line_indent = Pt(0)
                for r in p.runs:
                    r.font.size = Pt(10)
                    if ri == 0:
                        r.bold = True; r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                if ri == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if ri == 0:
                sombreia(tcPr)
        if ri == 0:
            repete_cabecalho(row)
d.save(ARQ)
print("tabelas formatadas:", len(d.tables))
