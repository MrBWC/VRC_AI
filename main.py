import sounddevice as sd
import numpy as np
import whisper
import requests
import asyncio
import soundfile as sf
import edge_tts  # Edge-TTS for Text-to-Speech
import atexit  # To ensure proper cleanup when exiting
import os  # To handle file removal

# Initialize Whisper model
whisper_model = whisper.load_model("small")  # or "tiny" for faster

# Audio recording settings
samplerate = 16000
duration = 5  # Seconds

# System prompt for Mistral model
system_prompt = """
You are an intelligent AI assistant. You are helpful, friendly, and always polite.
Your task is to assist the user in the most helpful and informative way possible.
Be brief and to the point, but also empathetic when necessary.
"""

# Global variable to track the Mistral model connection
mistral_connection = None

# Function to record audio
def record_audio(filename):
    print("🎙️ Listening...")
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    sf.write(filename, recording, samplerate)
    print(f"✅ Audio saved to {filename}")

# Function to transcribe audio to text using Whisper
def transcribe_audio(filename):
    print("🧠 Transcribing...")
    result = whisper_model.transcribe(filename)
    text = result["text"].strip()
    print(f"💬 User said: {text}")
    return text

# Function to ask Mistral model via Ollama
import requests
import json

def ask_mistral(prompt):
    print("🤖 Asking Mistral via Ollama...")

    if mistral_connection is None:
        print("⚠️ Mistral model is not connected.")
        return None

    # Send the request to Ollama (locally running Mistral model)
    response = requests.post(
        "http://localhost:11434/api/generate",  # Ollama endpoint
        json={"model": "mistral", "prompt": prompt},
        stream=True  # Use streaming mode to handle chunked responses
    )

    # Check for a successful response
    if response.status_code == 200:
        full_response = ''
        
        # Iterate over each chunk of the response
        for chunk in response.iter_lines():
            if chunk:
                try:
                    # Parse each JSON chunk
                    chunk_data = json.loads(chunk.decode('utf-8'))
                    
                    # Accumulate the "response" from each chunk
                    full_response += chunk_data.get('response', '')
                    
                    # If the response is complete, stop reading further
                    if chunk_data.get('done', False):
                        print(f"🤖 Final AI response: {full_response}")
                        return full_response
                except json.JSONDecodeError as e:
                    print(f"⚠️ Error decoding JSON chunk: {e}")
                    continue
    else:
        print(f"⚠️ Error: {response.status_code} - {response.text}")
        return None


# Function to speak using Edge-TTS
async def speak(text, voice="en-US-JennyNeural", output_path="response.mp3"):
    print(f"🗣️ Speaking with Edge-TTS ({voice})...")

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

    # Play the audio file
    data, fs = sf.read(output_path, dtype='float32')
    sd.play(data, fs)
    sd.wait()

    print(f"✅ Response spoken and saved to {output_path}")

# Cleanup function to delete files when exiting
def cleanup():
    print("🧹 Deleting files...")
    files_to_delete = ["input.wav", "response.mp3"]
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"🧹 {file} deleted.")

# Main loop
def main_loop():
    while True:
        try:
            input_file = "input.wav"
            output_file = "response.mp3"
            
            # Step 1: Record audio
            record_audio(input_file)
            
            # Step 2: Transcribe the recorded audio
            user_text = transcribe_audio(input_file)
            if user_text:
                # Step 3: Get AI reply from Mistral model
                ai_reply = ask_mistral(user_text)
                if ai_reply:
                    # Step 4: Speak the AI reply
                    asyncio.run(speak(ai_reply, output_path=output_file))

            # Cleanup the files (delete them)
            cleanup()

        except KeyboardInterrupt:
            print("🛑 Exiting loop.")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    # Set up cleanup function to be called on exit
    atexit.register(cleanup)

    # Load the Mistral model (simulate loading a local model)
    print("🔌 Loading Mistral model...")
    mistral_connection = "Mistral Model Loaded"  # Simulating model load, replace with actual loading logic
    print("✅ Mistral model loaded successfully.")

    # Run the main loop
    main_loop()

    # Cleanup will be called automatically when the program exits
