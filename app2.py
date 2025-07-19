import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from googleapiclient.discovery import build

def get_transcript_with_youtube_api(video_id):
    youtube = build('youtube', 'v3', developerKey=os.getenv("YOUTUBE_API_KEY"))
    
    # First check if captions are available
    captions = youtube.captions().list(
        part="snippet",
        videoId=video_id
    ).execute()
    
    if not captions.get('items'):
        return None
    
    # Then fetch the transcript (this part is more complex)
    # Note: Downloading actual captions requires OAuth and additional permissions
    # You might need to combine with the transcript API
# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Constants ---
DEFAULT_PROMPT = """
You are a YouTube video summarizer. Given a transcript, generate a structured summary with:
- Key points (bullet points)
- Important examples (if any)
- Actionable insights (if applicable)
Keep the summary under 250 words. Transcript:
"""

# --- Helper Functions ---
def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "embed/" in url:
        return url.split("embed/")[1].split("?")[0]
    return None

@st.cache_data(show_spinner=False)
def extract_transcript_details(youtube_video_url: str) -> str:
    """Fetch and concatenate YouTube transcript with error handling."""
    try:
        video_id = extract_video_id(youtube_video_url)
        if not video_id:
            st.error("❌ Invalid YouTube URL. Please check the link format.")
            return None
        
        # List of fallback proxies (rotate through these)
        proxy_list = [
            {'http': 'http://138.199.48.1:8443', 'https': 'http://138.199.48.1:8443'},
            {'http': 'http://209.126.6.159:80', 'https': 'http://209.126.6.159:80'},
            # Add more proxies here
            None  # Last resort try without proxy
        ]
        
        for proxy in proxy_list:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxy)
                return " ".join([t["text"] for t in transcript])
            except:
                continue  # Try next proxy
        
        # If all proxies fail, try direct
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])
    
    except (TranscriptsDisabled, NoTranscriptFound):
        st.error("🔇 No transcript available for this video.")
        return None
    except Exception as e:
        st.error(f"⚠️ Error fetching transcript: {str(e)}")
        return None

@st.cache_data(show_spinner=False)
def generate_gemini_content(transcript_text: str, prompt: str) -> str:
    """Generate summary using Gemini with error handling."""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-002")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"⚠️ Gemini API error: {str(e)}")
        return None

# --- Streamlit UI ---
st.set_page_config(page_title="YouTube Summarizer Pro", page_icon="📝")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("🔑 Google API Key", 
                          value=os.getenv("GOOGLE_API_KEY", ""),
                          type="password",
                          help="Overrides .env if provided")
    
    if api_key:
        genai.configure(api_key=api_key)
    
    summary_length = st.selectbox(
        "📏 Summary Length",
        ["Short (100 words)", "Medium (250 words)", "Detailed (500 words)"],
        index=1
    )
    
    st.markdown("---")
    st.markdown("🛠️ Made with [Gemini](https://ai.google.dev/) & [Streamlit](https://streamlit.io/)")

# Main interface
st.title("🎬 YouTube Video Summarizer Pro")
st.caption("Transform long videos into concise notes with AI")

# URL input with validation
youtube_link = st.text_input(
    "🔗 Paste YouTube URL",
    placeholder="https://www.youtube.com/watch?v=...",
    help="Supports regular links and youtu.be shortcuts"
)

# Dynamic prompt based on user selection
prompt = DEFAULT_PROMPT
if summary_length == "Short (100 words)":
    prompt = prompt.replace("250 words", "100 words")
elif summary_length == "Detailed (500 words)":
    prompt = prompt.replace("250 words", "500 words")

# Show video thumbnail if URL is valid
if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        try:
            st.image(
                f"http://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
                use_container_width=True,
                caption="Video Thumbnail"
            )
        except:
            st.image(
                f"http://img.youtube.com/vi/{video_id}/0.jpg",
                use_column_width=True,
                caption="Video Thumbnail (Fallback)"
            )

# Process when button is clicked
if st.button("✨ Generate Summary", type="primary"):
    if not youtube_link:
        st.warning("Please enter a YouTube URL")
    else:
        with st.status("🔍 Processing video...", expanded=True) as status:
            # Step 1: Get transcript
            st.write("📜 Fetching transcript...")
            transcript_text = extract_transcript_details(youtube_link)
            
            if transcript_text:
                # Step 2: Generate summary
                st.write("🧠 Generating AI summary...")
                summary = generate_gemini_content(transcript_text, prompt)
                
                status.update(label="✅ Processing complete!", state="complete")
                
                if summary:
                    # Display results
                    st.subheader("📋 Summary")
                    st.markdown(summary)
                    
                    # Download options
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📥 Download Summary",
                            data=summary,
                            file_name="youtube_summary.txt",
                            mime="text/plain"
                        )
                    with col2:
                        if st.button("🔄 Generate Again"):
                            st.cache_data.clear()
                            st.rerun()

# Footer
st.markdown("---")
st.caption("💡 Tip: For long videos (>30 mins), the transcript might be truncated due to API limits.")
