
<!-- Banner -->
<p align="center">
  <img src="assets/pixel-dialogue-banner.svg" alt="Pixel Dialogue Banner" width="100%" />
</p>

<h1 align="center">✨ Pixel Dialogue</h1>
<p align="center"><em>Chat with your images — Caption • Detect • OCR • Generate</em></p>

<p align="center">
  <!-- Badges -->
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="https://streamlit.io/"><img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?logo=streamlit&logoColor=white"></a>
  <a href="https://github.com/Onkar-Upadhyay/Pixel_Dialogue/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/License-MIT-2ea44f.svg"></a>
  <img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg">
  <img alt="Made with Love" src="https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-purple">
</p>

---

<p align="center">
  <img src="assets/demo.gif" alt="Pixel Dialogue demo (placeholder)" width="90%">
</p>

## 🚀 Features
- 🖼️ **Image Captioning** — BLIP generates rich descriptions.
- 🔍 **Object Detection** — YOLO finds objects + bounding boxes + confidence.
- 🧾 **Text Extraction (OCR)** — EasyOCR pulls text from images.
- 🎨 **AI Image Generation** — Stable Diffusion v1.5 renders from prompts.
- 🧠 **Conversational Agent** — LangChain + LLMs (Groq/Google) route tasks to the right tool.

## 🛠️ Tech Stack
**Streamlit** · **LangChain** · **Groq/Google LLMs** · **YOLO** · **BLIP** · **EasyOCR** · **Stable Diffusion** · **Python 3.10+**

---

## 📥 Installation
```bash
# Clone
git clone https://github.com/YOUR_USERNAME/Pixel_Dialogue.git
cd Pixel_Dialogue

# (Recommended) Virtual env
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

# Install deps
pip install -r requirements.txt

# Environment
copy .env.example .env  # create and fill with your keys
# Or create .env manually:
# GROQ_API_KEY=...
# GOOGLE_API_KEY=...
# TAVILY_API_KEY=...

# Run
streamlit run main.py
```

> **Note:** The app uses ephemeral workspaces: `.tmp/` for uploaded files and `.gen/` for generated images. The **Reset** button clears them and uses a **dynamic uploader key** to fully reset the UI.

---

## 🎬 Create a real demo GIF (replace the placeholder)

You have two easy options. After recording, **save the final GIF as** `assets/demo.gif`.

### Option A — OBS Studio (recommended)
1. Install [OBS Studio](https://obsproject.com/)
2. Record a short 10–20s clip interacting with the app
3. Export to MP4/WebM
4. Convert to GIF with **ffmpeg**:
   ```bash
   ffmpeg -i input.mp4 -vf "fps=10,scale=900:-1:flags=lanczos" -loop 0 assets/demo.gif
   ```

### Option B — Direct ffmpeg screen capture (Windows PowerShell)
```powershell
# Record a region (adjust size/offset) to output.mp4
ffmpeg -f gdigrab -framerate 30 -offset_x 100 -offset_y 100 -video_size 1280x720 -i desktop output.mp4

# Convert to GIF
ffmpeg -i output.mp4 -vf "fps=10,scale=900:-1:flags=lanczos" -loop 0 assets/demo.gif
```

---

## 🧭 Architecture
<p align="center">
  <img src="assets/architecture.svg" alt="Pixel Dialogue architecture diagram" width="100%">
</p>

**Flow:** Browser → Streamlit (UI + Agent) → LangChain → Tools (BLIP / YOLO / EasyOCR / SD) → Workspaces (`.tmp`, `.gen`) → Response.

---

## 📁 Project Structure
```
Pixel_Dialogue/
├─ main.py               # Streamlit UI + Agent orchestration
├─ tools.py              # Tools: caption, detect, OCR, generate, search
├─ assets/
│  ├─ pixel-dialogue-logo.svg
│  ├─ pixel-dialogue-banner.svg
│  ├─ architecture.svg
│  └─ demo.gif           # placeholder – replace with your real capture
├─ .tmp/                 # ephemeral uploads (gitignored)
├─ .gen/                 # generated images (gitignored)
├─ requirements.txt
├─ .gitignore
├─ .env.example          # template with keys
└─ README.md
```

---

## 🙌 Contributing
PRs are welcome! Ideas: improve UI, add new tools/models, add GPU tips, optimize SD pipeline, or write tests.

## 📜 License
MIT — see [LICENSE](LICENSE).

---

<p align="center">
  <img src="assets/pixel-dialogue-logo.svg" alt="Pixel Dialogue logo" width="56%" />
</p>
