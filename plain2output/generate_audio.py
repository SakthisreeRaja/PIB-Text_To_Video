from gtts import gTTS
import os
import ffmpeg
import time
import sys
from config import OUTPUT_WAV_FILE, DURATION_FILE 

# ----------------------------------------------------------------------
# --- New Function: Get Audio Duration ---
# ----------------------------------------------------------------------

def get_audio_duration(audio_file):
    """Probes the audio file using FFmpeg to get its duration in seconds."""
    try:
        # Use ffmpeg.probe to get metadata
        probe = ffmpeg.probe(audio_file)
        # Extract the duration from the stream data (duration of the first stream)
        duration = float(probe['streams'][0]['duration'])
        return duration
    except ffmpeg.Error as e:
        print(f"Error probing audio duration: {e}")
        return 0.0
    except Exception as e:
        print(f"Unexpected error getting audio duration: {e}")
        return 0.0

# ----------------------------------------------------------------------
# --- Main Audio Generation Function ---
# ----------------------------------------------------------------------

def generate_gtts_audio(text_prompt, output_wav, lang_code):
    temp_mp3 = "temp_gtts_audio.mp3"
    
    print(f"Generating audio for language code '{lang_code}' using gTTS...")
    start_time = time.time()
    
    # 1. Generate MP3 via gTTS
    try:
        tts = gTTS(text=text_prompt, lang=lang_code, slow=False)
        tts.save(temp_mp3)
        
        if not os.path.exists(temp_mp3) or os.path.getsize(temp_mp3) == 0:
            print(f"ERROR: gTTS failed to create a valid MP3 file.")
            return False, 0.0

    except Exception as e:
        print(f"Error generating gTTS audio: {e}")
        return False, 0.0

    
    # 2. Convert MP3 to WAV, Add Padding, and Save Final WAV
    try:
        # Convert and pad in a single pipeline for efficiency and reliability
        print(f"Converting MP3 to padded WAV and saving to {output_wav} (with 500ms lead-in silence)...")
        (
            ffmpeg
            .input(temp_mp3)
            .output(output_wav, 
                    acodec='pcm_s16le', 
                    ar=24000, 
                    af='adelay=500|500') # Add 500ms delay/padding
            .run(overwrite_output=True) 
        )
        os.remove(temp_mp3)
        
        # CRITICAL CHECK: Did the final conversion work and create content?
        if not os.path.exists(output_wav) or os.path.getsize(output_wav) == 0:
            print(f"FATAL ERROR: FFmpeg failed to convert/pad to WAV. {output_wav} is empty.")
            return False, 0.0
            
    except ffmpeg.Error as e:
        print("\n--- FFmpeg Conversion Error Details ---")
        print(f"Error Message: {e.stderr.decode('utf8', errors='ignore') if e.stderr else 'No detailed stderr output.'}")
        print("---------------------------------------")
        return False, 0.0
    except Exception as e:
        print(f"An unexpected error occurred during audio processing: {e}")
        return False, 0.0
        
    # 3. Calculate and Save Duration
    duration = get_audio_duration(output_wav)
    if duration > 0:
        with open(DURATION_FILE, 'w') as f:
            f.write(str(duration))
        print(f"Audio duration ({duration:.2f}s) saved to {DURATION_FILE}")
    else:
        print("Warning: Could not determine audio duration.")


    print(f"Audio generation took: {time.time() - start_time:.2f}s")
    
    # Return success status and duration
    return True, duration