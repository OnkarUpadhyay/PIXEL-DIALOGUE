<!-- Banner -->
<p align="center">
  <img src="assets/pixel-dialogue-banner.png" alt="Pixel Dialogue Banner" width="100%" />
</p>

<h1 align="center">
  <img
    src="https://readme-typing-svg.herokuapp.com?size=26&duration=2500&pause=700&color=FF3AA3&center=true&vCenter=true&width=600&lines=🌟+Pixel+Dialogur;Hello+traveler!;You’ve+entered+the+world+of+Pixel+Dialogur;A+chatbot+that+blends+agentic+intelligence;With+pixel‑perfect+charm;✨+Explore+the+code;✨+Share+your+thoughts;✨+Help+shape+the+dialogue"
    alt="Animated Pixel Dialogur welcome"
  />
</h1>


<h1 align="center">✨ Pixel Dialogue</h1>
<p align="center"><em>Chat with your images — Caption • Detect • OCR • Generate</em></p>

<p align="center">
  <!-- Badges -->
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="https://streamlit.io/"><img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?logo=streamlit&logoColor=white"></a>
  <a href="https://python.langchain.com/"><img alt="LangChain" src="https://img.shields.io/badge/LangChain-Tools-blueviolet"></a>
  <img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg">
  <img alt="Built with Love" src="https://img.shields.io/badge/Built%20with-%F0%9F%92%9C-purple">
</p>

---

<p align="center">
  <img src="assets/demo.gif" alt="Pixel Dialogue demo" width="80%">
</p>

## 🧠 What is Pixel Dialogue?
**Pixel Dialogue** is your images' conversational companion. Upload a picture and ask anything:
- “What’s in this image?”
- “List objects with bounding boxes and confidence.”
- “Extract the text in this poster.”
- “Generate a futuristic version of this scene.”

Under the hood, a LangChain agent chooses the right tool (BLIP, YOLO, EasyOCR, Stable Diffusion) and an LLM to deliver fast, grounded answers.

---


## 🚀 Features
- 🖼️ **Image Captioning** — BLIP generates rich descriptions.
- 🔍 **Object Detection** — YOLO finds objects + bounding boxes + confidence.
- 🧾 **Text Extraction (OCR)** — EasyOCR pulls text from images.
- 🎨 **AI Image Generation** — Stable Diffusion v1.5 renders from prompts.
- 🧠 **Conversational Agent** — LangChain + LLMs (Llama/Gemini) route tasks to the right tool.
- ♻️ **One‑click Reset** — Clears `.tmp/.gen` and **rebuilds file uploader** via dynamic keys for a fresh UI.

## 🛠️ Tech Stack
**Streamlit** · **LangChain** · **Groq/Google LLMs** · **YOLO** · **BLIP** · **EasyOCR** · **Stable Diffusion** · **Python 3.10+**

---

## 📥 Installation
```bash
# 1) Clone
git clone https://github.com/OnkarUpadhyay/PIXEL-DIALOGUE.git
cd Pixel_Dialogue

# 2) Virtual environment
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

# 3) Install
pip install -r requirements.txt

# 4) Environment (create .env)
# GROQ_API_KEY=...
# GOOGLE_API_KEY=...
# TAVILY_API_KEY=...

# 5) Run
streamlit run main.py
```

> **Note:** The app uses ephemeral workspaces: `.tmp/` for uploaded files and `.gen/` for generated images. The **Reset** button clears them and uses a **dynamic uploader key** to fully reset the UI.

---


## 🧭 Architecture
<p align="center">
  <img src="assets/architecture.png" alt="Pixel Dialogue architecture diagram" width="100%">
</p>

**Flow:** Browser → Streamlit (UI + Agent) → LangChain (Groq/Gemini) → Tools (BLIP/YOLO/EasyOCR/SD) → Workspaces (`.tmp`, `.gen`) → Answer.

---

## 📁 Project Structure
```
Pixel_Dialogue/
├─ main.py               # Streamlit UI + agent orchestration
├─ tools.py              # Tools: caption, detect, OCR, generate, search
├─ assets                # UI images (logo, banner, icons)
├─ .tmp/                 # ephemeral uploads (gitignored)
├─ .gen/                 # generated images (gitignored)
├─ requirements.txt
├─ .gitignore
└─ README.md
```

---

## 🙌 Contributing
PRs are welcome: new tools, UI polish, GPU tips, or CI workflows.

<p align="center">
  <img src="assets/pixel-dialogue-logo.png" alt="Pixel Dialogue logo" width="52%" />
</p>

