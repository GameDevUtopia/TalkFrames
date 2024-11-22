import os
import subprocess
from whisper import load_model


def process_video(video_path, output_path):
 
    print("Extracting audio...")
    audio_path = "temp_audio.wav"
    command_extract_audio = f"ffmpeg -i \"{video_path}\" -q:a 0 -map a \"{audio_path}\" -y"
    subprocess.run(command_extract_audio, shell=True, check=True)

   
    print("Generating subtitles...")
    model = load_model("base")
    result = model.transcribe(audio_path)

  
    print("Writing subtitles to SRT file...")
    srt_path = "temp_subtitles.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"]):
            start = format_time(segment["start"])
            end = format_time(segment["end"])
            text = segment["text"]
            f.write(f"{i + 1}\n{start} --> {end}\n{text}\n\n")

    print("Embedding subtitles into video...")
    command_add_subtitles = f"ffmpeg -i \"{video_path}\" -vf subtitles=\"{srt_path}\" \"{output_path}\" -y"
    subprocess.run(command_add_subtitles, shell=True, check=True)

  
    print("Cleaning up temporary files...")
    os.remove(audio_path)
    os.remove(srt_path)

    print(f"Subtitled video saved as: {output_path}")


def format_time(seconds):
    millis = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return f"{hours:02}:{mins:02}:{secs:02},{millis:03}"

# Main function
def main():
    video_path = "test3.mp4"  
    output_path = "output_video.mp4"  

    if not os.path.exists(video_path):
        print(f"Error: The file '{video_path}' does not exist.")
        return

    process_video(video_path, output_path)

if __name__ == "__main__":
    main()
