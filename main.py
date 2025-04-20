import sounddevice as sd
import numpy as np
import whisper
import requests
import edge_tts
import asyncio
import soundfile as sf

# Initialize Whisper model
whisper_model = whisper.load_model("base")  # or "tiny" for faster

# Audio recording settings
samplerate = 16000
duration = 5  # Seconds

def record_audio(filename):
    print("🎙️ Listening...")
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    sf.write(filename, recording, samplerate)
    print(f"✅ Audio saved to {filename}")

def transcribe_audio(filename):
    print("🧠 Transcribing...")
    result = whisper_model.transcribe(filename)
    text = result["text"].strip()
    print(f"💬 User said: {text}")
    return text

def ask_mistral(prompt):
    print("🤖 Asking Mistral via Ollama...")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt}
    )
    output = ""
    for line in response.iter_lines():
        if line:
            data = line.decode('utf-8')
            output += data
    print(f"🤖 AI response: {output.strip()}")
    return output.strip()

async def speak(text, voice="en-US-JennyNeural"):
    print(f"🗣️ Speaking with edge-tts ({voice})...")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("response.mp3")
    data, fs = sf.read("response.mp3", dtype='float32')
    sd.play(data, fs)
    sd.wait()

def main_loop():
    while True:
        try:
            record_audio("input.wav")
            user_text = transcribe_audio("input.wav")
            if user_text:
                ai_reply = ask_mistral(user_text)
                asyncio.run(speak(ai_reply))
        except KeyboardInterrupt:
            print("🛑 Exiting loop.")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main_loop()
