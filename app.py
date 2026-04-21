"""
app.py — Main entry point for the Asset Survey Automator Streamlit application.

A web-based document automation tool for generating Asset Monitoring Reports
(Laporan Survey Pengamanan Aset Tanah) for PT Petrokimia Gresik.

Run with:  streamlit run app.py
"""
import base64
import streamlit as st
import streamlit.components.v1 as components

from modules.auth import render_auth
from modules.utils import init_session_state
from modules.form_sections import (
    render_tab_identitas,
    render_tab_legal_fisik,
    render_tab_pihak_ketiga_peta,
    render_tab_risiko,
    render_tab_mitigasi_lampiran,
)
from modules.pdf_generator import PDFGenerator


# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Asset Survey Automator",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ───────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Header branding ─────────────────────────────── */
    .main-header {
        background: linear-gradient(135deg, #0D47A1 0%, #1565C0 50%, #1E88E5 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(13, 71, 161, 0.3);
    }
    .main-header h1 {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .main-header p {
        color: rgba(255,255,255,0.85);
        font-size: 0.9rem;
        margin: 0.3rem 0 0 0;
    }

    /* ── Sidebar styling ────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E1117 0%, #1A1F2E 100%);
    }
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(30, 136, 229, 0.4);
    }

    /* ── Tab styling ─────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(26, 35, 126, 0.1);
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.85rem;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1565C0, #1E88E5) !important;
        color: white !important;
    }

    /* ── Cards ────────────────────────────────────────── */
    .metric-card {
        background: linear-gradient(135deg, #1A1F2E, #252B3B);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #1E88E5;
        margin-bottom: 0.8rem;
    }
    .metric-card h4 {
        color: #90CAF9;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0 0 0.3rem 0;
    }
    .metric-card p {
        color: #E0E0E0;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
    }

    /* ── Preview container ───────────────────────────── */
    .pdf-preview-container {
        background: #1A1F2E;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(30, 136, 229, 0.3);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    /* ── Buttons ──────────────────────────────────────── */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #2E7D32, #43A047) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(46, 125, 50, 0.4) !important;
    }

    /* ── Divider ──────────────────────────────────────── */
    .gradient-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #1E88E5, transparent);
        margin: 1.5rem 0;
        border: none;
    }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Main application entry point."""

    # Initialize session state
    init_session_state()

    # ── Authentication Gate ───────────────────────────────────────────
    is_authenticated = render_auth()

    if not is_authenticated:
        return

    # ══════════════════════════════════════════════════════════════════
    # AUTHENTICATED — RENDER MAIN APP
    # ══════════════════════════════════════════════════════════════════

    # ── Header ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="main-header">
        <h1>🏢 Asset Survey Automator</h1>
        <p>Laporan Survey Pengamanan Aset Tanah — Departemen Manajemen Aset, PT Petrokimia Gresik</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar Controls ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🛠️ Panel Kontrol")
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

        # Quick stats
        d = st.session_state.form_data
        filled_count = sum(1 for k, v in d.items() if v and k not in [
            "risks", "uploaded_images", "pdf_title", "pdf_subtitle",
            "mitigasi_pembersihan", "mitigasi_patok", "mitigasi_papan",
            "mitigasi_patroli", "mitigasi_legal",
        ] and str(v).strip())

        st.markdown(f"""
        <div class="metric-card">
            <h4>Fields Filled</h4>
            <p>{filled_count} / 20</p>
        </div>
        """, unsafe_allow_html=True)

        img_count = len(d.get("uploaded_images", []))
        st.markdown(f"""
        <div class="metric-card">
            <h4>Foto Uploaded</h4>
            <p>{img_count} foto</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

        # Generate PDF button
        generate_clicked = st.button(
            "📄 Generate PDF Preview",
            use_container_width=True,
            type="primary",
        )

        if generate_clicked:
            with st.spinner("⏳ Membuat PDF..."):
                try:
                    generator = PDFGenerator(st.session_state.form_data)
                    st.session_state.pdf_bytes = generator.generate()
                    st.session_state.show_preview = True
                    st.success("✅ PDF berhasil dibuat!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    st.session_state.pdf_bytes = None

        # Download button
        if st.session_state.pdf_bytes:
            lokasi = d.get("lokasi_id_aset", "aset") or "aset"
            filename = f"Laporan_Survey_{lokasi.replace(' ', '_')}.pdf"

            st.download_button(
                label="⬇️ Download PDF",
                data=st.session_state.pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
            )

        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

        # Reset button
        if st.button("🔄 Reset Form", use_container_width=True):
            from modules.utils import get_default_form_data
            st.session_state.form_data = get_default_form_data()
            st.session_state.pdf_bytes = None
            st.session_state.show_preview = False
            st.rerun()

    # ── Main Content Area ─────────────────────────────────────────────

    # Layout: Form on left, Preview on right
    if st.session_state.show_preview and st.session_state.pdf_bytes:
        form_col, preview_col = st.columns([1, 1])
    else:
        form_col = st.container()
        preview_col = None

    # ── Form Tabs ─────────────────────────────────────────────────────
    with form_col:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Identitas",
            "⚖️ Legal & Fisik",
            "👥 Pihak Ketiga",
            "⚠️ Risiko",
            "📎 Mitigasi & Foto",
        ])

        with tab1:
            render_tab_identitas()
        with tab2:
            render_tab_legal_fisik()
        with tab3:
            render_tab_pihak_ketiga_peta()
        with tab4:
            render_tab_risiko()
        with tab5:
            render_tab_mitigasi_lampiran()

    # ── PDF Preview ───────────────────────────────────────────────────
    if preview_col and st.session_state.pdf_bytes:
        with preview_col:
            st.markdown("### 👁️ Live PDF Preview")
            st.markdown('<div class="pdf-preview-container">', unsafe_allow_html=True)

            # Encode PDF to base64 and embed in iframe
            b64_pdf = base64.b64encode(st.session_state.pdf_bytes).decode("utf-8")
            pdf_display = f"""
            <iframe
                src="data:application/pdf;base64,{b64_pdf}"
                width="100%"
                height="800px"
                type="application/pdf"
                style="border: none; border-radius: 8px;"
            >
                <p>Browser Anda tidak mendukung preview PDF.
                Silakan download untuk melihat.</p>
            </iframe>
            """
            components.html(pdf_display, height=820, scrolling=False)
            st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
