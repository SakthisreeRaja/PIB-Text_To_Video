import os
import ffmpeg
import sys
# Import the rendering function, which lives in a sibling file
from render_video import render_video_cv 

# ----------------------------------------------------------------------
# --- Audio-Video Merge for Non-Subtitled Languages (e.g., Tamil) ---
# ----------------------------------------------------------------------

def copy_audio_to_video(video_input, audio_input, video_output):
    """
    Uses FFmpeg to merge an existing silent video track with a separate 
    audio track. This is the function that runs for Tamil (ta) and uses 
    the stable 'libmp3lame' codec and outputs to the robust MKV container.
    """
    
    if not os.path.exists(audio_input):
        print(f"ERROR: Audio file not found at {audio_input}. Cannot merge.")
        return False
        
    video_stream = ffmpeg.input(video_input) 
    audio_stream = ffmpeg.input(audio_input)

    print(f"Merging audio ({os.path.basename(audio_input)}) into video ({os.path.basename(video_input)})...")

    try:
        (
            ffmpeg
            .output(video_stream.video, audio_stream.audio, 
                    video_output, 
                    vcodec='copy',           # Copy the video stream (fast)
                    acodec='libmp3lame',     # CRITICAL FIX: Use the stable MP3 encoder
                    audio_bitrate='192k',    # Ensure high quality MP3 audio
                    shortest=None,
                    loglevel='warning') 
            .run(overwrite_output=True)
        )
        print(f"Direct merge complete. Final video saved to {video_output}")
        return True 
    except ffmpeg.Error as e:
        # Print the detailed FFmpeg error output if it fails
        print("\n--- FFmpeg Merge Error Details ---")
        print(f"Error Message: {e.stderr.decode('utf8', errors='ignore') if e.stderr else 'No detailed stderr output.'}")
        print("---------------------------------------")
        print(f"FFmpeg Error during direct audio merge: {e}. Check if FFmpeg is installed and in PATH.")
        return False

# ----------------------------------------------------------------------
# --- Main Logic Dispatcher ---
# ----------------------------------------------------------------------

def handle_subtitles_and_merge(lang_code, input_video_file, output_wav_file, output_timestamps_file, output_video_no_audio, output_video_final):
    """
    Routes the workflow based on the language code.
    - 'en' triggers the complex frame-by-frame subtitle rendering.
    - Any other language triggers a simple audio merge (for Tamil, 'ta').
    """
    
    if lang_code == "en":
        print("\n--- Phase 3: Rendering Subtitles (English Only) ---")
        
        # This calls render_video.py
        return render_video_cv(
            input_video_file,
            output_wav_file,
            output_timestamps_file,
            output_video_no_audio,
            output_video_final # This will be the new .mkv name
        )
    else:
        print(f"\n--- Phase 3: Skipping Subtitles (Language: {lang_code}). Merging Audio directly. ---")
        
        # This runs the simple FFmpeg merge for non-English languages
        return copy_audio_to_video(input_video_file, output_wav_file, output_video_final)

if __name__ == "__main__":
    # Example usage block (not used in the main pipeline)
    if len(sys.argv) < 7:
        print("Usage: python subtitles.py <lang_code> <input_video> <output_wav> <timestamps_file> <temp_video> <final_video>")
        sys.exit(1)
        
    lang_code = sys.argv[1]
    input_video_file = sys.argv[2]
    output_wav_file = sys.argv[3]
    output_timestamps_file = sys.argv[4]
    output_video_no_audio = sys.argv[5]
    output_video_final = sys.argv[6]
    
    if not handle_subtitles_and_merge(lang_code, input_video_file, output_wav_file, output_timestamps_file, output_video_no_audio, output_video_final):
        sys.exit(1)