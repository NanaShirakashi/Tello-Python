from __future__ import division

from PyTorch_YOLOv3.models import *
from PyTorch_YOLOv3.utils.utils import *
from PyTorch_YOLOv3.utils.datasets import *
from PyTorch_YOLOv3.utils.augmentations import *
from PyTorch_YOLOv3.utils.transforms import *

import os
import sys
import time
import datetime
import argparse
import numpy as np

from PIL import Image

import torch
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import NullLocator

import os
from glob import glob
import cv2

def TelloDetect(model):
    class_path = "./PyTorch-YOLOv3/data/coco.names"
    conf_thres = 0.8
    nms_thres = 0.4
    batch_size = 1
    n_cpu = 0
    img_size = 416
    image_folder = '/mnt/c/Users/nana/Tello-Python-master/Tete/img'

    dataloader = DataLoader(
        ImageFolder(image_folder, transform= \
            transforms.Compose([DEFAULT_TRANSFORMS, Resize(img_size)])),
        batch_size=batch_size,
        shuffle=False,
        num_workers=n_cpu,
    )

    classes = load_classes(class_path)  # Extracts class labels from file

    Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

    imgs = []  # Stores image paths
    img_detections = []  # Stores detections for each image index

    print("\nPerforming object detection:")
    prev_time = time.time()
    for batch_i, (img_paths, input_imgs) in enumerate(dataloader):
    # Configure input
    # print(input_img.shape)
        input_imgs = Variable(input_imgs.type(Tensor))


            # Get detections
        with torch.no_grad():
            detections = model(input_imgs)
            detections = non_max_suppression(detections, conf_thres, nms_thres)

            # Log progress
        current_time = time.time()
        inference_time = datetime.timedelta(seconds=current_time - prev_time)
        prev_time = current_time
        print("\t+Inference Time: %s" % inference_time)

        # Save image and detections
        imgs.extend(img_paths)
        img_detections.extend(detections)    

    # Bounding-box colors
    cmap = plt.get_cmap("tab20b")
    colors = [cmap(i) for i in np.linspace(0, 1, 20)]

    print("\nSaving images:")
    # Iterate through images and save plot of detections
    for img_i, (path, detections) in enumerate(zip(imgs, img_detections)):

        print("Image: '%s'" % path)

        # Create plot
        img = np.array(Image.open(path))

        # plt.figure()
        # fig, ax = plt.subplots(1)
        # ax.imshow(img)
        class_name=[]
        # Draw bounding boxes and labels of detections
        if detections is not None:
            # Rescale boxes to original image
            detections = rescale_boxes(detections, img_size, img.shape[:2])
            unique_labels = detections[:, -1].cpu().unique()
            n_cls_preds = len(unique_labels)
            bbox_colors = random.sample(colors, n_cls_preds)

            for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections:
                
                print("\t+ Label: %s, Conf: %.5f" % (classes[int(cls_pred)], cls_conf.item()))
                # box_w = x2 - x1
                # box_h = y2 - y1

                # color = bbox_colors[int(np.where(unique_labels == int(cls_pred))[0])]
                    # Create a Rectangle patch
                # bbox = patches.Rectangle((x1, y1), box_w, box_h, linewidth=2, edgecolor=color, facecolor="none")
                    # Add the bbox to the plot
                # ax.add_patch(bbox)
                #     # Add label
                # plt.text(
                #     x1,
                #     y1,
                #     s=classes[int(cls_pred)],
                #     color="white",
                #     verticalalignment="top",
                #     bbox={"color": color, "pad": 0},
                # )
                class_name.append(classes[int(cls_pred)])


            # Save generated image with detections
        # plt.axis("off")
        # plt.gca().xaxis.set_major_locator(NullLocator())
        # plt.gca().yaxis.set_major_locator(NullLocator())
        # filename = os.path.basename(path).split(".")[0]
        # output_path = os.path.join("./output", f"{filename}.png")
        # os.makedirs("./output" , exist_ok=True)
        # plt.savefig(output_path, bbox_inches="tight", pad_inches=0.0)
        # plt.close()

    return class_name

