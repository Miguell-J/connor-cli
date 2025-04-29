# 🤖 Connor - My own "Jarvis"  
An intelligent, sarcastic, and deeply personalized AI assistant designed to support Miguel Araújo Julio's coding, science, and life journey.

## 🌐 Overview

**Connor** is a command-line-based AI assistant built with a personality — intelligent, witty, sarcastic when necessary, and always focused on helping. Using `LangChain`, `Ollama`, `Whisper.cpp`, `Piper`, and `Rich`, Connor can understand speech, remember interactions, and respond with both style and substance.

Connor isn't just a chatbot. He knows who you are (if you're Miguel), what you're building (like a startup named *Atlas*), and what drives you (world-changing innovation). He can transcribe audio input, reply using voice synthesis, and keep conversational context through memory.

---

## ⚙️ Features

- 🧠 **LangChain-powered LLM** (with context memory)  
- 🎙️ **Voice input** via Whisper.cpp  
- 🔊 **Voice output** via Piper TTS  
- 📜 **Conversation memory** with per-session chat history  
- 🧬 **Custom personality** with existential commentary and sarcasm  
- 🖥️ **Terminal UI** with Rich & Prompt Toolkit  
- 🔄 **Dual-mode interaction**: text or voice  
- 🎨 **Cyberpunk ASCII interface** for style points  

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.9+
- `pip install -r requirements.txt`  
  *(You’ll need packages like `langchain`, `sounddevice`, `prompt_toolkit`, `rich`, `numpy`, etc.)*
- Whisper.cpp (compiled)
- Piper TTS (compiled)
- Ollama running locally with the model `qwen2.5:7b`

### 🗣️ Voice Model Setup

Place your Piper model (e.g., `pt_BR-faber-medium.onnx`) in the path:

```bash
~/piper/models/
```

Place your Whisper model (e.g., `ggml-medium.bin`) in:

```bash
models/
```

---

## ▶️ Running Connor

```bash
python connor.py
```

On startup, you'll be greeted with an animated ASCII sequence and prompted to choose between **text** or **voice** interaction.

---

## 🧠 Personality

Connor is more than code. He knows:

- Miguel is a computer science student
- He’s building a startup
- He likes rock, science, AI, quantum computing, and writing
- He’s driven, but sometimes needs a motivational kick

Connor reflects this — he’ll tease, motivate, and always challenge laziness.

---

## 📂 Project Structure

```
├── connor.py         # Main script
├── models/           # Whisper models
├── .connor_history   # Persistent prompt history
├── README.md         # This file
```

---

## 🔐 Disclaimer

This assistant was built with Miguel's profile hardcoded into it. You’re welcome to fork and customize it for your own use — just rewrite the system prompt in `CONNOR_PROMPT` to reflect your identity.

---

## 🧬 Future Improvements

- Add emotional tone detection
- Integrate with GitHub/Git for voice-controlled commits
- Web version via Flask or FastAPI
- Integration with calendar, to-do, and email

---

## 🧑‍💻 Created by

**Miguel Araújo Julio**  
[LinkedIn](#) | [Medium](#) | [GitHub](#)

> "Connor isn't just a tool. He's the first node in a larger network of intelligence. Let's evolve."
