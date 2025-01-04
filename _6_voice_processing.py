import requests
import json
import wave
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import logging
import google.generativeai as genai
import asyncio
import pygame
import nest_asyncio
import edge_tts
import os
import _5_anonymize_voice_Main

# Configuration
LLM_API_KEY = 'AIzaSyBfF0aEh8ygArvvRy5v2l1G_xoMSHwyCJk'  # Your Google Gemini API key
TTS_API_KEY = 'AIzaSyDJv0ZQNvFqjirNh2PYPp5QV_FHHX5zOq8'  # Your Google Text-to-Speech API key
LLM_ENDPOINT = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={LLM_API_KEY}'
TTS_ENDPOINT = f'https://texttospeech.googleapis.com/v1/text:synthesize?key={TTS_API_KEY}'  # Google Text-to-Speech API endpoint

# Configure Google Generative AI
genai.configure(api_key=LLM_API_KEY)
nest_asyncio.apply()  # For async compatibility in PyCharm

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Voice Input
def record_audio(filename):
    """Records audio from the microphone and saves it as a WAV file."""
    duration = 5  # Duration in seconds
    fs = 44100  # Sample rate
    logging.info("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    logging.info("Finished recording.")

    # Save the recorded data as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 2 bytes for int16 format
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())

    logging.info(f"Audio saved as: {filename}")

# 2. Language Detection and Recognition
def recognize_speech(filename):
    """Attempts to recognize speech from an audio file in either Persian or English."""
    recognizer = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)

    # Try recognizing Persian first
    try:
        text_fa = recognizer.recognize_google(audio_data, language='fa-IR', show_all=True)
        if text_fa:
            best_fa = max(text_fa['alternative'], key=lambda x: x.get('confidence', 0))
            confidence = best_fa.get('confidence', None)
            if confidence is not None and confidence > 0.6:  # Confidence threshold for Persian
                logging.info(f"Recognized Persian Text: {best_fa['transcript']} with confidence: {confidence}")
                return best_fa['transcript'], 'fa'
    except sr.UnknownValueError:
        logging.warning("Could not understand Persian audio.")
    except sr.RequestError as e:
        logging.error(f"Request failed for Persian recognition: {e}")

    # Try recognizing English if Persian recognition fails
    try:
        text_en = recognizer.recognize_google(audio_data, language='en-US', show_all=True)
        if text_en:
            best_en = max(text_en['alternative'], key=lambda x: x.get('confidence', 0))
            confidence = best_en.get('confidence', None)
            if confidence is not None and confidence > 0.6:  # Confidence threshold for English
                logging.info(f"Recognized English Text: {best_en['transcript']} with confidence: {confidence}")
                return best_en['transcript'], 'en'
    except sr.UnknownValueError:
        logging.warning("Could not understand English audio.")
    except sr.RequestError as e:
        logging.error(f"Request failed for English recognition: {e}")

    logging.error("Speech recognition failed for both languages.")
    return None, None  # Return None if both attempts fail

# 3. LLM Integration using Google Generative AI
def process_text(question_text):
    """Uses Google Generative AI to process the input text and returns the response."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(question_text)
    if response:
        return response
    else:
        logging.error("No response received from the LLM.")
        return None

# 4. Text to Speech
async def generate_persian_audio(text, filename="output_persian.mp3"):
    """Generates Persian TTS audio from text using edge_tts and saves it to a file."""
    tts = edge_tts.Communicate(text, voice="fa-IR-FaridNeural")  # Set appropriate Persian voice
    await tts.save(filename)
    logging.info(f"Generated Persian audio saved as: {filename}")

def text_to_speech(text, language):
    """Converts text to speech using the appropriate TTS API based on language."""
    output_filename = "output_audio.mp3"

    if language == 'fa':  # Use Persian TTS if language is Persian
        asyncio.run(generate_persian_audio(text, output_filename))
    else:  # Use Google TTS for English
        data = {
            "input": {"text": text},
            "voice": {"languageCode": "en-US", "name": "en-US-Wavenet-D"},
            "audioConfig": {"audioEncoding": "LINEAR16"}
        }
        response = requests.post(TTS_ENDPOINT, json=data)
        response.raise_for_status()
        audio_content = response.json().get("audioContent")

        if audio_content:
            with open(output_filename, 'wb') as f:
                f.write(audio_content.encode('utf-8'))
            logging.info(f"Audio file saved as: {output_filename}")
        else:
            logging.error("No audio content received from Text-to-Speech API.")

    play_audio(output_filename)  # Automatically play the audio file

# 5. Audio Playback
def play_audio(filename):
    """Plays an audio file using pygame."""
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

# 6. Anonymize Audio
def anonymous(input_user):
    if input_user == 'Y':
        input_mp3_file = "output_audio.mp3"
        output_mp3_file = "output_anonymized.mp3"
        _5_anonymize_voice_Main.process_audio(input_mp3_file, output_mp3_file)
        play_audio(output_mp3_file)
    else:
        print("End.")

# 7. Main Function
def main():
    input_filename = 'input.wav'

    # Step 1: Record audio input
    record_audio(input_filename)

    # Step 2: Recognize speech from the recorded audio
    recognized_text, language = recognize_speech(input_filename)
    if recognized_text:
        logging.info(f"Detected Language: {language}")

        # Step 3: Process the recognized text with the LLM
        processed_text = process_text(recognized_text)

        if processed_text:
            # Step 4: Convert processed text to speech
            text_to_speech(processed_text.text, language)

            # Step 5: Option to anonymize the output audio
            input_user = input("Do you want the voice to be anonymized? Y/N: ")
            anonymous(input_user)

if __name__ == "__main__":
    main()