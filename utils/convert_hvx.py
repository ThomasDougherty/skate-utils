#!/usr/bin/env python3
'''Converts HVX raw files to .mp4 videos.'''

import argparse
import os
from pathlib import Path
import time

import cv2
import moviepy.editor as mp

FRAME_SIZE = (1920,1080)
VIDEO = 'VIDEO'
AUDIO = 'AUDIO'
MP4 = '.MP4'
MXF = '.MXF'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--c-dir', type=str, help="Path to 'CONTENTS' directory", required=True)
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

    for sample in os.listdir(Path(args.c_dir, VIDEO)):
        base = os.path.splitext(sample)[0]
        audiobase = base + '00' + MXF
        audioclip = mp.AudioFileClip(str(Path(args.c_dir, AUDIO, audiobase)))
        clip = mp.VideoFileClip(str(Path(args.c_dir, VIDEO, sample)))
        clip = clip.resize(FRAME_SIZE)
        clip.audio = audioclip
        clip = clip.volumex(4)

        converted_file = str(Path(out_dir, base + MP4))
        clip.write_videofile(converted_file,
        codec='libx264', 
        audio_codec='aac', 
        remove_temp=True
        )      
         
if __name__ == "__main__":
    main()