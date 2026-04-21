"""
image_processor.py — Handles uploaded image resizing, aspect-ratio preservation,
and conversion to ReportLab Image flowables for the Lampiran section.
"""
from io import BytesIO
from typing import List

from PIL import Image as PILImage
from reportlab.platypus import Image as RLImage, Table, Spacer, Paragraph
from reportlab.lib.units import mm

from modules.pdf_styles import get_styles, LIGHT_GRAY


# ── Constants ─────────────────────────────────────────────────────────────────
MAX_IMG_WIDTH = 80 * mm      # ~80mm per image (2 per row on A4)
MAX_IMG_HEIGHT = 65 * mm     # ~65mm per image
IMAGES_PER_ROW = 2
IMG_TABLE_COL_WIDTH = 88 * mm
IMG_SPACING = 4 * mm


def process_uploaded_image(uploaded_file) -> BytesIO:
    """
    Open an uploaded file with PIL, resize to fit within max dimensions,
    and return as a BytesIO buffer in PNG format.
    """
    img = PILImage.open(uploaded_file)

    # Convert RGBA → RGB for PDF compatibility
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Auto-rotate based on EXIF orientation
    try:
        from PIL import ExifTags
        for orientation_key in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation_key] == "Orientation":
                break
        exif = img._getexif()
        if exif is not None:
            orientation = exif.get(orientation_key)
            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, TypeError):
        pass

    # Resize maintaining aspect ratio
    img.thumbnail(
        (int(MAX_IMG_WIDTH / mm * 3), int(MAX_IMG_HEIGHT / mm * 3)),
        PILImage.LANCZOS,
    )

    buf = BytesIO()
    img.save(buf, format="PNG", quality=90)
    buf.seek(0)
    return buf


def create_image_flowable(image_buffer: BytesIO) -> RLImage:
    """Create a ReportLab Image flowable from a BytesIO buffer."""
    img = PILImage.open(image_buffer)
    w, h = img.size

    # Calculate display size maintaining aspect ratio within limits
    aspect = w / h
    if aspect >= (MAX_IMG_WIDTH / MAX_IMG_HEIGHT):
        display_w = MAX_IMG_WIDTH
        display_h = MAX_IMG_WIDTH / aspect
    else:
        display_h = MAX_IMG_HEIGHT
        display_w = MAX_IMG_HEIGHT * aspect

    image_buffer.seek(0)
    rl_img = RLImage(image_buffer, width=display_w, height=display_h)
    return rl_img


def build_image_grid(uploaded_files: list) -> list:
    """
    Process a list of uploaded files and return a list of ReportLab flowables
    arranged in a 2-column grid with numbered captions.
    """
    if not uploaded_files:
        return []

    styles = get_styles()
    flowables = []

    # Process all images
    image_data = []
    for i, uploaded_file in enumerate(uploaded_files):
        try:
            buf = process_uploaded_image(uploaded_file)
            rl_img = create_image_flowable(buf)
            caption = Paragraph(
                f"Foto {i + 1}: {uploaded_file.name}",
                styles["Caption"],
            )
            image_data.append([rl_img, caption])
        except Exception:
            # Skip unreadable images
            continue

    if not image_data:
        return []

    # Build rows of 2 images each
    rows = []
    for i in range(0, len(image_data), IMAGES_PER_ROW):
        img_row = []
        cap_row = []
        for j in range(IMAGES_PER_ROW):
            idx = i + j
            if idx < len(image_data):
                img_row.append(image_data[idx][0])
                cap_row.append(image_data[idx][1])
            else:
                img_row.append("")
                cap_row.append("")
        rows.append(img_row)
        rows.append(cap_row)

    col_widths = [IMG_TABLE_COL_WIDTH] * IMAGES_PER_ROW

    tbl = Table(rows, colWidths=col_widths)
    tbl.setStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.25, LIGHT_GRAY),
    ])

    flowables.append(tbl)

    return flowables
