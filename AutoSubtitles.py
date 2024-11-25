import os
from whisper import load_model
from moviepy.editor import VideoFileClip,VideoClip,CompositeVideoClip,TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
class AutoSubtitles:
    def __init__(self,video_path:str):
        """
        Parameters
        ----------
        video_path : str
            The path to the video file to be processed.
        output_path : str, optional
            The path to save the output video file to. Defaults to "output_video.mp4".
        """
        self.audio_path :str= "temp_audio.wav"
        self.video = VideoFileClip(video_path,audio=True)  
    def get_audio(self,audio_path :str|None=None)->None:
        """
        Extracts the audio from the video and saves it to a file.

        Parameters
        ----------
        audio_path : str, optional
            The path to save the audio file to. If not provided, the audio is saved to "temp_audio.wav".

        Returns
        -------
        None
        """
        print("Extracting audio...")
        audio = self.video.audio
        if audio_path:
            audio.write_audiofile(audio_path)
        else:
            audio.write_audiofile(self.audio_path)
        
    def get_subtitles(self):
        """
        Gets the subtitles for the video.

        Returns
        -------
        list
            A list of tuples, where each tuple contains the start and end time of a subtitle segment, and the text of the segment.
        """
        self.get_audio()
        print("Generating subtitles...")
        model = load_model("base")
        result = model.transcribe(self.audio_path)
        os.remove(self.audio_path)
        print("Writing subtitles ...")
        subtitles = []
        for i, segment in enumerate(result["segments"]):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            subtitles.append(((start, end), text))
        return subtitles

    def write_subtitles(self,font: str = "Arial", font_size: int = 24, color: str = "white",bg_color: str = "transparent")->VideoClip:
        """
        Embeds subtitles into the video and saves the resulting video to the specified output path.
        
        Parameters
        ----------
        font : str
            The font to use for the subtitle text.
        font_size : int
            The size of the font for the subtitle text.
        color : str
            The color of the subtitle text in string format (e.g., 'white', 'black').

        Returns
        -------
        None
        """
        subtitles = self.get_subtitles()
        print("Embedding subtitles into video...")
        def generator(text):
            return TextClip(text, fontsize=font_size,font=font, color=color,method='caption',size=(self.video.w*0.9,None),bg_color=bg_color)
        sub = SubtitlesClip(subtitles, generator)
        final = CompositeVideoClip([self.video, sub.set_position(("center",0.8),relative=True)])
        return final
#Example usage
def main():
    video_path = "Test_video.mp4"  
    output_path = "output_video.mp4"  
    font = "Arial"
    font_size = 36
    color = "black"
    subtitles = AutoSubtitles(video_path)
    sub = subtitles.get_subtitles()
    print(sub)
    final =subtitles.write_subtitles(font,font_size,color)
    final.write_videofile(output_path)

    
    
if __name__ == "__main__":
    main()
