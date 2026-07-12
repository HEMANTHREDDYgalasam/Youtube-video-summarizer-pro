# ==============================================================================
# app.py — YouTube Video Summarizer Pro
# Author  : Hemanth Reddy
# Run     : streamlit run app.py
# ==============================================================================

from __future__ import annotations

import os
import time

import streamlit as st
from dotenv import load_dotenv

from utils import (
    SUMMARY_PROMPTS,
    compute_stats,
    export_as_docx,
    export_as_pdf,
    export_as_txt,
    fetch_transcript,
    format_reading_time,
    generate_summary,
    get_thumbnail_url,
    extract_video_id,
)

# ─────────────────────────────────────────────────────────────────────────────
# Bootstrap — Load API key from environment (never exposed to the user)
# ─────────────────────────────────────────────────────────────────────────────

load_dotenv(override=True)  # Load .env file with override=True to support updates

GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

# ─────────────────────────────────────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="YouTube Video Summarizer Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/hemanthreddy/yt-summarizer-pro",
        "Report a bug": "https://github.com/hemanthreddy/yt-summarizer-pro/issues",
        "About": "YouTube Video Summarizer Pro — Built by Hemanth Reddy",
    },
)

# ─────────────────────────────────────────────────────────────────────────────
# Global CSS — Dark Premium Theme
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
    /* ── Google Font ──────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Root variables ───────────────────────────────── */
    :root {
        --accent:        #6C63FF;
        --accent-light:  #8B85FF;
        --accent-dark:   #4A43CC;
        --success:       #00C896;
        --warning:       #FFB347;
        --danger:        #FF6B6B;
        --bg-primary:    #0D0F1A;
        --bg-card:       #131629;
        --bg-card2:      #1A1E35;
        --bg-input:      #1E2240;
        --text-primary:  #E8EAFF;
        --text-secondary:#9BA3CC;
        --border:        #2A2F52;
        --radius:        14px;
        --radius-sm:     8px;
        --shadow:        0 8px 32px rgba(108,99,255,0.18);
    }

    /* ── Base ─────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }

    /* ── App container ────────────────────────────────── */
    .stApp {
        background: linear-gradient(135deg, #0D0F1A 0%, #131629 50%, #0F1221 100%) !important;
    }

    /* ── Sidebar ──────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: var(--bg-card) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }

    /* ── Inputs ───────────────────────────────────────── */
    .stTextInput > div > div > input {
        background-color: var(--bg-input) !important;
        border: 1.5px solid var(--border) !important;
        color: var(--text-primary) !important;
        border-radius: var(--radius-sm) !important;
        font-size: 15px !important;
        padding: 12px 16px !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(108,99,255,0.25) !important;
        outline: none !important;
    }

    /* ── Buttons ──────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 10px 28px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.4px !important;
        cursor: pointer !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(108,99,255,0.35) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(108,99,255,0.5) !important;
        opacity: 0.95 !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── Download buttons ─────────────────────────────── */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #1A1E35 0%, #2A2F52 100%) !important;
        color: var(--accent-light) !important;
        border: 1.5px solid var(--accent) !important;
        border-radius: 50px !important;
        padding: 8px 22px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
    }
    .stDownloadButton > button:hover {
        background: var(--accent) !important;
        color: #fff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(108,99,255,0.4) !important;
    }

    /* ── Selectbox / Radio ────────────────────────────── */
    .stSelectbox > div > div {
        background-color: var(--bg-input) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
    }

    /* ── Cards ────────────────────────────────────────── */
    .summary-card {
        background: var(--bg-card2);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 28px 32px;
        margin-top: 20px;
        box-shadow: var(--shadow);
        animation: fadeInUp 0.5s ease both;
    }

    .metric-card {
        background: var(--bg-card2);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        transition: transform 0.2s ease;
    }
    .metric-card:hover { transform: translateY(-3px); }
    .metric-card .metric-value {
        font-size: 26px;
        font-weight: 800;
        color: var(--accent-light);
    }
    .metric-card .metric-label {
        font-size: 12px;
        color: var(--text-secondary);
        margin-top: 4px;
        font-weight: 500;
    }

    /* ── Section headings ─────────────────────────────── */
    .section-title {
        font-size: 13px;
        font-weight: 700;
        color: var(--accent-light);
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 12px;
    }

    /* ── Video info banner ────────────────────────────── */
    .video-info-banner {
        background: linear-gradient(135deg, #131629 0%, #1A1E35 100%);
        border: 1px solid var(--border);
        border-left: 4px solid var(--accent);
        border-radius: var(--radius);
        padding: 16px 20px;
        margin: 16px 0;
    }

    /* ── Hero header ──────────────────────────────────── */
    .hero-header {
        text-align: center;
        padding: 40px 20px 20px;
    }
    .hero-header h1 {
        font-size: 44px;
        font-weight: 800;
        background: linear-gradient(135deg, var(--accent-light) 0%, #A78BFA 50%, #60A5FA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
        line-height: 1.2;
    }
    .hero-header p {
        color: var(--text-secondary);
        font-size: 16px;
        font-weight: 400;
        max-width: 560px;
        margin: 0 auto;
    }

    /* ── Badge ────────────────────────────────────────── */
    .badge {
        display: inline-block;
        background: rgba(108,99,255,0.18);
        color: var(--accent-light);
        border: 1px solid rgba(108,99,255,0.35);
        border-radius: 50px;
        padding: 4px 14px;
        font-size: 12px;
        font-weight: 600;
        margin: 4px 4px 4px 0;
    }

    /* ── Summary text ─────────────────────────────────── */
    .summary-text {
        font-size: 15.5px;
        line-height: 1.85;
        color: var(--text-primary);
        letter-spacing: 0.1px;
    }

    /* ── Divider ──────────────────────────────────────── */
    .custom-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 24px 0;
    }

    /* ── Footer ───────────────────────────────────────── */
    .app-footer {
        text-align: center;
        padding: 32px 20px 20px;
        color: var(--text-secondary);
        font-size: 13px;
        border-top: 1px solid var(--border);
        margin-top: 48px;
    }
    .app-footer strong { color: var(--accent-light); }

    /* ── Spinner override ─────────────────────────────── */
    .stSpinner > div { border-top-color: var(--accent) !important; }

    /* ── Animations ───────────────────────────────────── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0);    }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.6; }
    }

    /* ── Hide Streamlit branding ──────────────────────── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* ── Notification overrides ───────────────────────── */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: var(--radius-sm) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# Session State Initialisation
# ─────────────────────────────────────────────────────────────────────────────

_defaults: dict = {
    "summary": None,
    "transcript": None,
    "video_id": None,
    "video_url": None,
    "lang_code": None,
    "gen_time": None,
    "summary_mode": None,
    "stats": None,
}
for key, value in _defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding: 10px 0 20px;">
            <div style="font-size:48px; margin-bottom:8px;">🎬</div>
            <div style="font-size:18px; font-weight:800; color:#8B85FF;">YT Summarizer Pro</div>
            <div style="font-size:12px; color:#9BA3CC; margin-top:4px;">AI-Powered · Gemini 2.0 Flash</div>
        </div>
        <hr style="border:none;height:1px;background:linear-gradient(90deg,transparent,#2A2F52,transparent);margin:0 0 20px;">
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">⚙️ Summary Settings</div>', unsafe_allow_html=True)

    summary_mode = st.selectbox(
        "Summary Length",
        options=list(SUMMARY_PROMPTS.keys()),
        index=1,
        help="Choose how detailed the AI summary should be.",
        key="mode_select",
    )

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">🎨 Theme</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size:13px;color:#9BA3CC;line-height:1.7;">
            <span class="badge">🌑 Dark Mode</span>
            <span class="badge" style="background:rgba(108,99,255,0.18);color:#A78BFA;">Glassmorphism</span>
            <span class="badge">✨ Animated</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">ℹ️ About</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size:12.5px; color:#9BA3CC; line-height:1.8;">
            <b style="color:#E8EAFF;">YouTube Video Summarizer Pro</b><br>
            Paste any YouTube URL to instantly get an AI-powered summary.<br><br>
            <b style="color:#8B85FF;">Powered by:</b><br>
            🤖 Gemini 2.0 Flash<br>
            🎙️ YouTube Transcript API<br>
            ⚡ Streamlit<br><br>
            <b style="color:#8B85FF;">Creator:</b><br>
            👨‍💻 Hemanth Reddy
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# Hero Header
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
    """
    <div class="hero-header">
        <h1>🎬 YouTube Video Summarizer Pro</h1>
        <p>Instantly transform any YouTube video into a concise, AI-powered summary using <strong>Gemini 2.0 Flash</strong></p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# URL Input Section
# ─────────────────────────────────────────────────────────────────────────────

col_url, col_btn = st.columns([5, 1], vertical_alignment="bottom")

with col_url:
    youtube_url = st.text_input(
        "YouTube URL",
        placeholder="🔗  Paste a YouTube video URL here…  e.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        label_visibility="collapsed",
        key="url_input",
    )

with col_btn:
    summarize_btn = st.button("✨ Summarize", use_container_width=True, key="summarize_btn")

# ── Action row ──────────────────────────────────────────────────────────────

col_a, col_b, col_c = st.columns([1, 1, 4])

with col_a:
    clear_btn = st.button("🗑️ Clear", use_container_width=True, key="clear_btn")

with col_b:
    regen_btn = st.button("🔄 Regenerate", use_container_width=True, key="regen_btn")

# ── Clear handler ────────────────────────────────────────────────────────────

if clear_btn:
    for key in _defaults:
        st.session_state[key] = None
    st.rerun()

# ── Regenerate handler (reuse stored data) ───────────────────────────────────

if regen_btn and st.session_state.get("transcript"):
    load_dotenv(override=True)
    api_key_to_use = os.getenv("GOOGLE_API_KEY", "")
    if not api_key_to_use:
        st.error("⚙️ Server configuration error. Please contact the administrator.")
    else:
        with st.spinner("🔄 Regenerating summary with Gemini AI…"):
            try:
                new_summary, gen_time = generate_summary(
                    st.session_state["transcript"],
                    summary_mode,
                    api_key_to_use,
                )
                st.session_state["summary"] = new_summary
                st.session_state["gen_time"] = gen_time
                st.session_state["summary_mode"] = summary_mode
                st.session_state["stats"] = compute_stats(new_summary)
                st.success("✅ Summary regenerated successfully!")
            except ValueError as err:
                st.error(str(err))

# ─────────────────────────────────────────────────────────────────────────────
# Main Summarise Flow
# ─────────────────────────────────────────────────────────────────────────────

if summarize_btn:
    # ── Validation ──────────────────────────────────────────────────────────
    if not youtube_url.strip():
        st.error("❌ Please paste a YouTube URL to get started.")
        st.stop()

    load_dotenv(override=True)
    api_key_to_use = os.getenv("GOOGLE_API_KEY", "")
    if not api_key_to_use:
        st.error("⚙️ Server configuration error. Please contact the administrator.")
        st.stop()

    video_id = extract_video_id(youtube_url.strip())
    if not video_id:
        st.error(
            "❌ Invalid YouTube URL. Please check the URL format.\n\n"
            "**Supported formats:**\n"
            "- `https://www.youtube.com/watch?v=VIDEO_ID`\n"
            "- `https://youtu.be/VIDEO_ID`\n"
            "- `https://youtube.com/shorts/VIDEO_ID`"
        )
        st.stop()

    # ── Fetch transcript ─────────────────────────────────────────────────────
    with st.spinner("📄 Fetching video transcript…"):
        try:
            transcript_text, lang_code = fetch_transcript(video_id)
        except ValueError as err:
            st.error(str(err))
            st.stop()
        except Exception as exc:
            st.error(f"❌ Unexpected error while fetching transcript: {exc}")
            st.stop()

    # ── Generate summary ─────────────────────────────────────────────────────
    with st.spinner("🤖 Generating AI summary with Gemini AI…"):
        try:
            summary_text, gen_time = generate_summary(
                transcript_text,
                summary_mode,
                api_key_to_use,
            )
        except ValueError as err:
            st.error(str(err))
            st.stop()
        except Exception as exc:
            st.error(f"❌ Unexpected error during AI generation: {exc}")
            st.stop()

    # ── Persist to session state ─────────────────────────────────────────────
    st.session_state["summary"] = summary_text
    st.session_state["transcript"] = transcript_text
    st.session_state["video_id"] = video_id
    st.session_state["video_url"] = youtube_url.strip()
    st.session_state["lang_code"] = lang_code
    st.session_state["gen_time"] = gen_time
    st.session_state["summary_mode"] = summary_mode
    st.session_state["stats"] = compute_stats(summary_text)

    st.success("✅ Summary generated successfully!")

# ─────────────────────────────────────────────────────────────────────────────
# Results Display
# ─────────────────────────────────────────────────────────────────────────────

if st.session_state.get("summary"):
    summary = st.session_state["summary"]
    video_id = st.session_state["video_id"]
    video_url = st.session_state["video_url"]
    lang_code = st.session_state["lang_code"]
    gen_time = st.session_state["gen_time"]
    mode = st.session_state["summary_mode"]
    stats = st.session_state["stats"]

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ── Layout: Thumbnail | Info ─────────────────────────────────────────────
    col_thumb, col_info = st.columns([2, 3], gap="large")

    with col_thumb:
        thumb_url = get_thumbnail_url(video_id)
        st.markdown(
            f"""
            <div style="border-radius:{14}px; overflow:hidden;
                        box-shadow: 0 8px 32px rgba(108,99,255,0.25);
                        border: 1px solid #2A2F52;">
                <img src="{thumb_url}" style="width:100%; display:block;"
                     alt="Video Thumbnail" />
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_info:
        st.markdown(
            f"""
            <div class="video-info-banner">
                <div style="font-size:13px; color:#9BA3CC; margin-bottom:10px;">
                    🔗 <a href="{video_url}" target="_blank"
                         style="color:#8B85FF; text-decoration:none;">
                        Open in YouTube ↗
                    </a>
                </div>
                <div style="margin-bottom:8px;">
                    <span class="badge">🌐 Language: {lang_code.upper()}</span>
                    <span class="badge">📝 Mode: {mode}</span>
                </div>
                <div style="font-size:13px; color:#9BA3CC; margin-top:8px;">
                    🤖 Powered by <strong style="color:#8B85FF;">Gemini 2.0 Flash</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Metrics ──────────────────────────────────────────────────────────
        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">📝 {stats['word_count']}</div>
                    <div class="metric-label">Words</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m2:
            reading_time_str = format_reading_time(stats["reading_time_seconds"])
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">⏱️ {reading_time_str}</div>
                    <div class="metric-label">Read Time</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m3:
            gen_time_str = f"{gen_time:.1f}s"
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">⚡ {gen_time_str}</div>
                    <div class="metric-label">Gen. Time</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Summary Card ─────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="summary-card">
            <div class="section-title">📄 AI-Generated Summary</div>
            <div class="summary-text">{summary.replace(chr(10), '<br>')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Copy to Clipboard ────────────────────────────────────────────────────
    st.markdown('<div style="margin-top:16px;"></div>', unsafe_allow_html=True)

    copy_col, _ = st.columns([1, 3])
    with copy_col:
        if st.button("📋 Copy Summary", key="copy_btn", use_container_width=True):
            # Use JavaScript clipboard API via a hidden component
            escaped = summary.replace("\\", "\\\\").replace("`", "\\`").replace('"', '\\"').replace("'", "\\'")
            st.markdown(
                f"""
                <script>
                navigator.clipboard.writeText(`{escaped}`)
                    .then(() => console.log("Copied!"))
                    .catch(err => console.error("Copy failed:", err));
                </script>
                """,
                unsafe_allow_html=True,
            )
            st.success("✅ Summary copied to clipboard!")

    # ── Download Section ─────────────────────────────────────────────────────
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⬇️ Download Summary</div>', unsafe_allow_html=True)

    dl_col1, dl_col2, dl_col3 = st.columns(3)

    with dl_col1:
        txt_bytes = export_as_txt(summary, video_url, mode)
        st.download_button(
            label="📄 Download TXT",
            data=txt_bytes,
            file_name=f"summary_{video_id}.txt",
            mime="text/plain",
            use_container_width=True,
            key="dl_txt",
        )

    with dl_col2:
        pdf_bytes = export_as_pdf(summary, video_url, mode)
        st.download_button(
            label="📕 Download PDF",
            data=pdf_bytes,
            file_name=f"summary_{video_id}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="dl_pdf",
        )

    with dl_col3:
        docx_bytes = export_as_docx(summary, video_url, mode)
        st.download_button(
            label="📘 Download DOCX",
            data=docx_bytes,
            file_name=f"summary_{video_id}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
            key="dl_docx",
        )

    # ── Transcript Expander ──────────────────────────────────────────────────
    with st.expander("📜 View Full Transcript", expanded=False):
        transcript_text = st.session_state["transcript"]
        st.markdown(
            f'<div style="max-height:400px; overflow-y:auto; font-size:13px; '
            f'color:#9BA3CC; line-height:1.8; padding:8px;">{transcript_text}</div>',
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────────────────────────
# Empty State
# ─────────────────────────────────────────────────────────────────────────────

elif not summarize_btn:
    st.markdown(
        """
        <div style="text-align:center; padding: 60px 20px; color:#9BA3CC;">
            <div style="font-size:64px; margin-bottom:16px;">🎥</div>
            <div style="font-size:20px; font-weight:600; color:#E8EAFF; margin-bottom:10px;">
                Ready to Summarize
            </div>
            <div style="font-size:14px; max-width:420px; margin:0 auto; line-height:1.8;">
                Paste any YouTube video URL above and hit <strong style="color:#8B85FF;">✨ Summarize</strong>
                to instantly get an AI-powered summary.
            </div>
            <div style="margin-top:28px;">
                <span class="badge">🎬 Any YouTube Video</span>
                <span class="badge">🤖 Gemini 2.0 Flash</span>
                <span class="badge">⚡ Instant Results</span>
                <span class="badge">📥 Download Ready</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
    """
    <div class="app-footer">
        Made with ❤️ by <strong>Hemanth Reddy</strong> &nbsp;|&nbsp;
        Powered by <strong>Gemini 2.0 Flash</strong> &amp; <strong>Streamlit</strong>
        &nbsp;|&nbsp; YouTube Video Summarizer Pro &copy; 2025
    </div>
    """,
    unsafe_allow_html=True,
)
