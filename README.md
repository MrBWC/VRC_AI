# 🎮 VRChat AI Agent

This project creates an AI-powered virtual character for VRChat using:

- 🎙️ **Speech-to-Text (STT)** — OpenAI Whisper or Faster-Whisper  
- 🧠 **AI Model** — Mistral running locally via Ollama  
- 🗣️ **Text-to-Speech (TTS)** — Microsoft Edge-TTS (neural voices)  
- 🔊 **Virtual Audio Cable** — Sends AI voice to VRChat for in-game speaking  

---

## ⚙️ Features

✅ Converts real-time speech to text  
✅ Generates AI replies using Ollama's Mistral model  
✅ Speaks responses using Microsoft Edge-TTS neural voices  
✅ Sends the AI voice output directly to VRChat via Virtual Audio Cable  

---

## 🔧 Requirements
Ollama with Mistral: You need to have Ollama installed and the Mistral model running locally. You can find more details on setting up Ollama here.

Whisper: For real-time speech-to-text, we use Whisper, which will be automatically installed as part of the dependencies.

Microsoft Edge-TTS: Used for high-quality text-to-speech with neural voices.

Virtual Audio Cable: To route the AI's speech output into VRChat for in-game interaction.

---

## 📋 Setup Scripts
setup.bat: This batch script will set up the environment and install all the dependencies needed for the project.

run.bat: After the setup, run this batch script to start the project. It will activate the environment and run the Python script.

Additional Notes:
Ollama with Mistral: Make sure you have Ollama installed and the Mistral model set up. If you haven't installed Ollama yet, you can visit the official Ollama website for installation instructions.

Virtual Audio Cable Setup: Ensure that Virtual Audio Cable is installed and properly configured to send audio output into VRChat. You can download it from here.

---

## 💾 Installation

1. Clone the project:

```bash
git clone https://github.com/MrBWC/VRC_AI.git
cd vrc_ai
```

2. Run the bat files:
Run the setup.bat script to install dependencies and set up the environment:
```bash
setup.bat
```
After installation, you can run the project with the run.bat script:
```bash
run.bat
```