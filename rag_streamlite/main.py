import os
from pathlib import Path
from dotenv import load_dotenv

import streamlit as st

from ui_styles import inject_css
from rag_engine import run_pipeline
from gmail_tool import send_email_smtp
from prompt import DEFAULT_QUERY
from email_config import TO, CC, BCC, SUBJECT

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# ─────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Sapphire RAG Mail",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ─────────────────────────────────────────
# Header
# ─────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div>
        <h1>💎 Sapphire RAG Mail</h1>
        <p class="tagline">AI-powered issue analysis &amp; automated email dispatch</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# Sidebar — Configuration
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    st.markdown("**🔑 API Keys**")
    groq_key = st.text_input(
        "Groq API Key",
        value=os.getenv("GROQ_API_KEY", ""),
        type="password",
        placeholder="gsk_..."
    )

    st.markdown("---")
    st.markdown("**📤 SMTP Sender**")
    sender_email = st.text_input(
        "Sender Email",
        value=os.getenv("SENDER_EMAIL", ""),
        placeholder="you@gmail.com"
    )
    sender_password = st.text_input(
        "App Password",
        value=os.getenv("SENDER_PASSWORD", ""),
        type="password",
        placeholder="xxxx xxxx xxxx xxxx"
    )

    st.markdown("---")
    st.markdown("**🤖 Model Settings**")
    temperature   = st.slider("Temperature",   0.0,  1.0, 0.4, 0.05)
    chunk_size    = st.number_input("Chunk Size",    200, 2000, 500, 50)
    chunk_overlap = st.number_input("Chunk Overlap",   0,  200,  50, 10)

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.7rem;color:rgba(255,255,255,0.4);text-align:center;'>"
        "Powered by Groq · LangChain · ChromaDB</div>",
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────
# Session State Init
# ─────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

# ─────────────────────────────────────────
# Main Layout — Two Columns
# ─────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

# ── LEFT: Upload + Query ──────────────────
with col_left:
    st.markdown("""
    <div class="card">
        <div class="card-title"><span class="step-badge">Step 1</span> Upload Document</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a .txt file",
        type=["txt"],
        help="Upload the issues file you want to analyze"
    )

    if uploaded_file:
        st.markdown(
            f'<span class="status-success">✓ {uploaded_file.name} &nbsp;·&nbsp; {uploaded_file.size:,} bytes</span>',
            unsafe_allow_html=True
        )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card-title"><span class="step-badge">Step 2</span> Query</div>
    """, unsafe_allow_html=True)

    query = st.text_area(
        "What do you want to ask?",
        value=DEFAULT_QUERY,
        height=100,
        help="This query will be run against the uploaded document"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    analyze_clicked = st.button(
        "🔍 Analyze Document",
        use_container_width=True,
        disabled=(uploaded_file is None)
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is None:
        st.markdown('<p class="help-text">⬆ Upload a .txt file to enable analysis</p>', unsafe_allow_html=True)


# ── RIGHT: Email Config ───────────────────
with col_right:
    st.markdown("""
    <div class="card">
        <div class="card-title"><span class="step-badge">Step 3</span> Email Recipients</div>
    </div>
    """, unsafe_allow_html=True)

    subject = st.text_input(
        "📌 Subject",
        value=SUBJECT,
        placeholder="Enter email subject"
    )

    to_raw = st.text_area(
        "📨 To (required)",
        value=", ".join(TO),
        height=80,
        placeholder="email1@example.com, email2@example.com",
        help="Comma-separated list of primary recipients"
    )

    cc_raw = st.text_area(
        "📋 CC (optional)",
        value=", ".join(CC),
        height=60,
        placeholder="cc1@example.com, cc2@example.com",
        help="Comma-separated list of CC recipients"
    )

    bcc_raw = st.text_area(
        "🔒 BCC (optional)",
        value=", ".join(BCC),
        height=60,
        placeholder="bcc@example.com",
        help="Comma-separated list of BCC recipients"
    )

    # ── Parse & Preview email chips ──────────
    def parse_emails(raw: str) -> list:
        return [e.strip() for e in raw.split(",") if e.strip() and "@" in e]

    to_list  = parse_emails(to_raw)
    cc_list  = parse_emails(cc_raw)
    bcc_list = parse_emails(bcc_raw)

    if to_list or cc_list or bcc_list:
        preview_html = "<div style='margin-top:12px;'>"
        if to_list:
            preview_html += "<span style='font-size:0.75rem;color:#6b7c93;font-weight:600;'>TO &nbsp;</span>"
            preview_html += "".join(f'<span class="email-chip">{e}</span>' for e in to_list)
            preview_html += "<br style='margin:4px 0'>"
        if cc_list:
            preview_html += "<span style='font-size:0.75rem;color:#6b7c93;font-weight:600;'>CC &nbsp;</span>"
            preview_html += "".join(f'<span class="email-chip">{e}</span>' for e in cc_list)
            preview_html += "<br style='margin:4px 0'>"
        if bcc_list:
            preview_html += "<span style='font-size:0.75rem;color:#6b7c93;font-weight:600;'>BCC &nbsp;</span>"
            preview_html += "".join(f'<span class="email-chip">{e}</span>' for e in bcc_list)
        preview_html += "</div>"
        st.markdown(preview_html, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Step 4: Run RAG Pipeline
# ─────────────────────────────────────────
if analyze_clicked and uploaded_file is not None:
    st.session_state.email_sent = False
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    progress = st.progress(0, text="📥 Reading document…")

    progress.progress(15, text="✂️ Splitting into chunks…")
    progress.progress(35, text="🔢 Building embeddings…")
    progress.progress(60, text="🤖 Querying Groq LLM…")

    result, num_chunks = run_pipeline(
        file_bytes=uploaded_file.read(),
        query=query,
        groq_api_key=groq_key or os.getenv("GROQ_API_KEY"),
        temperature=temperature,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    progress.progress(100, text=f"✅ Done! ({num_chunks} chunks processed)")
    st.session_state.result = result

# ─────────────────────────────────────────
# Step 5: Show Result
# ─────────────────────────────────────────
if st.session_state.result:
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card-title"><span class="step-badge">Result</span> AI-Generated Answer</div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="answer-box">{st.session_state.result}</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col_dl, col_send = st.columns([1, 1])

    with col_dl:
        st.download_button(
            "⬇️ Download Answer (.txt)",
            data=st.session_state.result,
            file_name="sapphire_analysis.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col_send:
        send_clicked = st.button("📧 Send Email Now", use_container_width=True)

# ─────────────────────────────────────────
# Step 6: Send Email
# ─────────────────────────────────────────
    if send_clicked:
        errors = []
        if not to_list:        errors.append("At least one **To** recipient is required.")
        if not sender_email:   errors.append("Sender email not set — check sidebar.")
        if not sender_password:errors.append("App password not set — check sidebar.")
        if not subject.strip():errors.append("Subject cannot be empty.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            with st.spinner("Sending email…"):
                success, message = send_email_smtp(
                    to=", ".join(to_list),
                    subject=subject,
                    message=st.session_state.result,
                    cc=", ".join(cc_list),
                    bcc=", ".join(bcc_list),
                    sender_email=sender_email,
                    sender_password=sender_password,
                )

            if success:
                st.session_state.email_sent = True
                st.success(f"✅ {message}")
                st.balloons()
            else:
                st.error(f"❌ {message}")
