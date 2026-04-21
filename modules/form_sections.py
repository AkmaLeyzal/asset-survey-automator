"""
form_sections.py — Streamlit form section components for the Asset Survey Automator.
Each function renders a section of the survey form and updates session state.
"""
import streamlit as st
from datetime import date
from modules.utils import get_risk_color


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — IDENTITAS & RINGKASAN EKSEKUTIF
# ══════════════════════════════════════════════════════════════════════════════
def render_tab_identitas():
    """Render the Metadata + Executive Summary form tab."""
    d = st.session_state.form_data

    st.markdown("### 📋 Identitas Aset & Ringkasan")
    st.markdown("---")

    # ── PDF Customization ─────────────────────────────────────────────
    with st.expander("⚙️ Kustomisasi Judul PDF", expanded=False):
        d["pdf_title"] = st.text_input(
            "Judul PDF",
            value=d.get("pdf_title", "LAPORAN SURVEY PENGAMANAN ASET TANAH IDLE"),
            key="inp_pdf_title",
            help="Judul utama yang ditampilkan di PDF",
        )
        d["pdf_subtitle"] = st.text_area(
            "Subtitle PDF",
            value=d.get("pdf_subtitle", "DEPARTEMEN MANAJEMEN ASET\nPT PETROKIMIA GRESIK"),
            key="inp_pdf_subtitle",
            height=80,
            help="Baris subtitle di bawah judul",
        )

    st.markdown("#### 📝 Data Survey")

    col1, col2 = st.columns(2)
    with col1:
        d["periode_survey"] = st.text_input(
            "Periode Survey",
            value=d.get("periode_survey", ""),
            key="inp_periode",
            placeholder="Contoh: Semester I 2024",
        )
        d["tanggal_survey"] = st.date_input(
            "Tanggal Survey",
            value=d.get("tanggal_survey", date.today()),
            key="inp_tanggal",
        )
        d["surveyor"] = st.text_input(
            "Surveyor",
            value=d.get("surveyor", ""),
            key="inp_surveyor",
            placeholder="Nama Surveyor",
        )

    with col2:
        d["lokasi_id_aset"] = st.text_input(
            "Lokasi / ID Aset",
            value=d.get("lokasi_id_aset", ""),
            key="inp_lokasi",
            placeholder="Contoh: SHGB-03 Surabaya",
        )
        d["luas_m2"] = st.text_input(
            "Luas (m²)",
            value=d.get("luas_m2", ""),
            key="inp_luas",
            placeholder="Contoh: 5.000",
        )
        d["jenis_hak_sertifikat"] = st.text_input(
            "Jenis Hak / No. Sertifikat",
            value=d.get("jenis_hak_sertifikat", ""),
            key="inp_jenis_hak_srt",
            placeholder="Contoh: HGB No. 123/2020",
        )

    st.markdown("---")
    st.markdown("#### 📝 Ringkasan Eksekutif")
    d["ringkasan_eksekutif"] = st.text_area(
        "Ringkasan Eksekutif (§1)",
        value=d.get("ringkasan_eksekutif", ""),
        key="inp_ringkasan",
        height=150,
        placeholder="Contoh: Lahan terdapat 1 (satu) bangunan semi permanen berupa Pos/Gardu Palang Kereta Api. Kondisi lahan secara umum terawat dengan ...",
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — STATUS LEGAL & KONDISI FISIK
# ══════════════════════════════════════════════════════════════════════════════
def render_tab_legal_fisik():
    """Render the Legal Status + Physical Condition form tab."""
    d = st.session_state.form_data

    st.markdown("### ⚖️ Status Legal & Kondisi Fisik")
    st.markdown("---")

    # ── §2 Status Legal ───────────────────────────────────────────────
    st.markdown("#### 📜 Status Legal & Administrasi (§2)")

    col1, col2 = st.columns(2)
    with col1:
        d["jenis_hak"] = st.text_input(
            "a. Jenis Hak",
            value=d.get("jenis_hak", ""),
            key="inp_jenis_hak",
            placeholder="Contoh: Hak Guna Bangunan (HGB)",
        )
        d["no_sertifikat_tanggal"] = st.text_input(
            "b. No. Sertifikat & Tanggal",
            value=d.get("no_sertifikat_tanggal", ""),
            key="inp_no_sertifikat",
            placeholder="Contoh: No. 123 / 15 Januari 2020",
        )

    with col2:
        d["atas_nama"] = st.text_input(
            "c. Atas Nama",
            value=d.get("atas_nama", "PT Petrokimia Gresik"),
            key="inp_atas_nama",
        )
        d["kesesuaian_tata_ruang"] = st.selectbox(
            "d. Kesesuaian Tata Ruang",
            options=["Sesuai", "Tidak Sesuai", "Dalam Proses", "-"],
            index=["Sesuai", "Tidak Sesuai", "Dalam Proses", "-"].index(
                d.get("kesesuaian_tata_ruang", "-")
            ),
            key="inp_tata_ruang",
        )

    st.markdown("---")

    # ── §3 Kondisi Fisik ──────────────────────────────────────────────
    st.markdown("#### 🏗️ Kondisi Fisik & Batas Jalan (§3)")

    col1, col2, col3 = st.columns(3)

    with col1:
        patok_options = [
            "Ada - Lengkap", "Ada - Parsial", "Ada - Nihil",
            "Tidak Ada"
        ]
        d["patok_batas"] = st.selectbox(
            "Patok Batas",
            options=patok_options,
            index=patok_options.index(d.get("patok_batas", "Ada - Lengkap")),
            key="inp_patok",
            help="Keberadaan dan kondisi patok batas",
        )

        pagar_options = [
            "Ada - Baik", "Ada - Cukup", "Ada - Buruk",
            "Tidak Ada"
        ]
        d["pagar_pembatas"] = st.selectbox(
            "Pagar Pembatas",
            options=pagar_options,
            index=pagar_options.index(d.get("pagar_pembatas", "Ada - Baik")),
            key="inp_pagar",
        )

    with col2:
        papan_options = ["Ada", "Tidak Ada"]
        d["papan_kepemilikan"] = st.selectbox(
            "Papan Kepemilikan",
            options=papan_options,
            index=papan_options.index(d.get("papan_kepemilikan", "Ada")),
            key="inp_papan",
        )

        akses_options = ["Memadai", "Terbatas", "Tidak Ada"]
        d["akses_jalan"] = st.selectbox(
            "Akses Jalan",
            options=akses_options,
            index=akses_options.index(d.get("akses_jalan", "Memadai")),
            key="inp_akses",
        )

    with col3:
        permukaan_options = ["Kosong", "Semak", "Ditanami", "Okupasi"]
        d["kondisi_permukaan"] = st.selectbox(
            "Kondisi Permukaan",
            options=permukaan_options,
            index=permukaan_options.index(d.get("kondisi_permukaan", "Kosong")),
            key="inp_permukaan",
        )

        drainase_options = ["Baik", "Cukup", "Buruk"]
        d["drainase_kebersihan"] = st.selectbox(
            "Drainase & Kebersihan",
            options=drainase_options,
            index=drainase_options.index(d.get("drainase_kebersihan", "Baik")),
            key="inp_drainase",
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PIHAK KETIGA & PEMETAAN
# ══════════════════════════════════════════════════════════════════════════════
def render_tab_pihak_ketiga_peta():
    """Render Third Party Activity + Mapping & Coordinates form tab."""
    d = st.session_state.form_data

    st.markdown("### 👥 Pihak Ketiga & Pemetaan")
    st.markdown("---")

    # ── §4 Aktivitas Pihak Ketiga ─────────────────────────────────────
    st.markdown("#### 🏘️ Aktivitas Pihak Ketiga / Okupasi (§4)")

    col1, col2 = st.columns(2)
    with col1:
        okupasi_options = [
            "Tidak Ada",
            "Ada Tanaman",
            "Ada Bangunan",
            "Perlintasan Umum",
        ]
        d["indikasi_okupasi"] = st.selectbox(
            "Indikasi Okupasi",
            options=okupasi_options,
            index=okupasi_options.index(d.get("indikasi_okupasi", "Tidak Ada")),
            key="inp_okupasi",
        )

        usaha_options = ["Tidak", "Ya"]
        d["kegiatan_usaha"] = st.selectbox(
            "Kegiatan Usaha",
            options=usaha_options,
            index=usaha_options.index(d.get("kegiatan_usaha", "Tidak")),
            key="inp_usaha",
        )

    with col2:
        d["keterangan_saksi"] = st.text_area(
            "Keterangan Saksi / Warga (bila ada)",
            value=d.get("keterangan_saksi", ""),
            key="inp_saksi",
            height=120,
            placeholder="Keterangan dari warga atau saksi setempat...",
        )

    st.markdown("---")

    # ── §5 Pemetaan & Koordinat ───────────────────────────────────────
    st.markdown("#### 🗺️ Pemetaan & Koordinat (§5)")

    col1, col2 = st.columns(2)
    with col1:
        d["titik_lat"] = st.text_input(
            "Latitude",
            value=d.get("titik_lat", ""),
            key="inp_lat",
            placeholder="Contoh: 7°05'53\"S",
        )
    with col2:
        d["titik_lng"] = st.text_input(
            "Longitude",
            value=d.get("titik_lng", ""),
            key="inp_lng",
            placeholder="Contoh: 112°20'56\"E",
        )

    d["tautan_polygon"] = st.text_input(
        "Tautan Polygon (KML/GeoJSON/Google Maps)",
        value=d.get("tautan_polygon", ""),
        key="inp_polygon",
        placeholder="https://maps.google.com/...",
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ANALISIS RISIKO
# ══════════════════════════════════════════════════════════════════════════════
def render_tab_risiko():
    """Render the Risk Analysis form tab with interactive sliders."""
    d = st.session_state.form_data

    st.markdown("### ⚠️ Analisis & Penilaian Risiko")
    st.markdown("---")

    # ── §6 Reference Info ─────────────────────────────────────────────
    with st.expander("📖 Tabel Referensi Penilaian (Lihat Definisi)", expanded=False):
        st.markdown("##### Skala Kemungkinan (Likelihood)")
        st.markdown("""
| Nilai | Level | Keterangan |
|:-----:|:------|:-----------|
| 1 | Sangat Kecil (Rare) | Hampir tidak mungkin terjadi (pagar, patok dan plang) |
| 2 | Kecil (Unlikely) | Kemungkinan kecil terjadi (pagar dan plang) |
| 3 | Sedang (Moderate) | Dapat terjadi / tidak terjadi (patok lengkap) |
| 4 | Besar (Likely) | Besar kemungkinan terjadi (patok parsial) |
| 5 | Sangat Besar (Certain) | Hampir pasti terjadi (tidak ada pagar, patok dan plang) |
        """)

        st.markdown("##### Skala Dampak — Keuangan & Keamanan")
        st.markdown("""
| Nilai | Level | Keterangan |
|:-----:|:------|:-----------|
| 1 | Sangat Ringan | Potensi kerugian < Rp 50.000.000 |
| 2 | Ringan | Rp 50.000.001 – Rp 150.000.000 |
| 3 | Sedang | Rp 150.000.001 – Rp 300.000.000 |
| 4 | Berat | Rp 300.000.001 – Rp 500.000.000 dan/atau gangguan keamanan |
| 5 | Sangat Berat | > Rp 500.000.001 dan/atau gangguan keamanan |
        """)

    st.markdown("---")

    # ── §7 Risk Input ─────────────────────────────────────────────────
    st.markdown("#### 📊 Penilaian Risiko (§7)")
    st.caption("Geser slider untuk menentukan Dampak dan Kemungkinan masing-masing risiko.")

    risks = d.get("risks", [])

    for i, risk in enumerate(risks):
        with st.container():
            st.markdown(f"**Risiko {i + 1}:** {risk['name']}")

            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                risk["dampak"] = st.slider(
                    f"Dampak (Risiko {i + 1})",
                    min_value=1, max_value=5,
                    value=risk.get("dampak", 1),
                    key=f"slider_dampak_{i}",
                )
            with col2:
                risk["kemungkinan"] = st.slider(
                    f"Kemungkinan (Risiko {i + 1})",
                    min_value=1, max_value=5,
                    value=risk.get("kemungkinan", 1),
                    key=f"slider_kemungkinan_{i}",
                )
            with col3:
                tingkat = risk["dampak"] * risk["kemungkinan"]
                color_label = get_risk_color(tingkat)

                if tingkat >= 15:
                    st.markdown(f"#### :red[⬤ {tingkat}]")
                elif tingkat >= 6:
                    st.markdown(f"#### :orange[⬤ {tingkat}]")
                else:
                    st.markdown(f"#### :green[⬤ {tingkat}]")
                st.caption(color_label)

            st.markdown("---")

    # ── Live Risk Matrix Preview ──────────────────────────────────────
    st.markdown("#### 🎯 Preview Risk Matrix (5×5)")

    matrix_html = _generate_risk_matrix_html(risks)
    st.markdown(matrix_html, unsafe_allow_html=True)


def _generate_risk_matrix_html(risks: list) -> str:
    """Generate an HTML risk matrix for Streamlit preview."""
    # Collect user risk positions
    risk_positions = set()
    for risk in risks:
        pos = (risk.get("kemungkinan", 1), risk.get("dampak", 1))
        risk_positions.add(pos)

    html = """
    <style>
        .risk-matrix { border-collapse: collapse; margin: 0 auto; }
        .risk-matrix td, .risk-matrix th {
            width: 52px; height: 42px; text-align: center;
            font-weight: bold; font-size: 14px;
            border: 1px solid #444;
        }
        .risk-matrix th {
            background: #1A237E; color: white; font-size: 11px;
        }
        .risk-green { background: #C8E6C9; color: #2E7D32; }
        .risk-yellow { background: #FFF9C4; color: #F57F17; }
        .risk-red { background: #FFCDD2; color: #C62828; }
        .risk-marked { border: 3px solid #1565C0 !important; font-size: 16px !important; }
    </style>
    <table class="risk-matrix">
        <tr>
            <th>K↓ D→</th>
            <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
        </tr>
    """

    for lik in range(1, 6):
        html += f"<tr><th>{lik}</th>"
        for imp in range(1, 6):
            val = lik * imp
            if val >= 15:
                cls = "risk-red"
            elif val >= 6:
                cls = "risk-yellow"
            else:
                cls = "risk-green"

            marked = " risk-marked" if (lik, imp) in risk_positions else ""
            html += f'<td class="{cls}{marked}">{val}</td>'
        html += "</tr>"

    html += "</table>"
    return html


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — MITIGASI & LAMPIRAN
# ══════════════════════════════════════════════════════════════════════════════
def render_tab_mitigasi_lampiran():
    """Render the Mitigation checklist + Image Upload tab."""
    d = st.session_state.form_data

    st.markdown("### 📎 Mitigasi & Lampiran")
    st.markdown("---")

    # ── §8 Mitigasi ───────────────────────────────────────────────────
    st.markdown("#### 🛡️ Mitigasi / Rekomendasi (§8)")

    d["mitigasi_pembersihan"] = st.checkbox(
        "Pembersihan lahan periodik (3× setahun)",
        value=d.get("mitigasi_pembersihan", True),
        key="chk_m1",
    )
    d["mitigasi_patok"] = st.checkbox(
        "Pengukuran ulang dan pemeliharaan patok secara berkala",
        value=d.get("mitigasi_patok", True),
        key="chk_m2",
    )
    d["mitigasi_papan"] = st.checkbox(
        "Pemasangan papan kepemilikan & nomor hotline",
        value=d.get("mitigasi_papan", True),
        key="chk_m3",
    )
    d["mitigasi_patroli"] = st.checkbox(
        "Jadwal patroli dan inspeksi berkala",
        value=d.get("mitigasi_patroli", True),
        key="chk_m4",
    )
    d["mitigasi_legal"] = st.checkbox(
        "Pengawalan legal bila ada indikasi sengketa/okupasi",
        value=d.get("mitigasi_legal", True),
        key="chk_m5",
    )

    d["mitigasi_tambahan"] = st.text_area(
        "Rekomendasi Tambahan (opsional)",
        value=d.get("mitigasi_tambahan", ""),
        key="inp_tambahan",
        height=100,
        placeholder="Tambahan rekomendasi lainnya (satu per baris)...",
    )

    st.markdown("---")

    # ── Signature ─────────────────────────────────────────────────────
    st.markdown("#### ✍️ Tanda Tangan & Penanggung Jawab")

    col1, col2 = st.columns(2)
    with col1:
        d["tanggal_ttd"] = st.date_input(
            "Tanggal Dokumen",
            value=d.get("tanggal_ttd", date.today()),
            key="inp_tgl_ttd",
        )
    with col2:
        d["vp_nama"] = st.text_input(
            "Nama VP Manajemen Aset",
            value=d.get("vp_nama", ""),
            key="inp_vp",
            placeholder="Nama lengkap VP",
        )

    d["catatan"] = st.text_area(
        "Catatan (opsional)",
        value=d.get("catatan", ""),
        key="inp_catatan",
        height=80,
        placeholder="Catatan tambahan untuk laporan...",
    )

    st.markdown("---")

    # ── Image Upload ──────────────────────────────────────────────────
    st.markdown("#### 📷 Lampiran — Dokumentasi Foto")
    st.caption("Upload foto-foto dokumentasi survey. Gambar akan secara otomatis diatur di halaman Lampiran PDF.")

    uploaded_files = st.file_uploader(
        "Upload Foto Dokumentasi",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
        accept_multiple_files=True,
        key="file_uploader_photos",
        help="Maksimum 50MB total. Mendukung JPG, PNG, BMP, WebP.",
    )

    if uploaded_files:
        d["uploaded_images"] = uploaded_files
        st.success(f"✅ {len(uploaded_files)} foto berhasil di-upload")

        # Show thumbnails
        cols = st.columns(min(len(uploaded_files), 4))
        for i, f in enumerate(uploaded_files[:8]):  # Show first 8
            with cols[i % 4]:
                st.image(f, caption=f.name, use_container_width=True)

        if len(uploaded_files) > 8:
            st.info(f"... dan {len(uploaded_files) - 8} foto lainnya")
    else:
        d["uploaded_images"] = []
