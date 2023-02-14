# -*- coding: utf-8 -*-

import os, sys
import shutil, argparse, pytz
from datetime import datetime
import openslide
import numpy as np
from skimage import io
import PIL
from PIL import Image
PIL.Image.MAX_IMAGE_PIXELS = 933120000

from utils import numpy2tiff


def set_args():
    parser = argparse.ArgumentParser(description = "Convert WSI to Pyramidal TIFF")
    parser.add_argument("--data_root",         type=str,       default="/Data")
    parser.add_argument("--raw_slide_dir",     type=str,       default="RawSlides")
    parser.add_argument("--raw_slide_suffix",  type=str,       default=".svs")
    parser.add_argument("--tiff_slide_dir",    type=str,       default="TiffSlides")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = set_args()

    # Raw slide directory
    raw_slide_dir = os.path.join(args.data_root, args.raw_slide_dir)
    slide_lst = sorted([os.path.splitext(ele)[0] for ele in os.listdir(raw_slide_dir) if ele.endswith(args.raw_slide_suffix)])
    # Tiff slide directory
    tiff_slide_dir = os.path.join(args.data_root, args.tiff_slide_dir)
    if os.path.exists(tiff_slide_dir):
        shutil.rmtree(tiff_slide_dir)    
    os.makedirs(tiff_slide_dir)

    # covnert slides one-by-one
    for idx, cur_slide_name in enumerate(slide_lst):
        cur_time_str = datetime.now(pytz.timezone('America/Chicago')).strftime("%m/%d/%Y, %H:%M:%S")
        print("@ {} Norm {}/{} {}".format(cur_time_str, idx+1, len(slide_lst), cur_slide_name))
        # load slide
        raw_slide_path = os.path.join(raw_slide_dir, cur_slide_name + args.raw_slide_suffix)
        slide_head = openslide.OpenSlide(raw_slide_path)
        slide_w, slide_h = slide_head.dimensions
        wsi_img = slide_head.read_region(location=(0, 0), level=0, size=(slide_w, slide_h))
        wsi_img = np.asarray(wsi_img)[:, :, :3]
        # save to tif
        tif_img_path = os.path.join(tiff_slide_dir, cur_slide_name + ".tif")
        numpy2tiff(wsi_img, tif_img_path)
        # convert the tif to pyramid tiff
        tiff_slide_path = os.path.join(tiff_slide_dir, cur_slide_name + ".tiff")
        conversion_cmd_str = " ".join(["vips", "im_vips2tiff", tif_img_path, tiff_slide_path + ":jpeg:75,tile:256x256,pyramid"])
        os.system(conversion_cmd_str) 
        if os.path.exists(tif_img_path):
            os.remove(tif_img_path)