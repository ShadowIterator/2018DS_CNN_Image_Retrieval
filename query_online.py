# -*- coding: utf-8 -*-
# Author: yongyuan.name
from extract_cnn_vgg16_keras import VGGNet

import os
import numpy as np
import h5py

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse


f = open("result.txt", "w")


def get_imlist(path):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]


def query(path):
    # read and show query image
    queryDir = path
    # queryImg = mpimg.imread(queryDir)
    # plt.title("Query Image")
    # plt.imshow(queryImg)
    # plt.show()

    # init VGGNet16 model
    model = VGGNet()

    # extract query image's feature, compute simlarity score and sort
    queryVec = model.extract_feat(queryDir)
    scores = np.dot(queryVec, feats.T)
    rank_ID = np.argsort(scores)[::-1]
    # rank_score = scores[rank_ID]
    # print rank_ID
    # print rank_score

    # number of top retrieved images to show
    maxres = 10
    imlist = [imgNames[index] for i, index in enumerate(rank_ID[0:maxres])]
    # print "top %d images in order are: " % maxres, imlist
    print >> f, path,imlist

ap = argparse.ArgumentParser()
ap.add_argument("-query", required = True,
	help = "Path to query which contains image to be queried")
ap.add_argument("-index", required = True,
	help = "Path to index")
ap.add_argument("-result", required = True,
	help = "Path for output retrieved images")
args = vars(ap.parse_args())

# read in indexed images' feature vectors and corresponding image names
h5f = h5py.File(args["index"],'r')
feats = h5f['dataset_1'][:]
imgNames = h5f['dataset_2'][:]
h5f.close()
        
print "--------------------------------------------------"
print "               searching starts"
print "--------------------------------------------------"

query_list = get_imlist("ir")
for qimg in query_list:
    query(qimg)

# show top #maxres retrieved result one by one
# for i,im in enumerate(imlist):
#     image = mpimg.imread(args["result"]+"/"+im)
#     plt.title("search output %d" %(i+1))
#     plt.imshow(image)
#     plt.show()
