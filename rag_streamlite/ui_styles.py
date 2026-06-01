import streamlit as st


def inject_css():
    """Inject all custom CSS styles into the Streamlit app."""
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --sapphire:       #1a3a6b;
    --sapphire-light: #2a5aaa;
    --sapphire-pale:  #e8f0fb;
    --gold:           #c9a84c;
    --gold-light:     #f0d990;
    --surface:        #f7f9fc;
    --border:         #d4dde8;
    --text:           #1a2332;
    --muted:          #6b7c93;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

.stApp { background: var(--surface); }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--sapphire) !important;
    border-right: 3px solid var(--gold);
}
[data-testid="stSidebar"] * { color: #e8f0fb !important; }
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stTextArea textarea {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(201,168,76,0.4) !important;
    color: white !important;
    border-radius: 6px;
}
[data-testid="stSidebar"] label {
    color: var(--gold-light) !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Header ── */
.app-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 24px 0 8px 0;
    border-bottom: 2px solid var(--border);
    margin-bottom: 28px;
}
.app-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: var(--sapphire);
    margin: 0;
    letter-spacing: -0.02em;
}
.app-header .tagline {
    font-size: 0.85rem;
    color: var(--muted);
    margin: 0;
    letter-spacing: 0.04em;
}

/* ── Cards ── */
.card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(26,58,107,0.06);
}
.card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: var(--sapphire);
    margin: 0 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--sapphire-pale);
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Step Badge ── */
.step-badge {
    background: var(--gold);
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── Status Pills ── */
.status-success {
    display: inline-flex; align-items: center; gap: 6px;
    background: #e6f4ea; color: #1e7e34;
    padding: 6px 14px; border-radius: 20px;
    font-size: 0.82rem; font-weight: 600;
    border: 1px solid #b8dfc2;
}
.status-error {
    display: inline-flex; align-items: center; gap: 6px;
    background: #fde8e8; color: #c0392b;
    padding: 6px 14px; border-radius: 20px;
    font-size: 0.82rem; font-weight: 600;
    border: 1px solid #f5c6c6;
}

/* ── Buttons ── */
.stButton button {
    background: var(--sapphire) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    box-shadow: 0 3px 10px rgba(26,58,107,0.25);
    transition: all 0.2s ease;
}
.stButton button:hover {
    background: var(--sapphire-light) !important;
    box-shadow: 0 5px 16px rgba(26,58,107,0.35) !important;
    transform: translateY(-1px);
}
.primary-btn button {
    background: linear-gradient(135deg, var(--sapphire), var(--sapphire-light)) !important;
    font-size: 1rem !important;
    padding: 12px 32px !important;
}

/* ── Answer Box ── */
.answer-box {
    background: white;
    border: 1px solid var(--border);
    border-left: 4px solid var(--gold);
    border-radius: 8px;
    padding: 20px 24px;
    white-space: pre-wrap;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    line-height: 1.7;
    color: var(--text);
    max-height: 500px;
    overflow-y: auto;
}

/* ── Email Chip ── */
.email-chip {
    display: inline-block;
    background: var(--sapphire-pale);
    color: var(--sapphire);
    border: 1px solid #bfd0ef;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 3px 3px 3px 0;
}

/* ── Misc ── */
.section-divider { border: none; border-top: 1px solid var(--border); margin: 24px 0; }
.help-text       { font-size: 0.75rem; color: var(--muted); margin-top: 4px; font-style: italic; }
</style>
""", unsafe_allow_html=True)
