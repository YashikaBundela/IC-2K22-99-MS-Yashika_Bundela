
import requests
import getpass

def main():
    print("=" * 45)
    print("ELEVENLABS AI VOICE GENERATOR")
    print("=" * 45)

    api_key = getpass.getpass("Enter your ElevenLabs API key: ").strip()

    if not api_key:
        print("API key is required.")
        return

    headers = {"xi-api-key": api_key}

    # Get the voices available in your account
    response = requests.get(
        "https://api.elevenlabs.io/v1/voices",
        headers=headers
    )

    if response.status_code != 200:
        print("Could not retrieve voices.")
        print(response.text)
        return

    voices = response.json().get("voices", [])

    if not voices:
        print("No available voices were found.")
        return

    print("\nAvailable voices:")

    for i, voice in enumerate(voices, start=1):
        print(f"{i}. {voice['name']}")

    try:
        choice = int(input("\nChoose a voice number: "))

        if choice < 1 or choice > len(voices):
            print("Invalid voice number.")
            return

        selected_voice = voices[choice - 1]
        voice_id = selected_voice["voice_id"]

    except ValueError:
        print("Please enter a valid number.")
        return

    text = input("\nEnter the text to speak: ").strip()

    if not text:
        print("Text cannot be empty.")
        return

    print("\nGenerating audio...")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    headers["Content-Type"] = "application/json"

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        print("Audio generation failed.")
        print(response.text)
        return

    with open("generated_audio.mp3", "wb") as audio_file:
        audio_file.write(response.content)

    print("\nAudio generated successfully!")
    print("Saved as generated_audio.mp3")


if __name__ == "__main__":
    main()
