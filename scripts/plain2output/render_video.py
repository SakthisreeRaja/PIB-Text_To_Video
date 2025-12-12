import cv2
import json
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import ffmpeg
from config import INPUT_VIDEO_FILE, OUTPUT_VIDEO_FINAL, OUTPUT_VIDEO_NO_AUDIO

FONT_PATH = "NotoSans-Bold.ttf"
FONT_PATH_BENGALI = "NotoSansBengali.ttf"
FONT_PATH_MEITEI = "NotoSansMeeteiMayek-Regular.ttf"
FONT_SIZE = 36                      
TEXT_COLOR_RGB = (255, 255, 255)     
HIGHLIGHT_COLOR_RGB = (255, 223, 0) 
OUTLINE_COLOR_RGB = (0, 0, 0)
BOX_COLOR_RGBA = (0, 0, 0, 180)     
MAX_TEXT_WIDTH_FACTOR = 0.85         
MAX_LINES_VISIBLE = 2                

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_abs_path = os.path.join(current_dir, FONT_PATH)
    font_bengali_path = os.path.join(current_dir, FONT_PATH_BENGALI)
    font_meitei_path = os.path.join(current_dir, FONT_PATH_MEITEI)
    
    if os.path.exists(font_abs_path):
        PIL_FONT = ImageFont.truetype(font_abs_path, FONT_SIZE)
    else:
        PIL_FONT = ImageFont.truetype("arialbd.ttf", FONT_SIZE)
    
   
    if os.path.exists(font_bengali_path):
        PIL_FONT_BENGALI = ImageFont.truetype(font_bengali_path, FONT_SIZE)
    else:
        PIL_FONT_BENGALI = PIL_FONT
    
  
    if os.path.exists(font_meitei_path):
        PIL_FONT_MEITEI = ImageFont.truetype(font_meitei_path, FONT_SIZE)
    else:
        PIL_FONT_MEITEI = PIL_FONT
    
    LINE_SPACING = int(FONT_SIZE * 1.4)
except:
    PIL_FONT = ImageFont.load_default()
    PIL_FONT_BENGALI = PIL_FONT
    PIL_FONT_MEITEI = PIL_FONT
    LINE_SPACING = 40

WRAPPED_SENTENCE_CACHE = {}
CURRENT_FONT = None  

def get_text_width(text, font=None):
    if font is None:
        font = CURRENT_FONT or PIL_FONT
    try: return font.getlength(text)
    except: return font.getsize(text)[0]

def wrap_sentence(sentence_words, frame_width):
    sentence_text = " ".join([w['word'] for w in sentence_words])
    cache_key = sentence_text

    if cache_key in WRAPPED_SENTENCE_CACHE:
        return WRAPPED_SENTENCE_CACHE[cache_key]

    max_width = int(frame_width * MAX_TEXT_WIDTH_FACTOR)

    wrapped_lines = []
    current_line_words = []
    
    for word_info in sentence_words:
        test_line_words = current_line_words + [word_info]
        test_line_text = " ".join([w['word'] for w in test_line_words])
        
        if current_line_words and get_text_width(test_line_text) > max_width:
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
    
    if not window_word_data:
        return frame 

   
    all_wrapped_lines = wrap_sentence(window_word_data, frame_width)
    
  
    active_line_idx = 0
    for idx, line in enumerate(all_wrapped_lines):
        if not line: continue
        line_end_time = line[-1]['end']
        if current_time > line_end_time:
            active_line_idx = idx + 1
        if active_line_idx >= len(all_wrapped_lines):
            active_line_idx = len(all_wrapped_lines) - 1
    page_start = (active_line_idx // MAX_LINES_VISIBLE) * MAX_LINES_VISIBLE
    visible_lines = all_wrapped_lines[page_start : page_start + MAX_LINES_VISIBLE]

    
    total_text_height = len(visible_lines) * LINE_SPACING
    bottom_margin = 60
    start_y = frame_height - total_text_height - bottom_margin

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb_frame).convert("RGBA")
    overlay = Image.new("RGBA", pil_img.size, (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)

   
    max_visible_width = 0
    for line in visible_lines:
        w = get_text_width(" ".join([w['word'] for w in line]), PIL_FONT)
        if w > max_visible_width: max_visible_width = w
    
    box_padding_x = 30
    box_padding_y = 15
    
    box_left = (frame_width - max_visible_width) // 2 - box_padding_x
    box_right = (frame_width + max_visible_width) // 2 + box_padding_x
    box_top = start_y - box_padding_y
    box_bottom = start_y + total_text_height + box_padding_y

    draw_overlay.rectangle([(box_left, box_top), (box_right, box_bottom)], fill=BOX_COLOR_RGBA)

    pil_img = Image.alpha_composite(pil_img, overlay)
    draw = ImageDraw.Draw(pil_img)
    
    current_y = start_y

  
    for line_words_data in visible_lines:
        line_text = " ".join([w['word'] for w in line_words_data])
        line_width = get_text_width(line_text)
        current_x = (frame_width - line_width) // 2
        
        for i, word_info in enumerate(line_words_data):
            word = word_info['word']
            is_active = word_info['start'] <= current_time < word_info['end']
            fill_color = HIGHLIGHT_COLOR_RGB if is_active else TEXT_COLOR_RGB
            
            draw.text((current_x, current_y), word, font=CURRENT_FONT, fill=fill_color)
            
            current_x += get_text_width(word)
            if i < len(line_words_data) - 1:
                current_x += get_text_width(" ")
        
        current_y += LINE_SPACING
        
    return cv2.cvtColor(np.array(pil_img.convert("RGB")), cv2.COLOR_RGB2BGR)

def render_video_cv(video_file, audio_file, timestamp_file, output_no_audio, output_final, lang_code="en"):
    global CURRENT_FONT
    WRAPPED_SENTENCE_CACHE.clear() 
    
   
    if lang_code == 'mni':
        CURRENT_FONT = PIL_FONT_MEITEI
    elif lang_code in ['as', 'or', 'bn']:
        CURRENT_FONT = PIL_FONT_BENGALI
    else:
        CURRENT_FONT = PIL_FONT

    try:
        with open(timestamp_file, 'r', encoding='utf-8') as f:
            word_data = json.load(f)
    except FileNotFoundError:
        return False 
    
    
    if lang_code == 'mni':
        try:
            with open("script.txt", 'r', encoding='utf-8') as f:
                script_text = f.read().strip()
            
            import re
            script_words = re.findall(r'\S+', script_text)
            
        
            for i, word_info in enumerate(word_data):
                if i < len(script_words):
                    word_data[i]['word'] = script_words[i]
            
           
            if len(script_words) < len(word_data):
                word_data = word_data[:len(script_words)]
            
            print(f"INFO: Using Manipuri text for subtitles with English audio timing")
        except Exception as e:
            print(f"WARNING: Could not load Manipuri text: {e}")
    
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        return False 

    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_no_audio, fourcc, fps, (frame_width, frame_height))
    
    current_frame_number = 0
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
                
            current_frame_number += 1
            current_time = current_frame_number / fps

            frame = draw_dynamic_text(frame, word_data, current_time)
            out.write(frame)
    except Exception:
        cap.release()
        out.release()
        return False 

    cap.release()
    out.release()
    
    try:
        (
            ffmpeg
            .output(ffmpeg.input(output_no_audio).video, ffmpeg.input(audio_file).audio, 
                    output_final, 
                    vcodec='libx264', pix_fmt='yuv420p', acodec='aac', shortest=None, loglevel='error')
            .run(overwrite_output=True)
        )
        if os.path.exists(output_no_audio): os.remove(output_no_audio) 
        return True 
    except:
        return False