from moviepy.editor import VideoClip,CompositeVideoClip,VideoFileClip
from moviepy.video.tools.drawing import circle,color_gradient

def apply_transition(clips:list , transitions:list , duration:list)->VideoClip:
    transitions_types = {"crossfade":CrossFadeClip,"linear":LinearClip,"fadein":FadeInClip,"fadeout":FadeOutClip,"fadeinout":FadeInOutClip,"circle":CircleClip}
    if len(clips)-1 != len(transitions) or len(clips)-1 != len(duration):
        return None
    for i in range(len(clips)-1):
        clip1 = clips[i]
        clip2 = clips[i+1]
        transition_type = transitions[i]
        transition_duration = duration[i]
        clips[i+1] = transitions_types[transition_type](clip1,clip2,transition_duration)
        
    return clips[-1]

def CrossFadeClip(clip1: VideoClip, clip2: VideoClip, duration: float) -> VideoClip:
    
    clip1 = clip1.crossfadeout(duration)
    clip2 = clip2.crossfadein(duration)
    return CompositeVideoClip([clip1, clip2.set_start(clip1.end)])

def LinearClip(clip1: VideoClip, clip2: VideoClip, duration: float) -> VideoClip:
    
    return CompositeVideoClip([clip1.set_start(0), clip2.set_start(clip1.end)])

def FadeInClip(clip1: VideoClip, clip2: VideoClip, duration: float) -> VideoClip:
    
    return CompositeVideoClip([clip1.set_start(0), clip2.fadein(duration).set_start(clip1.end)])

def FadeOutClip(clip1: VideoClip, clip2: VideoClip, duration: float) -> VideoClip:
    clip = VideoClip(duration=duration,size=(clip1.h,clip1.w))
    return CompositeVideoClip([clip1.set_start(0),clip.set_start(clip1.end-duration) ,clip2.set_start(clip1.end)])

def FadeInOutClip(clip1: VideoClip, clip2: VideoClip, duration: float) -> VideoClip:
    
    return CompositeVideoClip([clip1.subclip(0,clip1.end-duration),clip1.subclip(clip1.end-duration,clip1.end).fadeout(duration).set_start(clip1.end-duration), clip2.set_opacity(0).fadein(duration).fadeout(duration).set_start(clip1.end)])

def CircleClip(clip1: VideoClip, clip2: VideoClip, duration: float) -> VideoClip:
    #make radius dynamic
    clip = clip1.subclip(clip1.end-duration,clip1.end)
    clip.add_mask()
    clip.mask.get_frame = lambda t: color_gradient(
    size=(clip1.w,clip1.h),
    p1=(clip1.w/2,clip1.h/4),
    vector=[1], 
    r=max(0,int(800-200*t)),
    shape='radial',
    col1=1, col2=0
    )
   
    print(clip.mask)
    return CompositeVideoClip([clip1.subclip(0,clip1.end-duration),clip.set_start(clip1.end-duration), clip2.set_start(clip1.end)])
def Slide(clip1: VideoClip, clip2: VideoClip,slide_duration: float,duration: float ) -> VideoClip:
    start_x = clip1.w  
    end_x = (clip1.w - clip2.w) // 2  
    y = (clip1.h - clip2.h) // 2  
    

    def slide_right_to_middle(t):
        if t <= slide_duration:
            
            return (start_x - (start_x - end_x) * (t / slide_duration), y)
        else:

            return (end_x, y)
    
    # Apply the position function to clip2 during the sliding phase
    sliding_clip = clip2.set_position(slide_right_to_middle).set_start(0).set_duration(slide_duration+duration)
            
    return CompositeVideoClip([clip1,sliding_clip])
def main():
    
    clip = VideoFileClip("Test_video.mp4")
    
    clip1 = clip.subclip(0, 15)
    clip2 = clip.subclip(5, 10).resize(width=clip1.w/2,height=clip1.h/2)
    clip3 = clip.subclip(10, 18)
    # clips = [clip1,clip2,clip3]
    # transtions = ["crossfade","fadein"]
    # duration = [3,3]
    # final =apply_transition(clips,transtions,duration)
    final = Slide(clip1,clip2,1,5)
    final.write_videofile("output_video_t.mp4")

if __name__ == "__main__":
    main()