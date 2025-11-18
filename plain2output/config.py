# --- File Paths ---

# The source file containing the text script
SCRIPT_FILE = "script.txt" 

# The video created in the second step (Visual Input Preparation)
INPUT_VIDEO_FILE = "input_video.mp4" 

# Temporary files for audio and timestamps
OUTPUT_WAV_FILE = "temp_audio.wav"
OUTPUT_TIMESTAMPS_FILE = "timestamps.json"

# --- REQUIRED CONSTANTS for Duration and Merge/Subtitle ---
# File to store the calculated audio duration (in seconds)
DURATION_FILE = "video_duration.txt"

# The final video output file (using the stable MKV container)
OUTPUT_VIDEO_FINAL = "output_reel_final.mkv" 
# Temporary video file used only in the English workflow
OUTPUT_VIDEO_NO_AUDIO = "output_video_no_audio.mp4" 

# Font file for rendering subtitles 
FONT_PATH = "NotoSans-Bold.ttf"