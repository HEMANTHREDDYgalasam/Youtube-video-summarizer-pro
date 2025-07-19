# **YouTube Video Summarizer Pro** 📝🎬  
**AI-powered tool to convert YouTube videos into concise summaries.**  

## **Table of Contents**  
1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Installation](#installation)  
4. [Configuration](#configuration)  
5. [Usage](#usage)  
6. [API Reference](#api-reference)  
7. [Error Handling](#error-handling)  
8. [Deployment](#deployment)  
9. [Limitations](#limitations)  
10. [Future Improvements](#future-improvements)  

---

## **1. Project Overview**  
This tool extracts transcripts from YouTube videos and Generates AI-powered summaries using **Google's Gemini Pro** model. Built with:  
- **Python** (Backend logic)  
- **Streamlit** (Web interface)  
- **YouTube Transcript API** (Transcript extraction)  
- **Google Generative AI** (Text summarization)  

**Use Cases**:  
✔ Students summarizing lectures  
✔ Professionals extracting insights from talks  
✔ Content creators repurposing videos  

---

## **2. Features**  
✅ **Smart URL Handling** - Supports multiple YouTube URL formats  
✅ **Adjustable Summary Length** - Short (100 words), Medium (250), or Detailed (500)  
✅ **Video Thumbnail Display** - Shows video preview  
✅ **Downloadable Summaries** - Save as `.txt` files  
✅ **Error Resilient** - Handles missing transcripts/API failures  
✅ **Caching** - Avoids reprocessing the same video  

---

## **3. Installation**  

### **Prerequisites**  
- Python 3.10+  
- Google API Key ([Get it here](https://ai.google.dev/))  

### **Steps**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-repo/youtube-summarizer.git
   cd youtube-summarizer
   ```

2. Create a virtual environment:  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file:  
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

---

## **4. Configuration**  
Configure via:  
1. **Environment Variables** (`.env` file):  
   ```env
   GOOGLE_API_KEY=your_key_here
   ```

2. **Streamlit UI** (Override in sidebar):  
   ![Settings Screenshot](https://i.imgur.com/settings_ui.png)  

---

## **5. Usage**  
1. Run the app:  
   ```bash
   streamlit run app.py
   ```

2. **Input a YouTube URL**:  
   ```
   https://www.youtube.com/watch?v=example123
   ```

3. **Select summary length** (Short/Medium/Detailed).  

4. Click **"Generate Summary"**.  

5. **Download** or regenerate as needed.  

---

## **6. API Reference**  

### **Functions**  
| Function | Description |
|----------|-------------|
| `extract_video_id(url)` | Extracts video ID from URLs (supports `youtu.be`, `embed/`, etc.) |
| `extract_transcript_details(url)` | Fetches transcript with error handling |
| `generate_gemini_content(text, prompt)` | Generates summary using Gemini Pro |

### **Environment Variables**  
| Variable | Purpose |
|----------|---------|
| `GOOGLE_API_KEY` | Authenticates Gemini API requests |

---

## **7. Error Handling**  
The app catches:  
- ❌ Invalid YouTube URLs  
- 🔇 Videos without transcripts  
- ⚠️ API quota limits  
- 🌐 Network errors  

**Example error message**:  
![Error Screenshot](https://i.imgur.com/error_ui.png)  

---

## **8. Deployment**  
### **Option A: Streamlit Sharing**  
1. Push code to GitHub.  
2. Deploy via [Streamlit Community Cloud](https://share.streamlit.io/).  

### **Option B: Docker**  
```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```
Build and run:  
```bash
docker build -t youtube-summarizer .
docker run -p 8501:8501 youtube-summarizer
```

---

## **9. Limitations**  
- ⏳ Transcripts limited to ~30 mins (YouTube API constraint)  
- 🔐 Requires Google API key  
- 📜 No support for auto-generated captions  

---

## **10. Future Improvements**  
- 🕒 Timestamp-based summaries ("What’s covered at 5:30?")  
- 🌍 Multilingual support  
- 📊 Sentiment analysis of video content  

---

**License**: MIT  
**Author**: Jaswanth  
**Feedback**: jaswanthmemories@example.com  

--- 
