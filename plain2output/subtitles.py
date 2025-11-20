import os
import ffmpeg
import sys
from render_video import render_video_cv 


def copy_audio_to_video(video_input, audio_input, video_output):
    
    
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
                    vcodec='copy',           
                    acodec='libmp3lame',     
                    audio_bitrate='192k',    
                    shortest=None,
                    loglevel='warning') 
            .run(overwrite_output=True)
        )
        print(f"Direct merge complete. Final video saved to {video_output}")
        return True 
    except ffmpeg.Error as e:
       
        print("\n--- FFmpeg Merge Error Details ---")
        print(f"Error Message: {e.stderr.decode('utf8', errors='ignore') if e.stderr else 'No detailed stderr output.'}")
        print("---------------------------------------")
        print(f"FFmpeg Error during direct audio merge: {e}. Check if FFmpeg is installed and in PATH.")
        return False



def handle_subtitles_and_merge(lang_code, input_video_file, output_wav_file, output_timestamps_file, output_video_no_audio, output_video_final):
    
    if lang_code == "en":
        print("\n--- Phase 3: Rendering Subtitles (English Only) ---")
        
        
        return render_video_cv(
            input_video_file,
            output_wav_file,
            output_timestamps_file,
            output_video_no_audio,
            output_video_final
        )
    else:
        print(f"\n--- Phase 3: Skipping Subtitles (Language: {lang_code}). Merging Audio directly. ---")
        
        
        return copy_audio_to_video(input_video_file, output_wav_file, output_video_final)

if __name__ == "__main__":
    
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