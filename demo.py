#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import shutil
import torch
import cv2
import numpy as np
from src.loftr import LoFTR, default_cfg
from src.basnet import generate_mask 

TOP_N = 10
IMAGE_DIR = None
NB_CONF_VALUES = 25 #5
if "NB_CONF_VALUES" in os.environ:
    NB_CONF_VALUES = int(os.environ["NB_CONF_VALUES"])

def autocrop(img):

    row = np.squeeze(cv2.reduce(img,0,cv2.REDUCE_MAX))
    col = np.squeeze(cv2.reduce(img,1,cv2.REDUCE_MAX))
    cmin=None
    cmax=None
    rmin=None
    rmax=None
    for i in range(row.shape[0]):
        if not cmin and row[i]>0:
            cmin = i
        if row[i] > 0:
            cmax = i
    for i in range(col.shape[0]):
        if not rmin and col[i]>0:
            rmin = i
        if col[i] > 0:
            rmax = i

    return img[rmin:rmax,cmin:cmax]


def compute_matching_score(matcher, device, lst_img0, lst_img1,scoring='conf'):

    img0 = torch.from_numpy(lst_img0)[None][None].to(device) / 255.
    img1 = torch.from_numpy(lst_img1)[None][None].to(device) / 255.

    batch = {'image0': img0, 'image1': img1}
    with torch.no_grad():
        matcher(batch)
        mkpts0 = batch['mkpts0_f'].cpu().numpy()
        mkpts1 = batch['mkpts1_f'].cpu().numpy()
        mconf = batch['mconf'].cpu().numpy()
        mkpts0_filtered = []
        mkpts1_filtered = []
        mconf_filtered = []
        # filter out list
        img0_raw = lst_img0#img0.cpu().numpy()
        img1_raw = lst_img1#img1.cpu().numpy()
        for n in range(len(mkpts0)):
            pt0 = [int(mkpts0[n][0]), int(mkpts0[n][1])]
            pt1 = [int(mkpts1[n][0]), int(mkpts1[n][1])]
            block0 = img0_raw[pt0[1] - 3:pt0[1] + 4, pt0[0] - 3:pt0[0] + 4]
            block1 = img1_raw[pt1[1] - 3:pt1[1] + 4, pt1[0] - 3:pt1[0] + 4]
            if cv2.countNonZero(block0) == 49 and cv2.countNonZero(block1) == 49:
                mkpts0_filtered.append(pt0)
                mkpts1_filtered.append(pt1)
                mconf_filtered.append(mconf[n])

    sort_index = np.argsort(mconf_filtered)
    sort_index = sort_index[::-1]
    arr_mconf_filtered = np.array([mconf_filtered[i] for i in sort_index])
    #print(arr_mconf_filtered[0:5])
    if scoring == 'count':
        return  len(mconf_filtered)   # to compare with SIFT
    # scoring=='conf'
    return np.sum(arr_mconf_filtered[0:NB_CONF_VALUES])


parser = argparse.ArgumentParser(description='Performance of LoFTR for whale identification based on a key image')
parser.add_argument("input_file",  help="Input file used to do the matching")
parser.add_argument("--mask_filename", type=str,
                    help="Save intermediate binary mask using given filename")
args = parser.parse_args()

SIDE = "RSD"
SPECIES = "Bm"

IMAGE_DIR = os.path.join( SPECIES+"_"+SIDE)

dict_images = {}
dset_name = os.path.join("dset_"+SPECIES+"_"+SIDE+".txt")
print("Opening dataset "+dset_name)
with open(dset_name) as fm:
    for matchline in fm:
    #    if matchline[0]=='#':
    #        continue
        matchline = matchline.rstrip()
        whale = matchline.split('/')[0]
        fname=matchline.split('/')[1]

        img0_pth = os.path.join("/opt/"+IMAGE_DIR,fname)
        #print(img0_pth)
        img0_raw = cv2.imread(img0_pth, cv2.IMREAD_GRAYSCALE)
        if img0_raw is None:
            print("  Can't read image, skip")
            continue
        img0_raw = autocrop(img0_raw)

        img0_raw = cv2.resize(img0_raw, (720,192))#(img0_raw.shape[1]//8*8, img0_raw.shape[0]//8*8))  # input size shuold be divisible by 8
        if whale not in dict_images:
            dict_images[whale] = []
        dict_images[whale].append([fname, img0_raw])

    # Inference with LoFTR and get prediction
if len(dict_images)==0:
    print("Dataset file not found")
    exit(1)

print("{} candidates".format(len(dict_images)))
nb_top_n = 0
nb_top_1 = 0
nbqueries = 0
nbskip = 0

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

matcher = LoFTR(config=default_cfg)
matcher.load_state_dict(torch.load("models/outdoor_ds.ckpt", map_location=torch.device(device))['state_dict'])
matcher = matcher.eval().to(device)

# External code has its own dataloader: more convenient to keep the same interface (disk)
whaleimfname = os.path.abspath(args.input_file)
generate_mask([whaleimfname], "/tmp") 
whalemaskfname = "/tmp/query.png"
if args.mask_filename:
    shutil.copyfile(whalemaskfname, args.mask_filename)

mask = cv2.imread(whalemaskfname, cv2.IMREAD_GRAYSCALE)  # Read mask from disk
img0_raw = cv2.imread(whaleimfname, cv2.IMREAD_GRAYSCALE)
if img0_raw is None or mask is None:
     print("Can't read input image")
     exit(1)
print("after mask")
img0_raw = cv2.bitwise_and(img0_raw, img0_raw, mask=mask)
img0_raw = autocrop(img0_raw)
img0_raw = cv2.resize(img0_raw, (720,192)) # input size shuold be divisible by 8

matches = {} 
for whale in dict_images.keys():
      for j in range(len(dict_images[whale])):   # Possibly many image for a given whale
            matches[whale] =  compute_matching_score(matcher, device,img0_raw, dict_images[whale][j][1], 'conf')

matches = {k: v for k, v in sorted(matches.items(), key=lambda item: item[1])}
idxs=list(matches.keys())[-10:]

firsthit = True
for i in idxs[::-1]:
    msg = ""
    if firsthit:
       msg = "-> Most likely candidate"
       firsthit = False
    print("{}:{} {}".format(i,matches[i], msg))

