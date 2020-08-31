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
    parser.add_argument('--vid-dir', type=str, help='Path to video directory.', required=True)
    parser.add_argument('--out-dir', type=str, default=None, help='Directory to save converted videos')
    args = parser.parse_args()

    if args.out_dir is None:

        if not os.path.exists(args.out_dir):
            os.makedirs(args.out_dir)

    vid_list = list()
    for (dirpath, dirnames, filenames) in os.walk(args.vid_dir):
        for file in filenames:
            vid_list += [os.path.join(dirpath, file) for file in filenames]
    vid_list = list(dict.fromkeys(vid_list))

    for sample in vid_list:
        try:
            base = os.path.basename(sample)
            converted_name = str(Path(args.out_dir, os.path.splitext(base)[0] + NEW_EXT))
            clip = mp.VideoFileClip(sample)
            clip = clip.resize(FRAME_SIZE)
            clip = clip.volumex(4)
            clip.write_videofile(converted_name, 
            codec='libx264', 
            audio_codec='aac', 
            remove_temp=True
            )
        except:
            print('Unable to process file: ' + str(sample))
            pass

if __name__ == "__main__":
    main()