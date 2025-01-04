import os
from _4_audio_anonymization import anonymize_voice
from _3_audio_conversion import AudioConverter, convert_wav_to_mp3


def process_audio(mp3_file, anonymized_mp3_file):
    """Performs full process of converting, anonymizing, and converting back to MP3."""
    # Define file paths with os.path.join for cross-platform compatibility
    wav_file = os.path.join(os.getcwd(), "temp_audio.wav")  # Temporary WAV file
    anonymized_wav_file = os.path.join(os.getcwd(), "anonymized_audio.wav")  # Anonymized WAV file

    # Convert MP3 to WAV
    converter = AudioConverter()
    converter.load_audio_from_mp3(mp3_file)
    converter.convert_to_wav(wav_file)

    # Anonymize the WAV file
    anonymize_voice(wav_file, anonymized_wav_file)

    # Convert the anonymized WAV file back to MP3
    convert_wav_to_mp3(anonymized_wav_file, anonymized_mp3_file)
    print("Anonymization and conversion to MP3 successful.")


# Example Usage
if __name__ == "__main__":
    # Define input and output paths for MP3 files
    input_mp3_file = os.path.join(os.getcwd(), "output_audio.mp3")  # Input MP3 file
    output_mp3_file = os.path.join(os.getcwd(), "output_anonymized.mp3")  # Output MP3 file

    # Process audio
    process_audio(input_mp3_file, output_mp3_file)
