import os
from cartesia import Cartesia
from pydub import AudioSegment
from dotenv import find_dotenv, load_dotenv
import subprocess

load_dotenv()
api_key = os.getenv("TTS_KEY")
client = Cartesia(api_key=api_key)

# speaker either 0 or 1 to denote which voice to use
# language either 0, 1 or 2 to denote which language
# 0 = English, 1 = Hindi, 2 = Japanese
def tts(text, language, empty_time=0, real_time=False):
    speech_model = [["34d923aa-c3b5-4f21-aac7-2c1f12730d4b", "4629672e-661d-4f59-93fc-8db4476b585f"],
                    ["7f423809-0011-4658-ba48-a411f5e516ba", "c1abd502-9231-4558-a054-10ac950c356d"],
                    ["9e7ef2cf-b69c-46ac-9e35-bbfd73ba82af", "06950fa3-534d-46b3-93bb-f852770ea0b5"]]
    for i in range(2):
        data = client.tts.bytes(
            model_id="sonic-2",
            transcript=text[i],
            voice_id=speech_model[language][i],  # Barbershop Man
            output_format={
                "container": "wav",
                "encoding": "pcm_s16le",
                "sample_rate": 44100,
            },
        )

        with open(f"temp{i}.wav", "wb") as f:
            f.write(data)

    # Load the existing audio file if it exists
    try:
        existing_audio = AudioSegment.from_wav("sonic-7.wav")
    except FileNotFoundError:
        existing_audio = AudioSegment.silent(duration=0)  # Create an empty audio segment

    # Create empty audio segment for specified duration (in milliseconds)
    if empty_time > 0:
        # silent_audio = AudioSegment.silent(duration=empty_time * 1000)
        audio0 = AudioSegment.from_wav("temp0.wav")
        gap_audio = AudioSegment.silent(duration= 500)
        audio1 = AudioSegment.from_wav("temp1.wav")
        audio0 = audio0 + gap_audio + audio1
    else:
        audio0 = AudioSegment.from_wav("temp0.wav")
        gap_audio = AudioSegment.silent(duration= 500)
        audio1 = AudioSegment.from_wav("temp1.wav")
        audio0 = audio0 + gap_audio + audio1
    # Concatenate the existing audio with the new audio
    combined_audio = existing_audio + audio0

    # Export the combined audio to the same file
    combined_audio.export("sonic-7.wav", format="wav")
    os.remove("temp0.wav")
    os.remove("temp1.wav")
    # Play the file
    
    subprocess.run(["ffplay", "-autoexit", "-nodisp", "sonic-5.wav"]) if real_time else None