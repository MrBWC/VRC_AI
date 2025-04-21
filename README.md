🎮 VRChat AI Agent
This project creates an AI-powered virtual character for VRChat — capable of listening, thinking, speaking, and even moving — using a combination of modern AI tools.

🧠 Tech Overview
🎙️ Speech-to-Text (STT) — OpenAI Whisper or Faster-Whisper

🧠 AI Brain — Mistral (via Ollama) for generating context-aware responses

🗣️ Text-to-Speech (TTS) — Microsoft Edge-TTS Neural Voices

🔊 Virtual Audio Cable — Streams AI voice directly into VRChat's microphone input

🕺 VR Movement Control — Uses OpenVR & OSC for avatar animations and behaviors

⚙️ Features
✅ Real-time speech-to-text conversion
✅ AI-generated replies using the locally hosted Mistral model (Ollama)
✅ Natural-sounding voice replies via Edge-TTS Neural voices
✅ AI voice routed directly to VRChat using Virtual Audio Cable
✅ Supports movement & gestures through VR-ready motion control (OpenVR & OSC)
✅ Includes idle "behavior tree" for autonomous patrolling when idle
✅ Logs user input, AI responses, and reactions for future behavior training

🔧 Requirements
💡 Ollama + Mistral — for AI responses.
Make sure the Mistral model is installed locally in Ollama.
👉 Get Ollama I https://ollama.com/

💡 Whisper (or Faster-Whisper) — for speech-to-text.
Installed automatically when running the setup script.

💡 Microsoft Edge-TTS — for high-quality TTS with neural voices.

💡 Virtual Audio Cable and Mixer — required to route AI-generated voice into VRChat.
👉 Download Virtual Audio Mixer Banana
👉 Download Virtual Audio Cable 
https://vb-audio.com/

📋 Setup Scripts
setup.bat
Installs all dependencies (Whisper, Edge-TTS, Ollama client libraries, etc.) and prepares your virtual environment.

run.bat
Launches the full AI assistant:

Listens to your voice

Generates a response

Sends voice output to VRChat

Controls avatar movement (if applicable)

💾 Installation Guide
1️⃣ Clone the repository:
git clone https://github.com/MrBWC/VRC_AI.git
cd VRC_AI

2️⃣ Run the setup:
setup.bat

3️⃣ Start the AI agent:
run.bat

⚠️ Notes
Make sure Ollama is installed and the Mistral model is downloaded.
You can download models directly through the Ollama terminal interface.

Configure Virtual Audio Cable so that your AI voice gets routed to VRChat's microphone input. Test it by playing back a .wav file before launching the project.