import os
import ffmpeg
import sys
from render_video import render_video_cv

def copy_audio_to_video(video_input, audio_input, video_output):
    if not os.path.exists(audio_input):
        return False

    video_stream = ffmpeg.input(video_input)
    audio_stream = ffmpeg.input(audio_input)

    try:
        (
            ffmpeg
            .output(video_stream.video, audio_stream.audio,
                    video_output,
                    vcodec='copy',
                    acodec='aac',
                    shortest=None,
                    loglevel='error')
            .run(overwrite_output=True)
        )
        return True
    except ffmpeg.Error:
        return False

def handle_subtitles_and_merge(lang_code, input_video_file, output_wav_file, output_timestamps_file, output_video_no_audio, output_video_final):

    if lang_code == "en" or lang_code == "mni":
        return render_video_cv(
            input_video_file,
            output_wav_file,
            output_timestamps_file,
            output_video_no_audio,
            output_video_final,
            lang_code  
        )
    else:
        return copy_audio_to_video(input_video_file, output_wav_file, output_video_final)

if __name__ == "__main__":
    if len(sys.argv) < 7:
        sys.exit(1)

    lang_code = sys.argv[1]
    input_video_file = sys.argv[2]
    output_wav_file = sys.argv[3]
    output_timestamps_file = sys.argv[4]
    output_video_no_audio = sys.argv[5]
    output_video_final = sys.argv[6]

    if not handle_subtitles_and_merge(lang_code, input_video_file, output_wav_file, output_timestamps_file, output_video_no_audio, output_video_final):
        sys.exit(1)