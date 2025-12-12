from gtts import gTTS
import os
import ffmpeg
import time
import re
from config import OUTPUT_WAV_FILE, DURATION_FILE

def get_audio_duration(audio_file):
    try:
        probe = ffmpeg.probe(audio_file)
        duration = float(probe['streams'][0]['duration'])
        return duration
    except Exception:
        return 0.0

def clean_text_for_audio(text):
    
    if "***" in text:
        text = text.split("***")[0]
    
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    
   
    text = text.replace('*', '')
    
    return text.strip()

def generate_audio(text_prompt, output_wav, lang_code):
    """
    Main audio generation function.
    Uses gTTS for supported languages, falls back to English for unsupported ones.
    """
    GTTS_SUPPORTED = ['en', 'hi', 'ur', 'pa', 'gu', 'mr', 'te', 'kn', 'ml', 'ta', 'bn']
    
    if lang_code in GTTS_SUPPORTED:
        return generate_gtts_audio(text_prompt, output_wav, lang_code)
    else:
        print(f"INFO: Using English audio for {lang_code} (gTTS doesn't support this language)")
        return generate_gtts_audio(text_prompt, output_wav, "en")

def generate_gtts_audio(text_prompt, output_wav, lang_code):
    """Generate audio using gTTS (free but limited language support)."""
    temp_mp3 = "temp_gtts_audio.mp3"

  
    cleaned_text = clean_text_for_audio(text_prompt)
    
    if not cleaned_text:
        print("Error: Text empty after cleaning.")
        return False, 0.0

    print(f"Generating audio ({lang_code})...")


    try:
        tts = gTTS(text=cleaned_text, lang=lang_code, slow=False)
        tts.save(temp_mp3)

        if not os.path.exists(temp_mp3) or os.path.getsize(temp_mp3) == 0:
            return False, 0.0

    except Exception as e:
        print(f"GTTS Error: {e}")
        return False, 0.0

    try:
        (
            ffmpeg
            .input(temp_mp3)
            .output(output_wav,
                    acodec='pcm_s16le',
                    ar=24000,
                    af='adelay=500|500')
            .run(overwrite_output=True, quiet=True)
        )
        os.remove(temp_mp3)

        if not os.path.exists(output_wav):
            return False, 0.0

    except Exception as e:
        print(f"FFmpeg Error: {e}")
        return False, 0.0

    duration = get_audio_duration(output_wav)
    if duration > 0:
        with open(DURATION_FILE, 'w') as f:
            f.write(str(duration))

    return True, duration