# 🔥 Blaze - Your Personal Local Jarvis

**A fully offline, voice-enabled AI companion** inspired by Jarvis from Iron Man. Built by Ayan Abbas.

![Demo](images/demo.gif)

---

## ✨ Key Features

- 100% Offline AI using Ollama
- Natural Voice Conversation with Piper TTS
- Persistent Memory with smart sliding window
- Real-time Streaming Responses
- Hardware Control (RGB Table Light via Arduino + FastAPI)
- Voice Toggle & Command System
- Clean Modular Code Architecture
- Time-aware conversations

---

## 🎥 Demo

[Watch Demo Video](https://youtu.be/YOUR_VIDEO_ID_HERE)  
*(Voice + Light Control + Streaming in action)*

![Blaze in Action](images/demo.gif)

---

## 🛠️ Tech Stack

- **Python 3**
- **LLM**: Ollama (Llama 3.2)
- **Voice**: Piper TTS
- **Backend**: FastAPI + Uvicorn
- **Hardware**: PySerial (Arduino)
- **Architecture**: Modular Python Package

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)
![PySerial](https://img.shields.io/badge/PySerial-000000?style=for-the-badge&logo=python&logoColor=white)
---

## 🚀 Quick Start

### Prerequisites
- Ollama installed and running (`llama3.2` model)
- Arduino + RGB setup (optional)
- **Piper TTS** (for voice output)
- Python 3.10+

### Installation

```bash
git clone https://github.com/Ayanabbas2006/Blaze.git
cd Blaze

pip install -r requirements.txt
```

### Running Blaze
## Terminal 1 — Start Hardware API:
```bash
uvicorn api.main:app --reload --port 8000
```
## Terminal 2 — Start Blaze:
```bash
python main.py
```
### 📁 Project Structure
```bash
Blaze/
├── main.py
├── config.py
├── requirements.txt
├── .gitignore
├── light.ino #Arduino code for Light
├── README.md
│
├── blaze/                  # Core Package
│   ├── __init__.py
│   ├── core.py
│   ├── memory.py
│   ├── voice.py
│   ├── hardware.py
│   ├── commands.py
│   ├── utils.py
│   └── prompts.py
│
├── api/                    # FastAPI Hardware Server
│   ├── __init__.py
│   └── main.py
│
├── data/
│   ├── blaze_memory.json
│   └── colors.txt
├── voice/
└── images/
```

### 🎮 Commands
```bash
--cmd -vc 1 → Voice ON
--cmd -vc 0 → Voice OFF
--cmd -m my-blaze → Switch model #custom model
--cmd -p model → Display Current Model
--cmd -exit → Save & Exit
```

### 📈 Future Enhancements

- Safe File System Access (Coding Assistant)
- Web Interface (Gradio/Streamlit)
- RAG & Tool Calling
- Docker Support

### 👨‍💻 About the Developer
- **Ayan Abbas**
- 3rd Year B.Tech Computer Science & Design
- Ghaziabad, Delhi-NCR, India
- *Passionate about: Building practical AI systems, Human-AI interaction, and local AI agents.*