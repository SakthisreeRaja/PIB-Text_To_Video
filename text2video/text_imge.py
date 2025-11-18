import os
import sys
import time
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image

# Assuming config is in the parent directory for a script executed in text2video/
# We need a fallback path, as the execution environment is different.
try:
    # Try importing from the main config file in plain2output directory
    # Adjust path to find config.py one level up in plain2output
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'plain2output'))
    from config import INPUT_VIDEO_FILE, DURATION_FILE
    CONFIG_LOADED = True
except ImportError as e:
    # Fallback if config import fails (used when running script directly)
    print(f"Warning: Could not import config. Using default file names. Error: {e}")
    INPUT_VIDEO_FILE = "input_video.mp4"
    DURATION_FILE = "video_duration.txt"
    CONFIG_LOADED = False

# --- Patch for MoviePy/Pillow Resizing (Unchanged) ---
def patch_moviepy_filter(original_filter):
    def patched_filter(get_frame, t, resize_width, resize_height):
        img = Image.fromarray(get_frame(t), 'RGB')
        # Use Image.LANCZOS for high quality resizing
        resized_img = img.resize((resize_width, resize_height), resample=Image.LANCZOS) 
        return original_filter(resized_img, t)
    return patched_filter

try:
    from moviepy.decorators import apply_to_mask
    apply_to_mask.filter = patch_moviepy_filter(apply_to_mask.filter)
    # print("✅ Pillow/MoviePy resizing filter patched successfully.")
except Exception:
    pass
# --- End Patch ---


def get_image_files(directory):
    """Finds all common image files in a directory."""
    image_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    return sorted([
        os.path.join(directory, f) 
        for f in os.listdir(directory) 
        if f.lower().endswith(image_extensions)
    ])

def create_video_from_images(image_paths, total_duration, output_file="input_video.mp4"):
    """Creates a silent video from a list of images with a total specified duration."""
    
    if not image_paths:
        print("FATAL ERROR: No images found for video assembly.")
        return

    num_images = len(image_paths)
    
    # CRITICAL: Calculate duration per image based on the required total duration
    if total_duration <= 0 or num_images == 0:
        print("FATAL ERROR: Cannot create video. Duration is zero or no images found.")
        return
        
    duration_per_image = total_duration / num_images
    
    print("\n--- Starting Video Assembly ---")
    print(f"Total Images: {num_images}")
    print(f"Total Required Duration: {total_duration:.2f} seconds")
    print(f"Duration per image: {duration_per_image:.2f} seconds")

    clips = []
    
    # Determine a consistent target size 
    base_width, base_height = 1200, 675 # Standardized vertical reel size 
    try:
        img = Image.open(image_paths[0])
        # Use a standardized resolution for reels
        print(f"Found base size: {base_width}x{base_height}")
    except Exception:
        pass


    for path in image_paths:
        try:
            print(f" -> Processing clip for {os.path.basename(path)}...")
            current_width, current_height = Image.open(path).size
            
            # Resize if necessary to match the base size (1200x675)
            if current_width != base_width or current_height != base_height:
                print(f" -> Resizing from ({current_width}, {current_height}) to ({base_width}, {base_height})")
                
            clip = ImageClip(path, duration=duration_per_image).set_fps(24).resize(newsize=(base_width, base_height))
            clips.append(clip)
            
        except Exception as e:
            print(f"Error processing image {os.path.basename(path)}: {e}. Skipping.")

    if not clips:
        print("FATAL ERROR: Could not create any video clips.")
        return

    print(f"\n--- Stitching all {len(clips)} valid clips together ---")
    final_clip = concatenate_videoclips(clips, method="compose")

    # Write the result (no audio)
    start_time = time.time()
    final_clip.write_videofile(
        output_file,
        codec='libx264',
        audio_codec='aac', # Keep a silent AAC track for merge stability
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        fps=24,
        verbose=False,
        logger=None # Suppress MoviePy output
    )
    
    print(f"Write time: {time.time() - start_time:.2f}s")
    print(f"✅ SUCCESS! Video sequence saved to {output_file}")
    print(f"Final video length: {final_clip.duration:.2f} seconds.")

    # Clean up
    for clip in clips:
        clip.close()

# ----------------------------------------------------------------------
# --- Main Execution ---
# ----------------------------------------------------------------------

if __name__ == "__main__":
    
    # --- 1. Determine Target Duration ---
    target_duration = 30.0 # Default fallback duration
    
    if os.path.exists(DURATION_FILE):
        try:
            with open(DURATION_FILE, 'r') as f:
                target_duration = float(f.read().strip())
            print(f"✅ Found audio duration in {DURATION_FILE}. Target video duration set to {target_duration:.2f} seconds.")
        except Exception as e:
            print(f"⚠️ Warning: Could not read duration from {DURATION_FILE}. Falling back to default {target_duration}s. Error: {e}")
    else:
        print(f"⚠️ Warning: {DURATION_FILE} not found. Falling back to default {target_duration}s. ENSURE Phase 1 ran first.")
        
    
    # --- 2. Find Images ---
    image_paths = get_image_files('assets')
    if not image_paths:
        print("🔍 Searching primary directory: assets...")
        print("⚠️ Primary directory 'assets' empty or not found. Checking backup: backup_assets...")
        image_paths = get_image_files('backup_assets')
        if image_paths:
            print(f"✅ Found {len(image_paths)} images in backup_assets. Using these.")
        else:
            print("FATAL ERROR: No images found in primary or backup directories. Aborting.")
            sys.exit(1)

    # --- 3. Create Video ---
    create_video_from_images(image_paths, target_duration, INPUT_VIDEO_FILE)