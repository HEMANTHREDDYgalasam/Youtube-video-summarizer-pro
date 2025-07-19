import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Improved prompt
PROMPT = """
You are a YouTube video summarizer. Given a transcript, generate a structured summary with:
- Key points (bullet points)
- Important examples (if any)
- Actionable insights (if applicable)
Keep the summary under 250 words. Transcript:
"""

# Extract YouTube video ID
def extract_video_id(url):
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "v=" in url:
        return url.split("v=")[1].split("&")[0]
    return None

# Fetch transcript with error handling
@st.cache_data
def extract_transcript_details(youtube_video_url):
    try:
        video_id = extract_video_id(youtube_video_url)
        if not video_id:
            st.error("Invalid YouTube URL. Please check the link.")
            return None
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])
    
    except Exception as e:
        st.error(f"Error fetching transcript: {str(e)}")
        return None

# Generate summary with caching
@st.cache_data
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro-002")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit UI
st.title("YouTube Video Summarizer")
youtube_link = st.text_input("Enter YouTube Video URL:")

if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Summary"):
    if not youtube_link:
        st.warning("Please enter a YouTube URL.")
    else:
        with st.spinner("Fetching transcript..."):
            transcript_text = extract_transcript_details(youtube_link)
        
        if transcript_text:
            with st.spinner("Generating summary..."):
                summary = generate_gemini_content(transcript_text, PROMPT)
            
            st.subheader("Summary")
            st.write(summary)
            
            st.download_button(
                label="Download Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain"
            )
