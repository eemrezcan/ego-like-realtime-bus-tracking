from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, StyleSheet1, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


REPO_ROOT = Path(__file__).resolve().parent
INPUT_PATH = REPO_ROOT / "REPORT_PREVIEW.md"
OUTPUT_PATH = REPO_ROOT.parent / "final-report.pdf"


def register_fonts() -> None:
    candidates = {
        "Arial": Path(r"C:\Windows\Fonts\arial.ttf"),
        "Arial-Bold": Path(r"C:\Windows\Fonts\arialbd.ttf"),
        "Arial-Italic": Path(r"C:\Windows\Fonts\ariali.ttf"),
        "Arial-BoldItalic": Path(r"C:\Windows\Fonts\arialbi.ttf"),
    }
    for name, path in candidates.items():
        if path.exists():
            pdfmetrics.registerFont(TTFont(name, str(path)))

    pdfmetrics.registerFontFamily(
        "Arial",
        normal="Arial",
        bold="Arial-Bold",
        italic="Arial-Italic",
        boldItalic="Arial-BoldItalic",
    )


def parse_sections(lines: list[str]) -> tuple[str, list[str], list[tuple[str, list[str]]]]:
    title = ""
    cover_items: list[str] = []
    sections: list[tuple[str, list[str]]] = []

    current_section: str | None = None
    current_lines: list[str] = []
    started = False

    for raw_line in lines:
        line = raw_line.rstrip("\n")

        if not started:
            if line.strip() == "## Baslik":
                started = True
                current_section = "Baslik"
            continue

        if line.startswith("## "):
            if current_section == "Baslik":
                title = "\n".join(x for x in current_lines if x.strip()).strip()
            elif current_section == "Kapak Bilgileri":
                cover_items = [x[2:].strip() for x in current_lines if x.startswith("- ")]
            elif current_section:
                sections.append((current_section, current_lines[:]))

            current_section = line[3:].strip()
            current_lines = []
            continue

        current_lines.append(line)

    if current_section == "Baslik":
        title = "\n".join(x for x in current_lines if x.strip()).strip()
    elif current_section == "Kapak Bilgileri":
        cover_items = [x[2:].strip() for x in current_lines if x.startswith("- ")]
    elif current_section:
        sections.append((current_section, current_lines[:]))

    return title, cover_items, sections


def make_styles() -> StyleSheet1:
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CoverLabel",
            parent=styles["Normal"],
            fontName="Arial",
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#666666"),
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Normal"],
            fontName="Arial-Bold",
            fontSize=22,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.black,
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSubtitle",
            parent=styles["Normal"],
            fontName="Arial",
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#444444"),
            spaceAfter=20,
        )
    )
    styles.add(
        ParagraphStyle(
            name="MetaKey",
            parent=styles["Normal"],
            fontName="Arial-Bold",
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="MetaValue",
            parent=styles["Normal"],
            fontName="Arial",
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading1"],
            fontName="Arial-Bold",
            fontSize=15,
            leading=19,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceBefore=8,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyTextCustom",
            parent=styles["BodyText"],
            fontName="Arial",
            fontSize=10.5,
            leading=15,
            alignment=TA_JUSTIFY,
            spaceAfter=7,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ListItem",
            parent=styles["BodyText"],
            fontName="Arial",
            fontSize=10.5,
            leading=15,
            alignment=TA_LEFT,
            leftIndent=16,
            firstLineIndent=-10,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TocItem",
            parent=styles["BodyText"],
            fontName="Arial",
            fontSize=11,
            leading=16,
            alignment=TA_LEFT,
            leftIndent=10,
            spaceAfter=7,
        )
    )
    return styles


def to_para_markup(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', escaped)

    def repl(match: re.Match[str]) -> str:
        label = html.escape(match.group(1))
        href = html.escape(match.group(2), quote=True)
        return f'<link href="{href}">{label}</link>'

    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, escaped)
    return escaped


def add_footer(canvas, doc) -> None:
    if doc.page == 1:
        return
    canvas.saveState()
    canvas.setFont("Arial", 9)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawCentredString(A4[0] / 2, 10 * mm, str(doc.page - 1))
    canvas.restoreState()


def build_story(title: str, cover_items: list[str], sections: list[tuple[str, list[str]]], styles: StyleSheet1):
    abstract_lines: list[str] = []
    keyword_items: list[str] = []
    content_sections: list[tuple[str, list[str]]] = []

    for section_title, section_lines in sections:
        if section_title == "Ozet":
            abstract_lines = [x.strip() for x in section_lines if x.strip()]
        elif section_title == "Anahtar Kelimeler":
            keyword_items = [x[2:].strip() for x in section_lines if x.strip().startswith("- ")]
        elif section_title == "Icindekiler":
            continue
        else:
            content_sections.append((section_title, section_lines))

    story = []

    # Cover
    story.append(Spacer(1, 28 * mm))
    story.append(Paragraph("Final Proje Raporu", styles["CoverLabel"]))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(to_para_markup(title), styles["CoverTitle"]))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("Gerçek Zamanlı Bulut Tabanlı Uygulama Çalışması", styles["CoverSubtitle"]))
    story.append(Spacer(1, 8 * mm))
    story.append(HRFlowable(width="90%", thickness=1.4, color=colors.HexColor("#333333")))
    story.append(Spacer(1, 7 * mm))

    rows = []
    for item in cover_items:
        if ":" in item:
            key, value = item.split(":", 1)
            rows.append(
                [
                    Paragraph(to_para_markup(key.strip()), styles["MetaKey"]),
                    Paragraph(to_para_markup(value.strip()), styles["MetaValue"]),
                ]
            )
    meta_table = Table(rows, colWidths=[55 * mm, 110 * mm])
    meta_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 7 * mm))
    story.append(HRFlowable(width="90%", thickness=1.4, color=colors.HexColor("#333333")))
    story.append(Spacer(1, 18 * mm))
    story.append(Paragraph("Ankara, 2026", styles["CoverSubtitle"]))
    story.append(PageBreak())

    # Abstract + keywords
    story.append(Paragraph("Özet", styles["SectionHeading"]))
    for line in abstract_lines:
        story.append(Paragraph(to_para_markup(line), styles["BodyTextCustom"]))
    if keyword_items:
        story.append(Spacer(1, 5 * mm))
        story.append(Paragraph("Anahtar Kelimeler", styles["SectionHeading"]))
        story.append(
            Paragraph(
                to_para_markup(", ".join(keyword_items)),
                styles["BodyTextCustom"],
            )
        )
    story.append(PageBreak())

    # TOC
    story.append(Paragraph("İçindekiler", styles["SectionHeading"]))
    for idx, (section_title, _) in enumerate(content_sections, start=1):
        story.append(Paragraph(f"{idx}. {to_para_markup(section_title)}", styles["TocItem"]))
    story.append(PageBreak())

    # Main content
    for idx, (section_title, section_lines) in enumerate(content_sections, start=1):
        story.append(Paragraph(f"{idx}. {to_para_markup(section_title)}", styles["SectionHeading"]))
        in_ul = False
        in_ol = False
        order = 1

        for raw_line in section_lines:
            line = raw_line.strip()
            if not line:
                story.append(Spacer(1, 2 * mm))
                in_ul = False
                in_ol = False
                order = 1
                continue

            if re.match(r"^\d+\.\s+", line):
                item_text = re.sub(r"^\d+\.\s+", "", line)
                story.append(Paragraph(f"{order}. {to_para_markup(item_text)}", styles["ListItem"]))
                order += 1
                in_ol = True
                in_ul = False
                continue

            if line.startswith("- "):
                story.append(Paragraph(f"• {to_para_markup(line[2:].strip())}", styles["ListItem"]))
                in_ul = True
                in_ol = False
                continue

            if in_ol:
                order = 1
                in_ol = False
            in_ul = False
            story.append(Paragraph(to_para_markup(line), styles["BodyTextCustom"]))

        story.append(Spacer(1, 3 * mm))

    return story


def main() -> None:
    register_fonts()
    styles = make_styles()
    lines = INPUT_PATH.read_text(encoding="utf-8").splitlines()
    title, cover_items, sections = parse_sections(lines)

    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=title,
        author="Ahmet Emre Özcan",
    )

    story = build_story(title, cover_items, sections, styles)
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"PDF olusturuldu: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
