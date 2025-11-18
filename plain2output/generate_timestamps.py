import whisper
import json
import os
import re 
from config import OUTPUT_WAV_FILE, OUTPUT_TIMESTAMPS_FILE 

def generate_word_timestamps(audio_file, output_file, lang_code, text_prompt):
    
    if not os.path.exists(audio_file):
        print(f"Error: Audio file not found at {audio_file}")
        return False
        
    print("Loading Whisper model (base)...")
    try:
        model = whisper.load_model("base") 
    except Exception as e:
        print(f"ERROR: Failed to load Whisper model: {e}")
        return False
    
    print("Generating word timestamps...")
    
    
    initial_prompt = text_prompt[:50] 

    
    try:
        result = model.transcribe(
            audio_file, 
            word_timestamps=True,
            language=lang_code,
            condition_on_previous_text=False,
            initial_prompt=initial_prompt
        )
    except Exception as e:
        print(f"ERROR during Whisper transcription: {e}")
        return False
    
    
    print("\n--- Whisper Transcription Result ---")
    print(f"Whisper Text:       {result.get('text', 'No transcription found').strip()}")
    print("----------------------------------\n")
    
    final_word_data = []
    

    for segment in result.get('segments', []):
        if 'words' in segment:
            for word in segment['words']:
                
                if 'word' in word and 'start' in word and 'end' in word:
                    
                    cleaned_word = word['word'].strip()
                    
                    word_entry = {
                        'word': cleaned_word,
                        'start': float(word['start']), 
                        'end': float(word['end'])
                    }
                    
                    if cleaned_word and cleaned_word[-1] in ['.', '!', '?', '।']: 
                        word_entry["sentence_end"] = True
                        
                    final_word_data.append(word_entry)
                

    if not final_word_data:
        print("ERROR: Whisper produced an empty transcription. Check audio file quality.")
        return False
        
    print(f"First extracted word in JSON: '{final_word_data[0]['word']}'")
    

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_word_data, f, indent=4, ensure_ascii=False)
        
    print(f"Phase 2 Complete! Timestamps saved to {output_file}")
    return True

if __name__ == "__main__":
    if os.path.exists(OUTPUT_WAV_FILE):
        example_text = "A motivation speech inspires an audience to change and take action."
        generate_word_timestamps(OUTPUT_WAV_FILE, OUTPUT_TIMESTAMPS_FILE, "en", example_text)
    else:
        print("Run generate_audio.py first to create temp_audio.wav")