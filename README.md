# YouTube Video Summarizer Pro

<div align="center">

![YouTube Video Summarizer Pro](https://img.shields.io/badge/YouTube-Video%20Summarizer%20Pro-6C63FF?style=for-the-badge&logo=youtube&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00C896?style=for-the-badge)

**Transform any YouTube video into a concise AI-powered summary — instantly.**

[Features](#features) • [Tech Stack](#tech-stack) • [Installation](#installation) • [Usage](#usage) • [Screenshots](#screenshots)

</div>

---

## 📌 Project Overview

**YouTube Video Summarizer Pro** is a production-quality, AI-powered web application that automatically extracts the transcript from any YouTube video and generates a beautifully formatted summary using **Google Gemini 2.0 Flash**. Built with **Streamlit**, it features a stunning dark-mode UI, multiple export formats, and a seamless user experience.

Whether you're a student, researcher, content creator, or busy professional, this tool lets you consume hours of video content in minutes.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔗 **Smart URL Parsing** | Extracts video IDs from all YouTube URL formats |
| 🖼️ **Thumbnail Display** | Shows the video thumbnail above the summary |
| 📄 **Transcript Fetching** | Auto-fetches subtitles in English or any available language |
| 🤖 **AI Summarization** | Powered by Google Gemini 2.0 Flash |
| 📏 **3 Summary Modes** | Short (~100w), Medium (~250w), Detailed (~500w) |
| ⬇️ **Export Options** | Download as TXT, PDF, or DOCX |
| 📋 **Copy to Clipboard** | One-click copy of the full summary |
| 📊 **Live Metrics** | Word count, estimated reading time, generation time |
| 🔄 **Regenerate** | Re-run summarization without re-fetching the transcript |
| 🗑️ **Clear Session** | Reset the app to start fresh |
| 🚨 **Error Handling** | Graceful messages for private videos, missing captions, bad URLs, API errors |
| 🎨 **Premium Dark UI** | Glassmorphism cards, gradient text, micro-animations |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit (latest) |
| **Backend** | Python 3.13+ |
| **AI Model** | Google Gemini 2.0 Flash (`google-genai`) |
| **Transcripts** | `youtube-transcript-api` |
| **PDF Export** | `reportlab` |
| **DOCX Export** | `python-docx` |
| **Image Processing** | `Pillow` |
| **HTTP** | `requests` |
| **Config** | `python-dotenv` |

---

## 📦 Installation

### Prerequisites

- Python 3.13 or higher
- A **Google Gemini API Key** — get one free at [Google AI Studio](https://aistudio.google.com/)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/hemanthreddy/youtube-video-summarizer-pro.git
cd youtube-video-summarizer-pro

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Open .env and paste your GOOGLE_API_KEY
```

### Environment Setup

Edit the `.env` file:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

---

## 🚀 Run Commands

```bash
# Start the application
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

## 📁 Folder Structure

```
youtube-video-summarizer-pro/
│
├── app.py                  # Main Streamlit application
├── utils.py                # Helper functions (transcript, AI, export)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .env                    # Your API keys (not committed to git)
├── README.md               # Project documentation
│
├── assets/                 # Static assets (logos, icons)
└── downloads/              # Directory for downloaded summaries (auto-created)
```

---

## 🖥️ Screenshots

> _Screenshots will be added after first deployment._

| Home Screen | Summary View | Download Options |
|---|---|---|
| ![Home](assets/screenshot_home.png) | ![Summary](assets/screenshot_summary.png) | ![Download](assets/screenshot_download.png) |

---

## 📋 Usage Guide

1. **Open the app** at `http://localhost:8501`
2. **Enter your API key** in the sidebar (or set it in `.env`)
3. **Choose summary length** — Short, Medium, or Detailed
4. **Paste a YouTube URL** in the input field
5. **Click ✨ Summarize** — the app will:
   - Extract the video ID
   - Fetch the transcript
   - Generate an AI summary
   - Display the thumbnail, metrics, and formatted summary
6. **Download or copy** the summary in your preferred format

---

## ⚠️ Error Handling

The app handles the following edge cases gracefully:

| Error | Message Shown |
|---|---|
| Invalid URL | Clear format instructions with valid URL examples |
| Private / Deleted Video | `VideoUnavailable` caught with user-friendly message |
| Subtitles Disabled | `TranscriptsDisabled` caught with explanation |
| No Transcript Found | `NoTranscriptFound` caught with suggestion |
| Invalid API Key | API error parsed with clear remediation steps |
| Quota Exceeded | Rate limit error caught and explained |
| Network Issues | `requests.RequestException` caught gracefully |

---

## 🔮 Future Enhancements

- [ ] **Multi-language summaries** — Summarize in Spanish, French, Hindi, etc.
- [ ] **Playlist support** — Summarize entire YouTube playlists
- [ ] **Video chapters** — Generate chapter-by-chapter breakdowns
- [ ] **Speaker detection** — Identify and attribute speakers in transcripts
- [ ] **Summary history** — Save and search past summaries locally
- [ ] **Share link** — Generate a shareable link to any summary
- [ ] **Browser extension** — One-click summarize from YouTube's website
- [ ] **Podcast/audio support** — Summarize audio content via Whisper
- [ ] **Slack/Email integration** — Send summaries directly to team channels
- [ ] **Comparison mode** — Compare summaries from multiple videos

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ by **Hemanth Reddy** &nbsp;|&nbsp; Powered by **Google Gemini 2.0 Flash** & **Streamlit**

⭐ If you find this project useful, please consider giving it a star!

</div>
