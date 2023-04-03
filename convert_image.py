# -*- coding: utf-8 -*-

import os, sys
import shutil, argparse, pytz
from datetime import datetime
import openslide
import numpy as np
from skimage import io
import cv2
import PIL
from PIL import Image
PIL.Image.MAX_IMAGE_PIXELS = None

from utils import numpy2tiff

def set_args():
    parser = argparse.ArgumentParser(description = "Convert Image to Pyramidal TIFF")
    parser.add_argument("--data_root",         type=str,       default="/Data")
    parser.add_argument("--raw_img_dir",       type=str,       default="RawImages")
    parser.add_argument("--raw_img_suffix",    type=str,       default=".tif")
    parser.add_argument("--tiff_slide_dir",    type=str,       default="TiffSlides")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = set_args()

    # Raw image directory
    raw_img_dir = os.path.join(args.data_root, args.raw_img_dir)
    img_lst = sorted([os.path.splitext(ele)[0] for ele in os.listdir(raw_img_dir) if ele.endswith(args.raw_img_suffix)])
    # Tiff image directory
    tiff_slide_dir = os.path.join(args.data_root, args.tiff_slide_dir)
    if os.path.exists(tiff_slide_dir):
        shutil.rmtree(tiff_slide_dir)    
    os.makedirs(tiff_slide_dir)

    # convert images one-by-one
    for idx, cur_img_name in enumerate(img_lst):
        cur_time_str = datetime.now(pytz.timezone('America/Chicago')).strftime("%m/%d/%Y, %H:%M:%S")
        print("@ {} Convert {}/{} {}".format(cur_time_str, idx+1, len(img_lst), cur_img_name))
        # load slide
        raw_img_path = os.path.join(raw_img_dir, cur_img_name + args.raw_img_suffix)
        raw_img = cv2.imread(raw_img_path)
        raw_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
        # save to tif
        tif_slide_path = os.path.join(tiff_slide_dir, cur_img_name + ".tif")
        numpy2tiff(raw_img, tif_slide_path)
        # convert the tif to pyramid tiff
        tiff_slide_path = os.path.join(tiff_slide_dir, cur_img_name + ".tiff")
        conversion_cmd_str = " ".join(["vips", "im_vips2tiff", tif_slide_path, tiff_slide_path + ":jpeg:75,tile:256x256,pyramid"])
        os.system(conversion_cmd_str) 
        if os.path.exists(tif_slide_path):
            os.remove(tif_slide_path)
