"""
Speech-to-speech (Voice Changer) with ElevenLabs.
Takes your recorded audio and re-speaks it in a stock voice you pick.

Setup:
    pip install requests python-dotenv
    Create a .env file next to this script with:
        ELEVENLABS_API_KEY=your_api_key_here

Usage:
    python sts_voice_changer.py                    # asks for the audio file path
    python sts_voice_changer.py input.wav          # uses the file you pass in
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
BASE_URL = "https://api.elevenlabs.io/v1"
MODEL_ID = "eleven_multilingual_sts_v2"   # speech-to-speech model
OUTPUT_FILE = "output_sts.mp3"


def get_headers():
    if not API_KEY:
        print("Error: ELEVENLABS_API_KEY not found. Check your .env file.")
        sys.exit(1)
    return {"xi-api-key": API_KEY}


def list_voices():
    resp = requests.get(f"{BASE_URL}/voices", headers=get_headers(), timeout=30)
    if resp.status_code != 200:
        print(f"Could not fetch voices ({resp.status_code}): {resp.text}")
        sys.exit(1)
    return resp.json().get("voices", [])


def choose_voice(voices):
    if not voices:
        print("No voices found on your account.")
        sys.exit(1)

    print("\nAvailable voices:")
    for i, v in enumerate(voices, start=1):
        labels = v.get("labels", {}) or {}
        desc = ", ".join(str(x) for x in labels.values())
        print(f"  {i:2d}. {v['name']}  [{v['voice_id']}]  {desc}")

    while True:
        choice = input("\nPick a voice number or name: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(voices):
            return voices[int(choice) - 1]

        for v in voices:
            if v["name"].lower() == choice.lower():
                return v

        print("Invalid choice, try again.")


def speech_to_speech(voice_id, audio_path, out_path=OUTPUT_FILE):
    if not os.path.isfile(audio_path):
        print(f"Audio file not found: {audio_path}")
        sys.exit(1)

    data = {
        "model_id": MODEL_ID,
        "voice_settings": json.dumps({
            "stability": 0.5,
            "similarity_boost": 0.75,
        }),
        "remove_background_noise": "false",   
    }

    print("Converting speech...")
    with open(audio_path, "rb") as f:
        files = {"audio": (os.path.basename(audio_path), f)}
        resp = requests.post(
            f"{BASE_URL}/speech-to-speech/{voice_id}",
            headers=get_headers(),
            data=data,
            files=files,
            timeout=300,
        )

    if resp.status_code != 200:
        print(f"Speech-to-speech failed ({resp.status_code}): {resp.text}")
        sys.exit(1)

    with open(out_path, "wb") as f:
        f.write(resp.content)
    print(f"Saved: {out_path}")


def main():
    if len(sys.argv) > 1:
        audio_path = " ".join(sys.argv[1:]).strip('"')
    else:
        audio_path = input("Path to your input audio file (wav/mp3/m4a): ").strip().strip('"')

    voices = list_voices()
    voice = choose_voice(voices)
    speech_to_speech(voice["voice_id"], audio_path)


if __name__ == "__main__":
    main()
