"""
pdf_styles.py — Color palette, paragraph styles, and table style templates
for the Asset Survey Report PDF generation using ReportLab.
"""
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.units import mm

# ══════════════════════════════════════════════════════════════════════════════
# COLOR PALETTE
# ══════════════════════════════════════════════════════════════════════════════

# Corporate Blues
CORP_BLUE_DARK = colors.HexColor("#0D47A1")
CORP_BLUE = colors.HexColor("#1565C0")
CORP_BLUE_LIGHT = colors.HexColor("#42A5F5")
CORP_BLUE_BG = colors.HexColor("#E3F2FD")

# Risk Matrix Colors
RISK_GREEN = colors.HexColor("#4CAF50")
RISK_GREEN_LIGHT = colors.HexColor("#C8E6C9")
RISK_YELLOW = colors.HexColor("#FFC107")
RISK_YELLOW_LIGHT = colors.HexColor("#FFF9C4")
RISK_RED = colors.HexColor("#F44336")
RISK_RED_LIGHT = colors.HexColor("#FFCDD2")

# Neutral
HEADER_BG = colors.HexColor("#1A237E")
HEADER_TEXT = colors.white
TABLE_BORDER = colors.HexColor("#90CAF9")
TABLE_ALT_ROW = colors.HexColor("#F5F5F5")
BODY_TEXT_COLOR = colors.HexColor("#212121")
SECTION_TITLE_COLOR = colors.HexColor("#0D47A1")
LIGHT_GRAY = colors.HexColor("#E0E0E0")

# ══════════════════════════════════════════════════════════════════════════════
# PARAGRAPH STYLES
# ══════════════════════════════════════════════════════════════════════════════

_base = getSampleStyleSheet()


def get_styles() -> dict:
    """Return a dictionary of all custom ParagraphStyles."""

    styles = {}

    styles["Title"] = ParagraphStyle(
        "CustomTitle",
        parent=_base["Title"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=CORP_BLUE_DARK,
        spaceAfter=2 * mm,
    )

    styles["Subtitle"] = ParagraphStyle(
        "CustomSubtitle",
        parent=_base["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=BODY_TEXT_COLOR,
        spaceAfter=6 * mm,
    )

    styles["SectionHeader"] = ParagraphStyle(
        "SectionHeader",
        parent=_base["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=SECTION_TITLE_COLOR,
        spaceBefore=6 * mm,
        spaceAfter=3 * mm,
        leftIndent=0,
    )

    styles["SubSectionHeader"] = ParagraphStyle(
        "SubSectionHeader",
        parent=_base["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=CORP_BLUE,
        spaceBefore=3 * mm,
        spaceAfter=2 * mm,
    )

    styles["Body"] = ParagraphStyle(
        "CustomBody",
        parent=_base["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        alignment=TA_JUSTIFY,
        textColor=BODY_TEXT_COLOR,
        spaceAfter=2 * mm,
    )

    styles["BodyBold"] = ParagraphStyle(
        "BodyBold",
        parent=styles["Body"],
        fontName="Helvetica-Bold",
    )

    styles["TableHeader"] = ParagraphStyle(
        "TableHeader",
        parent=_base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        alignment=TA_CENTER,
        textColor=HEADER_TEXT,
    )

    styles["TableCell"] = ParagraphStyle(
        "TableCell",
        parent=_base["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        alignment=TA_LEFT,
        textColor=BODY_TEXT_COLOR,
    )

    styles["TableCellCenter"] = ParagraphStyle(
        "TableCellCenter",
        parent=styles["TableCell"],
        alignment=TA_CENTER,
    )

    styles["RiskMatrixCell"] = ParagraphStyle(
        "RiskMatrixCell",
        parent=_base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=BODY_TEXT_COLOR,
    )

    styles["Bullet"] = ParagraphStyle(
        "CustomBullet",
        parent=styles["Body"],
        bulletFontName="Helvetica",
        bulletFontSize=9,
        leftIndent=15,
        bulletIndent=5,
    )

    styles["SignatureLabel"] = ParagraphStyle(
        "SignatureLabel",
        parent=_base["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=BODY_TEXT_COLOR,
        spaceBefore=8 * mm,
    )

    styles["SignatureName"] = ParagraphStyle(
        "SignatureName",
        parent=_base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=BODY_TEXT_COLOR,
        spaceBefore=20 * mm,
    )

    styles["Caption"] = ParagraphStyle(
        "Caption",
        parent=_base["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#666666"),
        spaceAfter=3 * mm,
    )

    styles["Footer"] = ParagraphStyle(
        "Footer",
        parent=_base["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#999999"),
    )

    return styles


# ══════════════════════════════════════════════════════════════════════════════
# TABLE STYLE HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def get_info_table_style():
    """Style for the metadata / key-value info tables."""
    return [
        ("BACKGROUND", (0, 0), (0, -1), CORP_BLUE_BG),
        ("TEXTCOLOR", (0, 0), (0, -1), CORP_BLUE_DARK),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ALIGN", (1, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, TABLE_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]


def get_section_table_style():
    """Style for section content tables (e.g., Physical Condition, Third Party)."""
    return [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), HEADER_TEXT),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (0, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, TABLE_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, TABLE_ALT_ROW]),
    ]


def get_risk_matrix_cell_color(value: int) -> colors.Color:
    """Return the background color for a risk matrix cell based on L × I value."""
    if value >= 15:
        return RISK_RED_LIGHT
    elif value >= 6:
        return RISK_YELLOW_LIGHT
    else:
        return RISK_GREEN_LIGHT


def get_risk_matrix_text_color(value: int) -> colors.Color:
    """Return the text color for a risk matrix cell."""
    if value >= 15:
        return RISK_RED
    elif value >= 6:
        return colors.HexColor("#F57F17")
    else:
        return colors.HexColor("#2E7D32")


def get_risk_badge_color(value: int) -> colors.Color:
    """Return color for the risk level badge in the assessment table."""
    if value >= 15:
        return RISK_RED
    elif value >= 6:
        return RISK_YELLOW
    else:
        return RISK_GREEN
