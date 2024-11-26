from AutoSubtitles import AutoSubtitles
import Transitions
from moviepy.editor import TextClip
def main():
    sub = AutoSubtitles("Test_video.mp4").write_subtitles(font_size=36,color="black")
    clip1 = sub.subclip(0, 6)
    clip2 = sub.subclip(6, 12)
    clip3 = sub.subclip(12, 18)
    clip4 = TextClip("The End", fontsize=64,color="white").set_position(("center")).set_duration(2)
    transitions = ["crossfade","linear","circle"]
    duration = [3,4,4]
    final = Transitions.apply_transition([clip1,clip2,clip3,clip4],transitions,duration)
    # final.preview(fps=24)
    final.write_videofile("output_video_ts.mp4") 
if __name__ == "__main__":  
    main()