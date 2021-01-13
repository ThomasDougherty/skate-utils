import argparse
import os
from pathlib import Path
import time

import moviepy.editor as mpe
import moviepy.video as mpv
FRAME_SIZE = (1920,1080)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--c-dir', type=str, default = './FISHEYE/', help="Path to 'CONTENTS' directory")
    parser.add_argument('--out-dir', type=str, default = None, help="Directory to save converted videos. If left 'None' then new output folder is generated instead.")
    parser.add_argument('--time-base', type=bool, default = False, help="If set 'True' with 'out-dir' argument, base folder given name with timestamp.")    
    args = parser.parse_args()

    t = time.localtime()
    if args.out_dir is None:
        out_dir = 'converted_fisheye_' + time.strftime('%m%d%Y_%H%M%S', t)
    else:
        if args.time_base:
            out_dir = Path(args.out_dir, time.strftime('%m%d%Y_%H%M%S', t))

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    num_vids = str(len(os.listdir(args.c_dir)))
    vid_list = os.listdir(args.c_dir)
    for cnt, sample in enumerate(vid_list):
        print("Video " + str(cnt) + " of " + num_vids)
        clip = mpe.VideoFileClip(str(Path(args.c_dir,sample)))
        clip = mpv.fx.all.crop(clip, x1=100, width=1720)
        clip = clip.resize(FRAME_SIZE)
        save_file = str(Path(out_dir,sample))
        clip.write_videofile(save_file,
                codec='libx264', 
                audio_codec='aac', 
                remove_temp=True
                )    
        os.remove(Path(args.c_dir,sample))

if __name__ == "__main__":
    main()