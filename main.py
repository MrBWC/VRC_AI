import sounddevice as sd
import numpy as np
import whisper
import requests
import asyncio
import soundfile as sf
import edge_tts  # Text-to-Speech
import atexit
import os
import testopenvr
import time
import json
from datetime import datetime
from movement_controller import (
    trigger_osc_animation, 
    simulate_head_movement, 
    simulate_full_body_tracking, 
    init_openvr, 
    shutdown_openvr
)

# Initialize Whisper model
whisper_model = whisper.load_model("small")

# Audio recording settings
samplerate = 16000
duration = 5  # Seconds

# Initialize OpenVR
init_openvr()

# Improved System Prompt
system_prompt = """
You are an intelligent AI assistant acting as a VRChat user.
You control body, hand, head, and movement through OSC.
When users mention physical actions (move, wave, dance, nod, walk, sit, idle, patrol):
- Execute via OSC and avoid speaking the action.
- Log user requests, AI actions, and user reactions for future learning.
- If idle, start behavior tree (wander or random patrol) to look social.
Always aim to behave like a friendly, natural VRChat user.
"""

# Global variable for AI model connection
mistral_connection = None

# Movement command config
movement_command_file = "movement_commands.json"
movement_commands = {
    "move": "Move",
    "dance": "Dance",
    "jump": "Jump",
    "walk": "Walk",
    "run": "Run",
    "wave": "Wave",
    "sit": "Sit",
    "patrol": "Patrol"
}

# Save this config to JSON
with open(movement_command_file, "w") as f:
    json.dump(movement_commands, f, indent=4)

# Simple memory log
def log_memory(user_input, ai_output, reaction=None):
    log = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "ai_output": ai_output,
        "user_reaction": reaction
    }
    with open("ai_memory_log.jsonl", "a") as f:
        f.write(json.dumps(log) + "\n")

# Record audio function
def record_audio(filename):
    print("🎙️ Listening...")
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    sf.write(filename, recording, samplerate)
    print(f"✅ Audio saved to {filename}")

# Whisper transcriber
def transcribe_audio(filename):
    print("🧠 Transcribing...")
    result = whisper_model.transcribe(filename)
    text = result["text"].strip()
    print(f"💬 User said: {text}")
    return text

# Mistral / Ollama Query
def ask_mistral(prompt):
    print("🤖 Asking Mistral via Ollama...")
    if mistral_connection is None:
        print("⚠️ Mistral model is not connected.")
        return None

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt},
        stream=True
    )

    if response.status_code == 200:
        full_response = ''
        for chunk in response.iter_lines():
            if chunk:
                try:
                    chunk_data = json.loads(chunk.decode('utf-8'))
                    full_response += chunk_data.get('response', '')
                    if chunk_data.get('done', False):
                        print(f"🤖 Final AI response: {full_response}")
                        return full_response
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON error: {e}")
    else:
        print(f"⚠️ HTTP error: {response.status_code} - {response.text}")
    return None

# Edge TTS speaker
async def speak(text, voice="en-US-JennyNeural", output_path="response.mp3"):
    print(f"🗣️ Speaking with Edge-TTS ({voice})...")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    data, fs = sf.read(output_path, dtype='float32')
    sd.play(data, fs)
    sd.wait()
    print(f"✅ Finished speaking.")

# Cleanup audio files
def cleanup():
    for file in ["input.wav", "response.mp3"]:
        if os.path.exists(file):
            os.remove(file)
            print(f"🧹 {file} deleted.")

# Movement filtering & execution
def handle_movement(text):
    for keyword, osc_trigger in movement_commands.items():
        if keyword in text.lower():
            print(f"🦾 Detected movement: {keyword} → {osc_trigger}")
            trigger_osc_animation(osc_trigger, 1)
            return True
    return False

# Idle Behavior Tree
def behavior_tree_idle():
    print("🤖 Idle: Patrolling...")
    while True:
        trigger_osc_animation("Patrol", 1)  # Looping patrol
        time.sleep(5)  # Simulate walking for 5 sec
        simulate_head_movement(np.random.uniform(-30, 30), np.random.uniform(-30, 30))
        if os.path.exists("input.wav"):
            break  # Stop patrol if new voice command was recorded

# Main Loop
def main_loop():
    idle_timer = 0
    last_interaction = time.time()

    while True:
        try:
            input_file = "input.wav"
            output_file = "response.mp3"
            record_audio(input_file)
            user_text = transcribe_audio(input_file)

            if user_text:
                last_interaction = time.time()
                ai_reply = ask_mistral(f"{system_prompt}\nUser: {user_text}")
                moved = handle_movement(user_text)

                if not moved:
                    if ai_reply:
                        asyncio.run(speak(ai_reply, output_path=output_file))
                        log_memory(user_text, ai_reply)
                else:
                    log_memory(user_text, f"Executed movement: {user_text}")

            else:
                log_memory("Silence", "No response")

            cleanup()

            if time.time() - last_interaction > 20:
                behavior_tree_idle()  # Start idle behaviors after 20 sec

        except KeyboardInterrupt:
            print("🛑 Exiting loop.")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")

# Main Entry
if __name__ == "__main__":
    atexit.register(cleanup)
    print("🔌 Loading Mistral model...")
    mistral_connection = "Mistral Model Loaded"  # Simulate model
    print("✅ Mistral model loaded.")
    main_loop()
    shutdown_openvr()
