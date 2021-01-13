'''Converts HVX raw files to .mp4 videos.'''

import argparse
import os
from pathlib import Path
import time

import moviepy.editor as mp

FRAME_SIZE = (1920,1080)
VIDEO = 'VIDEO'
AUDIO = 'AUDIO'
MP4 = '.MP4'
MXF = '.MXF'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--c-dir', type=str, default = './CONTENTS/', help="Path to 'CONTENTS' directory")
    parser.add_argument('--out-dir', type=str, default = None, help="Directory to save converted videos. If left 'None' then new output folder is generated instead.")
    parser.add_argument('--time-base', type=bool, default = False, help="If set 'True' with 'out-dir' argument, base folder given name with timestamp.")    
    args = parser.parse_args()

    t = time.localtime()
    if args.out_dir is None:
        out_dir = 'videos_' + time.strftime('%m%d%Y_%H%M%S', t)
    else:
        if args.time_base:
            out_dir = Path(args.out_dir, time.strftime('%m%d%Y_%H%M%S', t))

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    num_vids = str(len(os.listdir(Path(args.c_dir, VIDEO))))
    vid_list = os.listdir(Path(args.c_dir, VIDEO))
    for cnt, sample in enumerate(vid_list):
        print("Video " + str(cnt) + " of " + num_vids)
        base = os.path.splitext(sample)[0]
        audiobase = base + '00' + MXF
        audioclip = mp.AudioFileClip(str(Path(args.c_dir, AUDIO, audiobase)))
        clip = mp.VideoFileClip(str(Path(args.c_dir, VIDEO, sample)))
        clip = clip.resize(FRAME_SIZE)
        clip.audio = audioclip
        clip = clip.volumex(6)

        converted_file = str(Path(out_dir, base + MP4))
        clip.write_videofile(converted_file,
        codec='libx264', 
        audio_codec='aac', 
        remove_temp=True
        )    

    os.remove(args.c_dir)
         
if __name__ == "__main__":
    main()