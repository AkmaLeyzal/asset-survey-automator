"""
pdf_generator.py — Core PDF generation engine using ReportLab.
Faithfully recreates the Asset Survey Report (Laporan Survey Pengamanan Aset Tanah)
with tables, risk matrix, and dynamic image appendices.
"""
from io import BytesIO
from datetime import date

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable,
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

from modules.pdf_styles import (
    get_styles,
    get_info_table_style,
    get_section_table_style,
    get_risk_matrix_cell_color,
    get_risk_matrix_text_color,
    get_risk_badge_color,
    CORP_BLUE_DARK, CORP_BLUE, CORP_BLUE_LIGHT, CORP_BLUE_BG,
    HEADER_BG, HEADER_TEXT, TABLE_BORDER, LIGHT_GRAY,
    RISK_GREEN, RISK_GREEN_LIGHT,
    RISK_YELLOW, RISK_YELLOW_LIGHT,
    RISK_RED, RISK_RED_LIGHT,
    BODY_TEXT_COLOR, SECTION_TITLE_COLOR,
)
from modules.image_processor import build_image_grid


class PDFGenerator:
    """Generates the complete Asset Survey PDF report."""

    def __init__(self, form_data: dict):
        self.data = form_data
        self.styles = get_styles()
        self.page_width, self.page_height = A4
        self.margin = 20 * mm
        self.content_width = self.page_width - 2 * self.margin

    # ══════════════════════════════════════════════════════════════════════
    # HEADER
    # ══════════════════════════════════════════════════════════════════════
    def _build_header(self) -> list:
        """Build the report title/header block."""
        elements = []

        # Decorative top line
        elements.append(
            HRFlowable(
                width="100%", thickness=2,
                color=CORP_BLUE_DARK, spaceBefore=0, spaceAfter=3 * mm,
            )
        )

        title_text = self.data.get("pdf_title", "LAPORAN SURVEY PENGAMANAN ASET TANAH IDLE")
        elements.append(Paragraph(title_text, self.styles["Title"]))

        subtitle_text = self.data.get(
            "pdf_subtitle", "DEPARTEMEN MANAJEMEN ASET<br/>PT PETROKIMIA GRESIK"
        ).replace("\n", "<br/>")
        elements.append(Paragraph(subtitle_text, self.styles["Subtitle"]))

        elements.append(
            HRFlowable(
                width="100%", thickness=1,
                color=CORP_BLUE_LIGHT, spaceBefore=0, spaceAfter=4 * mm,
            )
        )

        return elements

    # ══════════════════════════════════════════════════════════════════════
    # METADATA TABLE
    # ══════════════════════════════════════════════════════════════════════
    def _build_metadata(self) -> list:
        """Build the metadata key-value table at the top."""
        d = self.data
        tanggal = d.get("tanggal_survey", date.today())
        if isinstance(tanggal, date):
            tanggal_str = tanggal.strftime("%d %B %Y")
        else:
            tanggal_str = str(tanggal)

        table_data = [
            [Paragraph("<b>Periode Survey</b>", self.styles["TableCell"]),
             Paragraph(d.get("periode_survey", ""), self.styles["TableCell"]),
             Paragraph("<b>Tanggal Survey</b>", self.styles["TableCell"]),
             Paragraph(tanggal_str, self.styles["TableCell"])],

            [Paragraph("<b>Surveyor</b>", self.styles["TableCell"]),
             Paragraph(d.get("surveyor", ""), self.styles["TableCell"]),
             Paragraph("<b>Lokasi/ID Aset</b>", self.styles["TableCell"]),
             Paragraph(d.get("lokasi_id_aset", ""), self.styles["TableCell"])],

            [Paragraph("<b>Luas (m²)</b>", self.styles["TableCell"]),
             Paragraph(d.get("luas_m2", ""), self.styles["TableCell"]),
             Paragraph("<b>Jenis Hak/No. Sertifikat</b>", self.styles["TableCell"]),
             Paragraph(d.get("jenis_hak_sertifikat", ""), self.styles["TableCell"])],
        ]

        col_widths = [35 * mm, 50 * mm, 40 * mm, 45 * mm]
        tbl = Table(table_data, colWidths=col_widths)
        tbl.setStyle(TableStyle(get_info_table_style()))

        return [tbl, Spacer(1, 4 * mm)]

    # ══════════════════════════════════════════════════════════════════════
    # §1 RINGKASAN EKSEKUTIF
    # ══════════════════════════════════════════════════════════════════════
    def _build_section_1(self) -> list:
        """Build Section 1 — Executive Summary."""
        elements = []
        elements.append(Paragraph("1. Ringkasan Eksekutif", self.styles["SectionHeader"]))
        text = self.data.get("ringkasan_eksekutif", "-")
        if not text.strip():
            text = "-"
        elements.append(Paragraph(text, self.styles["Body"]))
        return elements

    # ══════════════════════════════════════════════════════════════════════
    # §2 STATUS LEGAL & ADMINISTRASI
    # ══════════════════════════════════════════════════════════════════════
    def _build_section_2(self) -> list:
        """Build Section 2 — Legal Status & Administration."""
        elements = []
        elements.append(Paragraph("2. Status Legal &amp; Administrasi", self.styles["SectionHeader"]))

        d = self.data
        table_data = [
            [Paragraph("<b>a. Jenis Hak</b>", self.styles["TableCell"]),
             Paragraph(d.get("jenis_hak", ""), self.styles["TableCell"])],
            [Paragraph("<b>b. No. Sertifikat &amp; Tanggal</b>", self.styles["TableCell"]),
             Paragraph(d.get("no_sertifikat_tanggal", ""), self.styles["TableCell"])],
            [Paragraph("<b>c. Atas Nama</b>", self.styles["TableCell"]),
             Paragraph(d.get("atas_nama", "PT Petrokimia Gresik"), self.styles["TableCell"])],
            [Paragraph("<b>d. Kesesuaian Tata Ruang</b>", self.styles["TableCell"]),
             Paragraph(d.get("kesesuaian_tata_ruang", "-"), self.styles["TableCell"])],
        ]

        col_widths = [55 * mm, 115 * mm]
        tbl = Table(table_data, colWidths=col_widths)
        tbl.setStyle(TableStyle(get_info_table_style()))
        elements.append(tbl)
        return elements

    # ══════════════════════════════════════════════════════════════════════
    # §3 KONDISI FISIK & BATAS JALAN
    # ══════════════════════════════════════════════════════════════════════
    def _build_section_3(self) -> list:
        """Build Section 3 — Physical Condition & Road Boundaries."""
        elements = []
        elements.append(Paragraph("3. Kondisi Fisik &amp; Batas Jalan", self.styles["SectionHeader"]))

        d = self.data
        hdr = self.styles["TableHeader"]
        cell = self.styles["TableCellCenter"]

        header_row = [
            Paragraph("Patok Batas<br/>(ada/tidak)<br/>&amp; Kondisi", hdr),
            Paragraph("Pagar<br/>Pembatas<br/>(ada/tidak)<br/>&amp; Kondisi", hdr),
            Paragraph("Papan<br/>Kepemilikan<br/>(ada/tidak)", hdr),
            Paragraph("Akses Jalan<br/>(memadai,<br/>terbatas,<br/>tidak ada)", hdr),
            Paragraph("Kondisi<br/>Permukaan<br/>(kosong, semak,<br/>ditanami, okupasi)", hdr),
            Paragraph("Drainase &amp;<br/>Kebersihan<br/>(baik, cukup,<br/>buruk)", hdr),
        ]

        data_row = [
            Paragraph(d.get("patok_batas", ""), cell),
            Paragraph(d.get("pagar_pembatas", ""), cell),
            Paragraph(d.get("papan_kepemilikan", ""), cell),
            Paragraph(d.get("akses_jalan", ""), cell),
            Paragraph(d.get("kondisi_permukaan", ""), cell),
            Paragraph(d.get("drainase_kebersihan", ""), cell),
        ]

        col_w = self.content_width / 6
        tbl = Table([header_row, data_row], colWidths=[col_w] * 6)
        tbl.setStyle(TableStyle(get_section_table_style()))
        elements.append(tbl)
        return elements

    # ══════════════════════════════════════════════════════════════════════
    # §4 AKTIVITAS PIHAK KETIGA
    # ══════════════════════════════════════════════════════════════════════
    def _build_section_4(self) -> list:
        """Build Section 4 — Third Party Activity."""
        elements = []
        elements.append(
            Paragraph("4. Aktivitas Pihak Ketiga (Okupasi/Penggunaan)", self.styles["SectionHeader"])
        )

        d = self.data
        hdr = self.styles["TableHeader"]
        cell = self.styles["TableCellCenter"]

        header_row = [
            Paragraph("Indikasi Okupasi<br/>(tidak ada, ada tanaman,<br/>ada bangunan, perlintasan umum)", hdr),
            Paragraph("Keterangan Saksi<br/>atau Warga<br/>(bila ada)", hdr),
            Paragraph("Apakah Ada<br/>Kegiatan Usaha<br/>(ya, tidak)", hdr),
        ]

        data_row = [
            Paragraph(d.get("indikasi_okupasi", ""), cell),
            Paragraph(d.get("keterangan_saksi", "-"), cell),
            Paragraph(d.get("kegiatan_usaha", ""), cell),
        ]

        col_w = self.content_width / 3
        tbl = Table([header_row, data_row], colWidths=[col_w] * 3)
        tbl.setStyle(TableStyle(get_section_table_style()))
        elements.append(tbl)
        return elements

    # ══════════════════════════════════════════════════════════════════════
    # §5 PEMETAAN & KOORDINAT
    # ══════════════════════════════════════════════════════════════════════
    def _build_section_5(self) -> list:
        """Build Section 5 — Mapping & Coordinates."""
        elements = []
        elements.append(Paragraph("5. Pemetaan &amp; Koordinat", self.styles["SectionHeader"]))

        d = self.data
        lat = d.get("titik_lat", "")
        lng = d.get("titik_lng", "")
        coords = f"{lat}, {lng}" if lat and lng else "-"

        table_data = [
            [Paragraph("<b>Titik Patokan (Lat, Lng)</b>", self.styles["TableCell"]),
             Paragraph(coords, self.styles["TableCell"])],
            [Paragraph("<b>Tautan Polygon (KML/GeoJSON/Google Maps)</b>", self.styles["TableCell"]),
             Paragraph(d.get("tautan_polygon", "-"), self.styles["TableCell"])],
        ]

        col_widths = [65 * mm, 105 * mm]
        tbl = Table(table_data, colWidths=col_widths)
        tbl.setStyle(TableStyle(get_info_table_style()))
        elements.append(tbl)
        return elements

    # ══════════════════════════════════════════════════════════════════════
    # §6 ANALISIS RISIKO (Reference Tables)
    # ══════════════════════════════════════════════════════════════════════
    def _build_section_6(self) -> list:
        """Build Section 6 — Risk Analysis reference tables."""
        elements = []
        elements.append(Paragraph("6. Analisis Risiko", self.styles["SectionHeader"]))

        # ── a) Penilaian Kemungkinan ──────────────────────────────
        elements.append(
            Paragraph("a.) Penilaian Kemungkinan — Historis Keterjadian Risiko", self.styles["SubSectionHeader"])
        )

        likelihood_data = [
            ["1 = Sangat Kecil (Rare)", "Hampir tidak mungkin terjadi (pagar, patok dan plang)"],
            ["2 = Kecil (Unlikely)", "Kemungkinan kecil terjadi (pagar dan plang)"],
            ["3 = Sedang (Moderate)", "Dapat terjadi/tidak terjadi (patok lengkap)"],
            ["4 = Besar (Likely)", "Besar kemungkinan terjadi (patok parsial)"],
            ["5 = Sangat Besar (Certain)", "Hampir pasti terjadi (tidak ada pagar, patok dan plang)"],
        ]

        hdr = self.styles["TableHeader"]
        cell = self.styles["TableCell"]

        l_table = [[Paragraph("<b>Nilai</b>", hdr), Paragraph("<b>Keterangan</b>", hdr)]]
        for row in likelihood_data:
            l_table.append([
                Paragraph(row[0], self.styles["TableCellCenter"]),
                Paragraph(row[1], cell),
            ])

        tbl = Table(l_table, colWidths=[50 * mm, 120 * mm])
        tbl.setStyle(TableStyle(get_section_table_style()))
        elements.append(tbl)
        elements.append(Spacer(1, 3 * mm))

        # ── b) Penilaian Dampak — Keuangan ────────────────────────
        elements.append(
            Paragraph("b.) Penilaian Dampak — Keuangan dan Keamanan", self.styles["SubSectionHeader"])
        )

        impact_fin = [
            ["1 = Sangat Ringan (Insignificant)", "Potensi kerugian < Rp. 50.000.000"],
            ["2 = Ringan (Minor)", "Potensi kerugian Rp. 50.000.001 – Rp. 150.000.000"],
            ["3 = Sedang (Moderate)", "Potensi kerugian Rp. 150.000.001 – Rp. 300.000.000"],
            ["4 = Berat (Major)", "Potensi kerugian Rp. 300.000.001 – Rp. 500.000.000 dan/atau gangguan keamanan"],
            ["5 = Sangat Berat (Catastrophic)", "Potensi kerugian > Rp. 500.000.001 dan/atau gangguan keamanan"],
        ]

        f_table = [[Paragraph("<b>Nilai</b>", hdr), Paragraph("<b>Keterangan</b>", hdr)]]
        for row in impact_fin:
            f_table.append([
                Paragraph(row[0], self.styles["TableCellCenter"]),
                Paragraph(row[1], cell),
            ])

        tbl = Table(f_table, colWidths=[50 * mm, 120 * mm])
        tbl.setStyle(TableStyle(get_section_table_style()))
        elements.append(tbl)
        elements.append(Spacer(1, 3 * mm))

        # ── Penilaian Dampak — Reputasi ───────────────────────────
        elements.append(
            Paragraph("Penilaian Dampak — Reputasi Perusahaan", self.styles["SubSectionHeader"])
        )

        impact_rep = [
            ["1 = Sangat Ringan (Insignificant)", "Publisitas jelek di internal perusahaan"],
            ["2 = Ringan (Minor)", "Publisitas jelek di masyarakat sekitar"],
            ["3 = Sedang (Moderate)", "Publisitas jelek di media tertulis (email, medsos) dan bukan media resmi"],
            ["4 = Berat (Major)", "Publisitas jelek di media massa (regional/nasional)"],
            ["5 = Sangat Berat (Catastrophic)", "Publisitas jelek skala nasional dan sulit dikendalikan"],
        ]

        r_table = [[Paragraph("<b>Nilai</b>", hdr), Paragraph("<b>Keterangan</b>", hdr)]]
        for row in impact_rep:
            r_table.append([
                Paragraph(row[0], self.styles["TableCellCenter"]),
                Paragraph(row[1], cell),
            ])

        tbl = Table(r_table, colWidths=[50 * mm, 120 * mm])
        tbl.setStyle(TableStyle(get_section_table_style()))
        elements.append(tbl)

        return elements

    # ══════════════════════════════════════════════════════════════════════
    # §7 PENILAIAN RISIKO + RISK MATRIX
    # ══════════════════════════════════════════════════════════════════════
    def _build_section_7(self) -> list:
        """Build Section 7 — Risk Assessment table and 5×5 Risk Matrix."""
        elements = []
        elements.append(Paragraph("7. Penilaian Risiko", self.styles["SectionHeader"]))
        elements.append(
            Paragraph(
                "Metodologi: Likelihood (1–5) × Impact (1–5). "
                "Prioritas: <font color='#F44336'><b>Merah (≥15)</b></font>, "
                "<font color='#FFC107'><b>Kuning (6–12)</b></font>, "
                "<font color='#4CAF50'><b>Hijau (≤5)</b></font>.",
                self.styles["Body"],
            )
        )

        # ── Risk Assessment Table ─────────────────────────────────
        hdr = self.styles["TableHeader"]
        cell_c = self.styles["TableCellCenter"]
        cell = self.styles["TableCell"]

        header_row = [
            Paragraph("<b>No</b>", hdr),
            Paragraph("<b>Risiko</b>", hdr),
            Paragraph("<b>Dampak<br/>(1-5)</b>", hdr),
            Paragraph("<b>Kemungkinan<br/>(1-5)</b>", hdr),
            Paragraph("<b>Tingkat<br/>Risiko</b>", hdr),
            Paragraph("<b>Peta<br/>Risiko</b>", hdr),
        ]

        risks = self.data.get("risks", [])
        risk_rows = [header_row]

        for i, risk in enumerate(risks):
            dampak = risk.get("dampak", 1)
            kemungkinan = risk.get("kemungkinan", 1)
            tingkat = dampak * kemungkinan

            badge_color = get_risk_badge_color(tingkat)
            level_text = "Tinggi" if tingkat >= 15 else ("Sedang" if tingkat >= 6 else "Rendah")

            risk_rows.append([
                Paragraph(f"<b>{i + 1}</b>", cell_c),
                Paragraph(risk.get("name", ""), cell),
                Paragraph(f"<b>{dampak}</b>", cell_c),
                Paragraph(f"<b>{kemungkinan}</b>", cell_c),
                Paragraph(f"<b>{tingkat}</b>", cell_c),
                Paragraph(f"<b>{level_text}</b>", cell_c),
            ])

        col_widths = [10 * mm, 62 * mm, 20 * mm, 25 * mm, 20 * mm, 25 * mm]
        risk_tbl = Table(risk_rows, colWidths=col_widths)

        risk_style = list(get_section_table_style())

        # Color the Peta Risiko column cells
        for i, risk in enumerate(risks):
            row_idx = i + 1
            tingkat = risk.get("dampak", 1) * risk.get("kemungkinan", 1)
            bg = get_risk_matrix_cell_color(tingkat)
            txt_color = get_risk_matrix_text_color(tingkat)
            risk_style.append(("BACKGROUND", (5, row_idx), (5, row_idx), bg))
            risk_style.append(("TEXTCOLOR", (5, row_idx), (5, row_idx), txt_color))
            risk_style.append(("BACKGROUND", (4, row_idx), (4, row_idx), bg))
            risk_style.append(("TEXTCOLOR", (4, row_idx), (4, row_idx), txt_color))

        risk_tbl.setStyle(TableStyle(risk_style))
        elements.append(risk_tbl)
        elements.append(Spacer(1, 3 * mm))

        # ── S&K Note ──────────────────────────────────────────────
        elements.append(
            Paragraph(
                "<i>S&amp;K: Risiko Nomor 3 &amp; 4 aktif apabila aset tanah "
                "tidak dimanfaatkan atau tidak ada patok lengkap.</i>",
                self.styles["Body"],
            )
        )
        elements.append(Spacer(1, 4 * mm))

        # ── 5×5 Risk Matrix ──────────────────────────────────────
        elements.append(Paragraph("<b>Risk Matrix</b>", self.styles["SubSectionHeader"]))
        elements.extend(self._build_risk_matrix_5x5())

        return elements

    def _build_risk_matrix_5x5(self) -> list:
        """Build the 5×5 colored risk matrix grid."""
        hdr = self.styles["TableHeader"]
        rm_cell = self.styles["RiskMatrixCell"]

        # Header row: blank + Impact 1..5
        matrix_data = [
            [
                Paragraph("<b>Kemungkinan ↓<br/>Dampak →</b>", hdr),
                Paragraph("<b>1</b>", hdr),
                Paragraph("<b>2</b>", hdr),
                Paragraph("<b>3</b>", hdr),
                Paragraph("<b>4</b>", hdr),
                Paragraph("<b>5</b>", hdr),
            ]
        ]

        # Build 5 rows (Likelihood 1..5)
        for likelihood in range(1, 6):
            row = [Paragraph(f"<b>{likelihood}</b>", hdr)]
            for impact in range(1, 6):
                val = likelihood * impact
                row.append(Paragraph(f"<b>{val}</b>", rm_cell))
            matrix_data.append(row)

        cell_size = 22 * mm
        col_widths = [30 * mm] + [cell_size] * 5
        row_heights = [14 * mm] + [cell_size] * 5

        matrix_tbl = Table(matrix_data, colWidths=col_widths, rowHeights=row_heights)

        # Base styling
        style_cmds = [
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 1, colors.white),
            ("BOX", (0, 0), (-1, -1), 1.5, CORP_BLUE_DARK),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            # Header row
            ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
            ("TEXTCOLOR", (0, 0), (-1, 0), HEADER_TEXT),
            # Header column
            ("BACKGROUND", (0, 0), (0, -1), HEADER_BG),
            ("TEXTCOLOR", (0, 0), (0, -1), HEADER_TEXT),
        ]

        # Color each cell based on L × I value
        for row in range(1, 6):       # Likelihood (row index 1..5)
            for col in range(1, 6):   # Impact (col index 1..5)
                val = row * col
                bg = get_risk_matrix_cell_color(val)
                txt = get_risk_matrix_text_color(val)
                style_cmds.append(("BACKGROUND", (col, row), (col, row), bg))
                style_cmds.append(("TEXTCOLOR", (col, row), (col, row), txt))

        # Mark user's risk positions with bold borders
        risks = self.data.get("risks", [])
        for risk in risks:
            lik = risk.get("kemungkinan", 1)
            imp = risk.get("dampak", 1)
            style_cmds.append(
                ("BOX", (imp, lik), (imp, lik), 3, CORP_BLUE_DARK)
            )

        matrix_tbl.setStyle(TableStyle(style_cmds))

        # Legend
        legend_data = [[
            Paragraph("■", ParagraphStyle("lg", fontName="Helvetica-Bold", fontSize=12, textColor=RISK_GREEN, alignment=1)),
            Paragraph("Rendah (≤5)", self.styles["TableCell"]),
            Paragraph("■", ParagraphStyle("ly", fontName="Helvetica-Bold", fontSize=12, textColor=RISK_YELLOW, alignment=1)),
            Paragraph("Sedang (6–12)", self.styles["TableCell"]),
            Paragraph("■", ParagraphStyle("lr", fontName="Helvetica-Bold", fontSize=12, textColor=RISK_RED, alignment=1)),
            Paragraph("Tinggi (≥15)", self.styles["TableCell"]),
        ]]

        legend = Table(legend_data, colWidths=[8 * mm, 25 * mm, 8 * mm, 25 * mm, 8 * mm, 25 * mm])
        legend.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))

        return [matrix_tbl, Spacer(1, 2 * mm), legend]

    # ══════════════════════════════════════════════════════════════════════
    # §8 MITIGASI / REKOMENDASI
    # ══════════════════════════════════════════════════════════════════════
    def _build_section_8(self) -> list:
        """Build Section 8 — Mitigation & Recommendations."""
        elements = []
        elements.append(
            Paragraph("8. Mitigasi / Rekomendasi &amp; Rencana Tindak Lanjut", self.styles["SectionHeader"])
        )

        d = self.data
        mitigations = []
        if d.get("mitigasi_pembersihan"):
            mitigations.append("Pembersihan lahan periodik (3× setahun).")
        if d.get("mitigasi_patok"):
            mitigations.append("Pengukuran ulang dan pemeliharaan patok secara berkala.")
        if d.get("mitigasi_papan"):
            mitigations.append("Pemasangan papan kepemilikan & nomor hotline.")
        if d.get("mitigasi_patroli"):
            mitigations.append("Jadwal patroli dan inspeksi berkala.")
        if d.get("mitigasi_legal"):
            mitigations.append("Pengawalan legal bila ada indikasi sengketa/okupasi.")

        tambahan = d.get("mitigasi_tambahan", "")
        if tambahan.strip():
            for line in tambahan.strip().split("\n"):
                if line.strip():
                    mitigations.append(line.strip())

        for item in mitigations:
            elements.append(
                Paragraph(f"●  {item}", self.styles["Bullet"])
            )

        return elements

    # ══════════════════════════════════════════════════════════════════════
    # SIGNATURE BLOCK
    # ══════════════════════════════════════════════════════════════════════
    def _build_signature(self) -> list:
        """Build the signature / Date / VP block."""
        elements = []
        elements.append(Spacer(1, 6 * mm))

        d = self.data
        tanggal = d.get("tanggal_ttd", date.today())
        if isinstance(tanggal, date):
            tanggal_str = tanggal.strftime("%d %B %Y")
        else:
            tanggal_str = str(tanggal)

        catatan = d.get("catatan", "")

        if catatan.strip():
            elements.append(Paragraph(f"<b>Catatan:</b> {catatan}", self.styles["Body"]))
            elements.append(Spacer(1, 3 * mm))

        # Signature table — right-aligned
        sig_data = [
            [
                "",
                Paragraph(f"Tanggal: {tanggal_str}", self.styles["SignatureLabel"]),
            ],
            [
                "",
                Paragraph("VP Manajemen Aset", self.styles["SignatureLabel"]),
            ],
            [
                "",
                Paragraph(
                    d.get("vp_nama", "___________________"),
                    self.styles["SignatureName"],
                ),
            ],
        ]

        sig_tbl = Table(sig_data, colWidths=[self.content_width * 0.5, self.content_width * 0.5])
        sig_tbl.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        elements.append(sig_tbl)

        return elements

    # ══════════════════════════════════════════════════════════════════════
    # LAMPIRAN (APPENDIX)
    # ══════════════════════════════════════════════════════════════════════
    def _build_lampiran(self) -> list:
        """Build the Lampiran section with photo grid."""
        elements = []
        uploaded = self.data.get("uploaded_images", [])

        if not uploaded:
            return elements

        elements.append(PageBreak())
        elements.append(Paragraph("Lampiran Laporan", self.styles["SectionHeader"]))
        elements.append(
            Paragraph("1. Dokumentasi Foto", self.styles["SubSectionHeader"])
        )

        # Build the image grid
        image_flowables = build_image_grid(uploaded)
        elements.extend(image_flowables)

        return elements

    # ══════════════════════════════════════════════════════════════════════
    # GENERATE FULL PDF
    # ══════════════════════════════════════════════════════════════════════
    def generate(self) -> bytes:
        """Generate the complete PDF and return as bytes."""
        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=self.margin,
            rightMargin=self.margin,
            topMargin=15 * mm,
            bottomMargin=15 * mm,
            title=self.data.get("pdf_title", "Laporan Survey Aset"),
            author="Departemen Manajemen Aset - PT Petrokimia Gresik",
        )

        # Build all elements in order
        elements = []
        elements.extend(self._build_header())
        elements.extend(self._build_metadata())
        elements.extend(self._build_section_1())
        elements.extend(self._build_section_2())
        elements.extend(self._build_section_3())
        elements.extend(self._build_section_4())
        elements.extend(self._build_section_5())

        # Page break before risk analysis (large section)
        elements.append(PageBreak())
        elements.extend(self._build_section_6())

        elements.append(PageBreak())
        elements.extend(self._build_section_7())

        elements.extend(self._build_section_8())
        elements.extend(self._build_signature())
        elements.extend(self._build_lampiran())

        doc.build(elements)
        return buffer.getvalue()
