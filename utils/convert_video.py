#!/usr/bin/env python3
'''Converts videos to formats acceptable my iMovie.'''

import argparse
import os
from pathlib import Path

import cv2
import moviepy.editor as mp

NEW_EXT = '.MP4'
FRAME_SIZE = (1920,1080)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vid-path', type=str, help='Path to video directory or file.', required=True)
    parser.add_argument('--out-dir', type=str, default='./', help='Directory to save converted videos')
    args = parser.parse_args()

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    
    vid_list = []
    if os.path.isfile(args.vid_path):
        vid_list.append(args.vid_path)
    else:
        vids = os.listdir(args.vid_path)
        vid_list = [Path(args.vid_path, vid) for vid in vids]

    for vid in vid_list:
        try:
            base = os.path.splitext(str(os.path.basename(vid)))[0]
            converted_name = str(Path(args.out_dir, base + NEW_EXT))
            clip = mp.VideoFileClip(str(vid))
            clip = clip.resize(FRAME_SIZE)
            clip = clip.volumex(4)
            clip.write_videofile(converted_name, 
            codec='libx264', 
            audio_codec='aac', 
            remove_temp=True
            )
        except:
            print('Unable to process file: ' + str(vid))
            pass

if __name__ == "__main__":
    main()