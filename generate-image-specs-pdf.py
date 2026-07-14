#!/usr/bin/env python3
"""Generate designer image size specification PDF for Rajasthan Marbles site."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).resolve().parent / "Rajasthan-Marbles-Image-Size-Specs.pdf"

INK = colors.HexColor("#0B0A09")
CRIMSON = colors.HexColor("#C92140")
GOLD = colors.HexColor("#C9A24A")
BEIGE = colors.HexColor("#E9DEBC")
FOG = colors.HexColor("#5A5248")
LINE = colors.HexColor("#D9D0C0")
ROW_ALT = colors.HexColor("#F7F3EA")
HEADER_BG = colors.HexColor("#17130F")
WHITE = colors.white


def styles():
    base = getSampleStyleSheet()
    return {
        "cover_brand": ParagraphStyle(
            "cover_brand",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=GOLD,
            alignment=TA_CENTER,
            letterSpacing=3,
            spaceAfter=8,
        ),
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=28,
            textColor=INK,
            alignment=TA_CENTER,
            leading=34,
            spaceAfter=10,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            textColor=FOG,
            alignment=TA_CENTER,
            leading=16,
            spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=16,
            textColor=INK,
            spaceBefore=4,
            spaceAfter=8,
            leading=20,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            textColor=CRIMSON,
            spaceBefore=12,
            spaceAfter=6,
            leading=15,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            textColor=FOG,
            leading=13,
            spaceAfter=6,
        ),
        "note": ParagraphStyle(
            "note",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8.5,
            textColor=FOG,
            leading=12,
            spaceAfter=8,
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            textColor=INK,
            leading=11,
        ),
        "cell_bold": ParagraphStyle(
            "cell_bold",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=INK,
            leading=11,
        ),
        "th": ParagraphStyle(
            "th",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            textColor=BEIGE,
            leading=10,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            textColor=FOG,
            alignment=TA_CENTER,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            textColor=FOG,
            leading=13,
            leftIndent=12,
            spaceAfter=3,
        ),
    }


def p(text, style):
    return Paragraph(str(text), style)


def make_table(headers, rows, col_widths, s):
    data = [[p(h, s["th"]) for h in headers]]
    for row in rows:
        cells = []
        for i, val in enumerate(row):
            style = s["cell_bold"] if i in (0, 3) else s["cell"]
            cells.append(p(val, style))
        data.append(cells)

    table = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), BEIGE),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("BOX", (0, 0), (-1, -1), 0.8, INK),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    table.setStyle(TableStyle(style_cmds))
    return table


def section(title, intro, headers, rows, col_widths, s, extra=None):
    bits = [p(title, s["h2"]), p(intro, s["body"]), make_table(headers, rows, col_widths, s)]
    if extra:
        bits.append(Spacer(1, 4))
        bits.append(p(extra, s["note"]))
    bits.append(Spacer(1, 6))
    return KeepTogether(bits)


def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    y = 12 * mm
    canvas.line(18 * mm, y + 6, A4[0] - 18 * mm, y + 6)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(FOG)
    canvas.drawString(18 * mm, y, "Rajasthan Marbles — Image Size Specs for Designers")
    canvas.drawRightString(A4[0] - 18 * mm, y, f"Page {doc.page}")
    canvas.restoreState()


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=18 * mm,
        title="Rajasthan Marbles — Image Size Specifications",
        author="Rajasthan Marbles",
        subject="Designer image size documentation for all website pages",
    )

    W = A4[0] - 32 * mm
    # Column presets
    c5 = [W * 0.22, W * 0.10, W * 0.24, W * 0.22, W * 0.22]
    c4 = [W * 0.28, W * 0.14, W * 0.28, W * 0.30]
    c3 = [W * 0.34, W * 0.33, W * 0.33]
    headers5 = ["Slot", "Qty", "Display (CSS)", "Export W×H", "Ratio / Notes"]
    headers4 = ["Slot", "Qty", "Export W×H", "Notes"]

    story = []

    # Cover
    story.append(Spacer(1, 40 * mm))
    story.append(p("RAJASTHAN MARBLES", s["cover_brand"]))
    story.append(p("Website Image Size<br/>Specifications", s["cover_title"]))
    story.append(Spacer(1, 4 * mm))
    story.append(
        p(
            "Designer handoff document — banners, heroes, cards &amp; gallery sizes<br/>"
            "for every page on the site.",
            s["cover_sub"],
        )
    )
    story.append(Spacer(1, 8 * mm))
    story.append(
        p(
            "Content shell: <b>1280px</b> &nbsp;|&nbsp; Crop: <b>cover / center</b> &nbsp;|&nbsp; "
            "Color: <b>sRGB</b> &nbsp;|&nbsp; Prefer <b>2× retina</b> exports",
            s["cover_sub"],
        )
    )
    story.append(Spacer(1, 10 * mm))
    story.append(
        p(
            "<b>Important:</b> The project currently has no image files on disk. "
            "Most visuals are CSS textures. Only these filenames are referenced in code: "
            "<b>rm-living.jpg</b>, <b>rm-kitchen.jpg</b>, <b>rm-bathroom.jpg</b>.",
            s["note"],
        )
    )
    story.append(PageBreak())

    # Global rules
    story.append(p("1. Global export rules", s["h1"]))
    story.append(
        p(
            "Use these rules on every asset unless a page section says otherwise.",
            s["body"],
        )
    )
    story.append(
        make_table(
            ["Rule", "Specification"],
            [
                ["Format", "JPG / WebP for photos · PNG for logos / UI marks"],
                ["Color space", "sRGB"],
                ["Retina", "Export at 2× display size whenever practical"],
                ["Crop mode", "object-fit: cover · object-position: center"],
                ["Safe zone", "Keep subject in center–lower third; leave ~10% edge margin"],
                ["Full-bleed banners", "Export wider/taller than viewport — they will crop"],
                ["Text overlays", "Avoid critical detail on left text columns & bottom captions"],
            ],
            [W * 0.28, W * 0.72],
            s,
        )
    )
    story.append(Spacer(1, 8))
    story.append(p("Priority deliverables", s["h2"]))
    for line in [
        "1. Three full-page application banners at <b>2560×1440 px</b> (rm-living / kitchen / bathroom)",
        "2. Five coverflow slides at <b>640×600 px</b> per product page",
        "3. Home gallery mosaic + journal / Instagram cards",
        "4. Remaining section images (about, blog, contact, use-cards)",
    ]:
        story.append(p("• " + line, s["bullet"]))

    story.append(PageBreak())

    # Home
    story.append(p("2. Home — index.html", s["h1"]))
    story.append(
        section(
            "Hero, cards &amp; sections",
            "Homepage image slots. Hero is currently a CSS gradient — ready for a photo background.",
            headers5,
            [
                ["Hero / Banner", "1", "Full viewport 100svh", "1920×1080 min / 2560×1440 ideal", "~16:9 full-bleed"],
                ["Doorway cards", "4", "~300×340 each", "600×680", "~3:4"],
                ["Category cards", "4", "~300×344", "600×688", "~3:4"],
                ["About figure", "1", "Aspect 4:5 (~560×700)", "1120×1400", "4:5 portrait"],
                ["Room highlight tiles", "4", "Min height 300px", "Wide 1480×600 / Tall 1060×600", "Flexible cover"],
                ["Journal covers", "3", "Aspect 16:10 (~400×250)", "800×500", "16:10"],
                ["Instagram cards", "6+", "216–290 × 9:16", "580×1032", "9:16 vertical"],
            ],
            c5,
            s,
        )
    )
    story.append(
        section(
            "Project gallery mosaic (at 1280 shell)",
            "Grid: 6 columns · gap 16px · auto-rows 200px.",
            ["Frame", "Display approx", "Export (2×)"],
            [
                ["Large g1 (4×2)", "848×416", "1696×832"],
                ["Small g2 / g3 (2×1)", "416×200", "832×400"],
                ["Mid g4 / g5 (3×1)", "632×200", "1264×400"],
            ],
            c3,
            s,
        )
    )

    # About / Blog / Contact
    story.append(p("3. About — about.html", s["h1"]))
    story.append(
        section(
            "Image slots",
            "Story visual uses a 4:5 portrait frame; team cards are fixed-height photo strips.",
            headers5,
            [
                ["Page hero banner", "1", "Full-width padded hero", "1920×900", "~21:10 optional BG"],
                ["Story visual", "1", "Aspect 4:5", "1120×1400", "4:5"],
                ["Team card photos", "3+", "Card width × 240px (~300×240)", "600×480", "5:4"],
            ],
            c5,
            s,
        )
    )

    story.append(p("4. Blog / Journal — blog.html", s["h1"]))
    story.append(
        section(
            "Image slots",
            "Hero visual + featured article media + grid card covers.",
            headers5,
            [
                ["Hero visual panel", "1", "Min ~560×280", "1200×600", "2:1"],
                ["Featured article media", "1", "Min ~640×420", "1280×840", "~3:2"],
                ["Blog card covers", "6–9", "Aspect 16:10", "800×500", "16:10"],
            ],
            c5,
            s,
        )
    )

    story.append(p("5. Contact — contact.html", s["h1"]))
    story.append(
        section(
            "Image slots",
            "Map area is the main photographic / map graphic slot.",
            headers5,
            [
                ["Page hero", "1", "Text + gradient hero", "1920×900", "Optional BG"],
                ["Map area", "1", "Full width × 480px (300 mobile)", "2560×960", "Desktop map/photo"],
            ],
            c5,
            s,
        )
    )

    story.append(PageBreak())

    # Product pages
    story.append(p("6. Product pages (shared layout)", s["h1"]))
    story.append(
        p(
            "Applies to: <b>rajasthan-marbles-tiles.html</b>, <b>Sanitaryware.html</b>, "
            "<b>Kitchen-Accessories.html</b>, <b>PVC-Pipes.html</b>, <b>Paints-Coatings.html</b>.",
            s["body"],
        )
    )
    story.append(
        section(
            "Per-page image slots",
            "Coverflow is the primary hero visual. Mobile slide width is 74vw — same export works with cover crop.",
            headers5,
            [
                ["Hero banner area", "1", "Full viewport 100svh", "1920×1080", "~16:9 optional BG"],
                ["Coverflow slides", "5", "Max 320×300 (clamp 208–320 × 228–300)", "640×600", "~1:1 / 16:15"],
                ["Use / application cards", "4", "~303×320 min", "640×640", "1:1"],
                ["Journal feature media", "1", "~650×380", "1300×760", "~17:10"],
            ],
            c5,
            s,
            extra="Tip: Export one set of 5 coverflow images per product category (tiles, sanitaryware, kitchen, PVC, paints).",
        )
    )

    # Application pages
    story.append(p("7. Application pages — full-bleed banners", s["h1"]))
    story.append(
        p(
            "Applies to: <b>rajasthan-marbles-residential.html</b>, <b>Hospitality.html</b>, "
            "<b>Commercial-&amp;-Govt-Institutions.html</b>.",
            s["body"],
        )
    )
    story.append(
        section(
            "Hero banners (critical)",
            "CSS: height 100svh · min-height 600px · object-fit cover · slight Ken Burns scale (1.08 → 1).",
            ["File name", "Role", "Export W×H", "Ratio"],
            [
                ["rm-living.jpg", "Banner 01 — primary scene", "1920×1080 min / 2560×1440 ideal", "16:9"],
                ["rm-kitchen.jpg", "Banner 02 — secondary scene", "1920×1080 min / 2560×1440 ideal", "16:9"],
                ["rm-bathroom.jpg", "Banner 03 — tertiary scene", "1920×1080 min / 2560×1440 ideal", "16:9"],
            ],
            c4,
            s,
            extra="Qty: 3 banners × 3 pages = 9 unique photos if pages should differ; or reuse the same 3 filenames across pages.",
        )
    )
    story.append(
        section(
            "Other image slots (same 3 pages)",
            "Zone and journal visuals currently use CSS scene textures — ready for photography.",
            headers5,
            [
                ["Zone visuals", "3", "Min ~540×300 half-column", "1200×800", "3:2"],
                ["Journal card tops", "3", "Card width × 170px (~400×170)", "800×340", "~21:9"],
            ],
            c5,
            s,
        )
    )

    story.append(PageBreak())

    # Quick checklist
    story.append(p("8. Quick banner checklist — all pages", s["h1"]))
    story.append(
        make_table(
            ["Page", "Banner type", "Recommended size"],
            [
                ["Home", "Full-screen hero", "2560×1440 px"],
                ["About", "Page hero BG", "1920×900 px"],
                ["Blog", "Page hero panel", "1200×600 px"],
                ["Contact", "Page hero BG", "1920×900 px"],
                ["Tiles / Sanitaryware / Kitchen / PVC / Paints", "Hero + 5 coverflow", "Hero 1920×1080 · slides 640×600"],
                ["Residential / Hospitality / Commercial", "3× full-page banners", "2560×1440 px each"],
            ],
            [W * 0.38, W * 0.28, W * 0.34],
            s,
        )
    )

    story.append(Spacer(1, 10))
    story.append(p("9. Suggested file naming", s["h1"]))
    naming = """
home-hero.jpg &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 2560×1440<br/>
home-gallery-01.jpg … 05.jpg &nbsp;→ mosaic sizes<br/>
home-journal-01.jpg … 03.jpg &nbsp;→ 800×500<br/>
home-ig-01.jpg … &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 580×1032<br/><br/>
about-story.jpg &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 1120×1400<br/>
about-team-01.jpg … &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 600×480<br/><br/>
blog-hero.jpg &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 1200×600<br/>
blog-featured.jpg &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 1280×840<br/>
blog-card-01.jpg … &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 800×500<br/><br/>
contact-map.jpg &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 2560×960<br/><br/>
[product]-slide-01.jpg … 05.jpg &nbsp;→ 640×600<br/>
[product]-use-01.jpg … 04.jpg &nbsp;&nbsp;&nbsp;→ 640×640<br/>
[product]-journal.jpg &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 1300×760<br/><br/>
rm-living.jpg &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 2560×1440<br/>
rm-kitchen.jpg &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 2560×1440<br/>
rm-bathroom.jpg &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 2560×1440
"""
    story.append(p(naming, s["body"]))

    story.append(Spacer(1, 8))
    story.append(
        p(
            "Generated for designer handoff from the live CSS layout of the Rajasthan Marbles website. "
            "Display sizes may vary slightly by viewport; exports are sized for retina and cover-crop safety.",
            s["note"],
        )
    )

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"Wrote: {OUT}")


if __name__ == "__main__":
    build()
