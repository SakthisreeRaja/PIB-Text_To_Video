import cv2
import json
import os
import subprocess 
import numpy as np
from PIL import Image, ImageDraw, ImageFont 
import ffmpeg 
from config import INPUT_VIDEO_FILE, OUTPUT_VIDEO_FINAL, OUTPUT_VIDEO_NO_AUDIO


FONT_PATH = "NotoSans-Bold.ttf" 
FONT_SIZE = 40
TEXT_COLOR_RGB = (255, 255, 255)
HIGHLIGHT_COLOR_RGB = (255, 255, 0)
OUTLINE_COLOR_RGB = (0, 0, 0)
MAX_TEXT_WIDTH_FACTOR = 0.8 


try:
    PIL_FONT = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    LINE_SPACING = FONT_SIZE + 15 
    print(f"Font loaded successfully from {FONT_PATH}.")
except IOError:
    print(f"FATAL ERROR: Font file not found at {FONT_PATH}. Please ensure 'NotoSans-Bold.ttf' is in the same directory.")
    PIL_FONT = ImageFont.load_default()
    LINE_SPACING = 30 


WRAPPED_SENTENCE_CACHE = {} 


def get_text_width(text, font):
    
    try:
        if hasattr(font, 'getlength'):
            return font.getlength(text)
        return font.getsize(text)[0]
    except Exception:
        try:
             bbox = font.getbbox(text)
             return bbox[2] - bbox[0]
        except Exception:
             return font.getsize(text)[0]


SPACE_WIDTH = get_text_width(" ", PIL_FONT)


def wrap_sentence(sentence_words, frame_width):
    
    sentence_text = " ".join([w['word'] for w in sentence_words])
    cache_key = sentence_text

    if cache_key in WRAPPED_SENTENCE_CACHE:
        return WRAPPED_SENTENCE_CACHE[cache_key]

    max_width = int(frame_width * MAX_TEXT_WIDTH_FACTOR)
    
    def get_line_width(words):
        
        test_line = " ".join([w['word'] for w in words])
        return get_text_width(test_line, PIL_FONT)

    wrapped_lines = []
    current_line_words = []
    
    for word_info in sentence_words:
        test_line_words = current_line_words + [word_info]
        
        if current_line_words and get_line_width(test_line_words) > max_width:
            wrapped_lines.append(current_line_words)
            current_line_words = [word_info]
        else:
            current_line_words.append(word_info)
    
    if current_line_words:
        wrapped_lines.append(current_line_words)
    
    WRAPPED_SENTENCE_CACHE[cache_key] = wrapped_lines
    return wrapped_lines


def draw_dynamic_text(frame, word_data, current_time):
    
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]
    
    
    sentence_start_index = 0
    sentence_end_index = len(word_data)
    
    for i in range(len(word_data)):
        word_info = word_data[i]
        
        
        if current_time >= word_info['end'] and word_info.get('sentence_end'):
            sentence_start_index = i + 1
        
        if current_time < word_info['end']:
            for j in range(i, len(word_data)):
                if word_data[j].get('sentence_end'):
                    sentence_end_index = j + 1
                    break
            break 
            
    window_word_data = word_data[sentence_start_index:sentence_end_index]
    
    if not window_word_data or current_time < window_word_data[0]['start']:
        return frame 

    wrapped_lines = wrap_sentence(window_word_data, frame_width)
    
    total_text_height = len(wrapped_lines) * LINE_SPACING 
    bottom_anchor = int(frame_height * 0.75) 
    current_y = bottom_anchor - total_text_height 
    
    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)

    for line_words_data in wrapped_lines:
        
        line_width = get_text_width(" ".join([w['word'] for w in line_words_data]), PIL_FONT)
        current_x = (frame_width - line_width) // 2
        
        for i, word_info in enumerate(line_words_data):
            
            word = word_info['word']
            is_active = word_info['start'] <= current_time < word_info['end']
            color = HIGHLIGHT_COLOR_RGB if is_active else TEXT_COLOR_RGB
             
            for offset_x in [-2, 0, 2]:
                for offset_y in [-2, 0, 2]:
                    if offset_x == 0 and offset_y == 0: continue
                    draw.text(
                        (current_x + offset_x, current_y + offset_y), 
                        word, 
                        font=PIL_FONT, 
                        fill=OUTLINE_COLOR_RGB # Black
                    )
            
             
            draw.text(
                (current_x, current_y), 
                word, 
                font=PIL_FONT, 
                fill=color
            )
            
            word_width = get_text_width(word, PIL_FONT)
            current_x += word_width
            
             
            if i < len(line_words_data) - 1:
                current_x += SPACE_WIDTH
        
        current_y += LINE_SPACING
        
    
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)




def render_video_cv(video_file, audio_file, timestamp_file, output_no_audio, output_final):
    WRAPPED_SENTENCE_CACHE.clear() 

    try:
        with open(timestamp_file, 'r', encoding='utf-8') as f:
            word_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Timestamps file not found at {timestamp_file}")
        return False 
    
    
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"Error: Could not open input video file {video_file}")
        return False 

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps == 0:
        print("Warning: Could not get video FPS. Defaulting to 24.")
        fps = 24.0 
        
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    if frame_width == 0 or frame_height == 0:
        print(f"Error: Invalid video dimensions ({frame_width}x{frame_height}).")
        return False 

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_no_audio, fourcc, fps, (frame_width, frame_height))
    
    current_frame_number = 0
    print(f"Starting frame-by-frame rendering at {fps} FPS...")
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            current_frame_number += 1
            current_time = current_frame_number / fps

            frame = draw_dynamic_text(frame, word_data, current_time)
            out.write(frame)
    except Exception as e:
        print(f"FATAL ERROR during frame processing (OpenCV/Pillow): {e}")
        cap.release()
        out.release()
        return False 

    cap.release()
    out.release()
    print("Video track rendered successfully (no audio).")

    print("Merging audio and video tracks...")
    
    video_stream = ffmpeg.input(output_no_audio) 
    audio_stream = ffmpeg.input(audio_file)

    try:
        (
            ffmpeg
            .output(video_stream.video, audio_stream.audio, 
                    output_final, 
                    vcodec='copy', 
                    acodec='aac', 
                    shortest=None,
                    loglevel='quiet')
            .run(overwrite_output=True)
        )
        
        if os.path.exists(output_no_audio):
             os.remove(output_no_audio) 
             
        print(f"✨ Final video saved to {output_final} ✨")
        return True 
    except ffmpeg.Error:
        print(f"FFmpeg Error: Could not merge audio/video. Check if ffmpeg is installed.")
        return False


if __name__ == "__main__":
    pass