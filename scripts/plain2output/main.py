import os
import sys
import time
import json
import ffmpeg
import whisper
import re 
import langdetect

from generate_audio import generate_audio
from subtitles import handle_subtitles_and_merge
from config import SCRIPT_FILE, INPUT_VIDEO_FILE, OUTPUT_WAV_FILE, OUTPUT_TIMESTAMPS_FILE, DURATION_FILE, OUTPUT_VIDEO_FINAL, OUTPUT_VIDEO_NO_AUDIO



def load_text_and_detect_lang():
    """Reads script and language info from files."""
    try:
        with open(SCRIPT_FILE, 'r', encoding='utf-8') as f:
            script_text = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Script file not found at {SCRIPT_FILE}")
        sys.exit(1)

    if not script_text:
        print("Error: Script file is empty. Cannot detect language.")
        sys.exit(1)

   
    lang_info_file = "language_info.txt"
    detected_lang = None
    
    if os.path.exists(lang_info_file):
        try:
            with open(lang_info_file, 'r', encoding='utf-8') as f:
                detected_lang = f.read().strip()
            print(f"INFO: Language read from file: '{detected_lang}'")
        except:
            pass
    
    
    if not detected_lang:
        try:
            detected_lang = langdetect.detect(script_text)
            print(f"INFO: Language detected using langdetect: '{detected_lang}'")
        except Exception as e:
            print(f"WARNING: Language detection failed ({e}). Falling back to 'en'.")
            detected_lang = "en"
    

    audio_lang = detected_lang
        
    return script_text, detected_lang, audio_lang


def generate_timestamps_with_whisper(audio_file, text, timestamps_file):
    
    try:
        print("Loading Whisper model (base)...")
        model = whisper.load_model("base")
        
        print("Generating word timestamps...")
        result = model.transcribe(audio_file, word_timestamps=True, verbose=False)
        
        word_timestamps = []
        for segment in result['segments']:
            for word in segment['words']:
                word_timestamps.append({
                    "word": word['word'].strip(),
                    "start": word['start'],
                    "end": word['end']
                })

        with open(timestamps_file, 'w', encoding='utf-8') as f:
            json.dump(word_timestamps, f, ensure_ascii=False, indent=4)

        print("Phase 2 Complete! Timestamps saved to timestamps.json")
        
    except Exception as e:
        print(f"Error during Whisper transcription: {e}")
        sys.exit(1)



def phase_1_audio_generation():
    """Handles Phase 1: Audio generation and duration calculation/saving."""
    script_text, detected_lang, audio_lang = load_text_and_detect_lang()
    
    print("--------------------------------------------------")
    print(f" Phase 1: Audio Generation for Language: {detected_lang} (Audio: {audio_lang})")
    print("--------------------------------------------------")

   
    audio_text = script_text
    if detected_lang == 'mni' and os.path.exists("script_audio.txt"):
        with open("script_audio.txt", 'r', encoding='utf-8') as f:
            audio_text = f.read().strip()
        print("INFO: Using English text for Manipuri audio generation")

    success, duration = generate_audio(audio_text, OUTPUT_WAV_FILE, audio_lang)
    
    if not success:
        print("Audio generation failed. Aborting workflow.")
        sys.exit(1)
        
    print(f"Phase 1 Complete! Audio created and duration (%.2fs) saved to %s." % (duration, DURATION_FILE))


def phase_2_and_3_merge_and_cleanup():
    
    script_text, detected_lang, audio_lang = load_text_and_detect_lang()
    
    print("--------------------------------------------------")
    print(f" Phases 2 & 3: Timestamp/Merge for Language: {detected_lang} (Audio: {audio_lang})")
    print("--------------------------------------------------")

 
    
    if detected_lang == "en" or detected_lang == "mni":
        print(f"\n--- Phase 2: Generating Word Timestamps using Whisper ({detected_lang}) ---")
        generate_timestamps_with_whisper(OUTPUT_WAV_FILE, script_text, OUTPUT_TIMESTAMPS_FILE)
    else:
        print(f"\n--- Phase 2: Skipping Whisper timestamp generation for {detected_lang} (no subtitles needed). ---")
        if os.path.exists(OUTPUT_TIMESTAMPS_FILE):
             os.remove(OUTPUT_TIMESTAMPS_FILE)
             print(f"Cleaned up {OUTPUT_TIMESTAMPS_FILE}")

    if not handle_subtitles_and_merge(
        detected_lang, 
        INPUT_VIDEO_FILE, 
        OUTPUT_WAV_FILE, 
        OUTPUT_TIMESTAMPS_FILE, 
        OUTPUT_VIDEO_NO_AUDIO, 
        OUTPUT_VIDEO_FINAL
    ):
        print("Final video merge failed. Aborting workflow.")
        sys.exit(1)

    
    
    print("\n--- Finalizing and Cleaning Up ---")
    
    
    if os.path.exists(DURATION_FILE):
        os.remove(DURATION_FILE)
        print(f"Cleaned up {DURATION_FILE}")
        
    
    if os.path.exists(OUTPUT_WAV_FILE):
        os.remove(OUTPUT_WAV_FILE)
        print(f"Cleaned up {OUTPUT_WAV_FILE}")
    
    
   
    if (detected_lang == "en" or detected_lang == "mni") and os.path.exists(OUTPUT_VIDEO_NO_AUDIO):
        os.remove(OUTPUT_VIDEO_NO_AUDIO)
        print(f"Cleaned up {OUTPUT_VIDEO_NO_AUDIO}")


    print("--------------------------------------------------")
    print(f" Success! The final video is ready at {OUTPUT_VIDEO_FINAL}")
    print("--------------------------------------------------")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == "audio":
            phase_1_audio_generation()
        elif mode == "merge":
            phase_2_and_3_merge_and_cleanup()
        else:
            print("Usage: python main.py [audio | merge]")
            sys.exit(1)
    else:
        print("FATAL ERROR: Script must be run with a mode argument: 'audio' or 'merge'")
        sys.exit(1)