"""
auth.py — Authentication handler using streamlit-authenticator.
Loads credentials from config.yaml and manages login/logout flow.
"""
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from pathlib import Path


def load_auth_config() -> dict:
    """Load authentication configuration from config.yaml."""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=SafeLoader)
    return config


def save_auth_config(config: dict):
    """Save updated config (e.g., hashed passwords) back to config.yaml."""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)


def render_auth() -> bool:
    """
    Render the authentication UI and return True if user is authenticated.
    Returns False if not authenticated.
    """
    config = load_auth_config()

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )

    # ── Render login widget ────────────────────────────────────
    try:
        authenticator.login()
    except Exception as e:
        st.error(f"Authentication error: {e}")

    # ── Handle authentication status ──────────────────────────
    auth_status = st.session_state.get("authentication_status")

    if auth_status:
        # ── Authenticated ─────────────────────────────────────
        with st.sidebar:
            st.markdown("---")
            st.markdown(
                f"👤 **{st.session_state.get('name', 'User')}**"
            )
            authenticator.logout("🚪 Logout", "sidebar")

        # Save config in case passwords were hashed on first login
        save_auth_config(config)
        return True

    elif auth_status is False:
        st.error("❌ Username atau password salah.")
        return False

    elif auth_status is None:
        # ── Show branded login page ───────────────────────────
        st.markdown(
            """
            <div style="text-align: center; padding: 2rem 0;">
                <h2 style="color: #1E88E5;">🏢 Asset Survey Automator</h2>
                <p style="color: #999; font-size: 0.95rem;">
                    Departemen Manajemen Aset — PT Petrokimia Gresik
                </p>
                <p style="color: #666; font-size: 0.85rem;">
                    Silakan login untuk melanjutkan
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return False
