"""
utils.py — Session state helpers and utility functions for the Asset Survey Automator.
"""
import streamlit as st
from datetime import date


def get_default_form_data() -> dict:
    """Returns the default form data structure with all fields initialized."""
    return {
        # ── Metadata ──────────────────────────────────────────────
        "periode_survey": "",
        "tanggal_survey": date.today(),
        "surveyor": "",
        "lokasi_id_aset": "",
        "luas_m2": "",
        "jenis_hak_sertifikat": "",

        # ── §1 Ringkasan Eksekutif ────────────────────────────────
        "ringkasan_eksekutif": "",

        # ── §2 Status Legal & Administrasi ────────────────────────
        "jenis_hak": "",
        "no_sertifikat_tanggal": "",
        "atas_nama": "PT Petrokimia Gresik",
        "kesesuaian_tata_ruang": "-",

        # ── §3 Kondisi Fisik & Batas Jalan ────────────────────────
        "patok_batas": "Ada - Lengkap",
        "pagar_pembatas": "Ada - Baik",
        "papan_kepemilikan": "Ada",
        "akses_jalan": "Memadai",
        "kondisi_permukaan": "Kosong",
        "drainase_kebersihan": "Baik",

        # ── §4 Aktivitas Pihak Ketiga ─────────────────────────────
        "indikasi_okupasi": "Tidak Ada",
        "keterangan_saksi": "",
        "kegiatan_usaha": "Tidak",

        # ── §5 Pemetaan & Koordinat ───────────────────────────────
        "titik_lat": "",
        "titik_lng": "",
        "tautan_polygon": "",

        # ── §7 Penilaian Risiko ───────────────────────────────────
        "risks": [
            {
                "name": "Lahan dimanfaatkan oleh Pihak Lain (bangunan semi permanen & permanen)",
                "dampak": 3,
                "kemungkinan": 2,
            },
            {
                "name": "Penyusutan Luas Lahan & Claim Kepemilikan Lahan oleh Pihak Lain",
                "dampak": 3,
                "kemungkinan": 2,
            },
            {
                "name": "Terhambatnya proses pengurusan perpanjangan sertipikat",
                "dampak": 2,
                "kemungkinan": 1,
            },
            {
                "name": "Diambil alih oleh Negara",
                "dampak": 4,
                "kemungkinan": 1,
            },
        ],

        # ── §8 Mitigasi ──────────────────────────────────────────
        "mitigasi_pembersihan": True,
        "mitigasi_patok": True,
        "mitigasi_papan": True,
        "mitigasi_patroli": True,
        "mitigasi_legal": True,
        "mitigasi_tambahan": "",

        # ── Signature ────────────────────────────────────────────
        "tanggal_ttd": date.today(),
        "catatan": "",
        "vp_nama": "",

        # ── Lampiran ─────────────────────────────────────────────
        "uploaded_images": [],

        # ── PDF Customization ────────────────────────────────────
        "pdf_title": "LAPORAN SURVEY PENGAMANAN ASET TANAH IDLE",
        "pdf_subtitle": "DEPARTEMEN MANAJEMEN ASET\nPT PETROKIMIA GRESIK",
    }


def init_session_state():
    """Initialize session state with default form data if not already set."""
    if "form_data" not in st.session_state:
        st.session_state.form_data = get_default_form_data()
    if "pdf_bytes" not in st.session_state:
        st.session_state.pdf_bytes = None
    if "show_preview" not in st.session_state:
        st.session_state.show_preview = False


def update_form_field(key: str, value):
    """Update a specific form field in session state."""
    st.session_state.form_data[key] = value


def get_risk_color(value: int) -> str:
    """Return risk level color name based on the risk score."""
    if value >= 15:
        return "Merah (Tinggi)"
    elif value >= 6:
        return "Kuning (Sedang)"
    else:
        return "Hijau (Rendah)"


def get_risk_level_text(value: int) -> str:
    """Return risk level text based on the risk score."""
    if value >= 15:
        return "Tinggi"
    elif value >= 6:
        return "Sedang"
    else:
        return "Rendah"
