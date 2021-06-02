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


# class TelloDetect:
#     def __init__(self):
#         weights_path = "./PyTorch-YOLOv3/weights/yolov3.weights"
#         class_path = "./PyTorch-YOLOv3/data/coco.names"
#         conf_thres = 0.8
#         nms_thres = 0.4
#         batch_size = 1
#         n_cpu = 0
#         img_size = 416


def TelloDetect(input_img, img_path,model):
    weights_path = "./PyTorch-YOLOv3/weights/yolov3.weights"
    class_path = "./PyTorch-YOLOv3/data/coco.names"
    conf_thres = 0.8
    nms_thres = 0.4
    batch_size = 1
    n_cpu = 0
    img_size = 416
    model_def = './PyTorch-YOLOv3/config/yolov3.cfg'
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--image_folder", type=str, default="./imgs", help="path to dataset")
    # parser.add_argument("--model_def", type=str, default="./PyTorch-YOLOv3/config/yolov3.cfg", help="path to model definition file")
    # parser.add_argument("--weights_path", type=str, default="./PyTorch-YOLOv3/weights/yolov3.weights", help="path to weights file")
    # parser.add_argument("--class_path", type=str, default="./PyTorch-YOLOv3/data/coco.names", help="path to class label file")
    # parser.add_argument("--conf_thres", type=float, default=0.8, help="object confidence threshold")
    # parser.add_argument("--nms_thres", type=float, default=0.4, help="iou thresshold for non-maximum suppression")
    # parser.add_argument("--batch_size", type=int, default=1, help="size of the batches")
    # parser.add_argument("--n_cpu", type=int, default=0, help="number of cpu threads to use during batch generation")
    # parser.add_argument("--img_size", type=int, default=416, help="size of each image dimension")
    # parser.add_argument("--checkpoint_model", type=str, help="path to checkpoint model")
    # self = parser.parse_args()
    # print(self)

    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    os.makedirs("output", exist_ok=True)

    # # Set up model
    # model = Darknet(model_def, img_size=img_size).to(device)

    # if weights_path.endswith(".weights"):
    #     # Load darknet weights
    #     model.load_darknet_weights(weights_path)
    # else:
    #     # Load checkpoint weights
    #     model.load_state_dict(torch.load(weights_path))

    # model.eval()  # Set in evaluation mode

    # dataloader = DataLoader(
    #     ImageFolder(image_folder, transform= \
    #         transforms.Compose([DEFAULT_TRANSFORMS, Resize(img_size)])),
    #     batch_size=batch_size,
    #     shuffle=False,
    #     num_workers=n_cpu,
    # )

    classes = load_classes(class_path)  # Extracts class labels from file

    Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

    imgs = []  # Stores image paths
    img_detections = []  # Stores detections for each image index

    print("\nPerforming object detection:")
    prev_time = time.time()
    # for batch_i, (img_path, input_img) in enumerate(dataloader):
    # Configure input
    # print(input_img.shape)
    input_img = Variable(input_img.type(Tensor))


        # Get detections
    with torch.no_grad():
        detections = model(input_img)
        detections = non_max_suppression(detections, conf_thres, nms_thres)

        # Log progress
    current_time = time.time()
    inference_time = datetime.timedelta(seconds=current_time - prev_time)
    prev_time = current_time
    print("\t+Inference Time: %s" % inference_time)

    # Save image and detections
    # imgs.extend(img_path)
    # img_detections.extend(detections)    

    # Bounding-box colors
    cmap = plt.get_cmap("tab20b")
    colors = [cmap(i) for i in np.linspace(0, 1, 20)]

    print("\nSaving images:")
    # Iterate through images and save plot of detections
    # for img_i, (path, detections) in enumerate(zip(imgs, img_detections)):

    print("Image: '%s'" % img_path)

        # Create plot
    img = np.array(Image.open(img_path))

    # plt.figure()
    # fig, ax = plt.subplots(1)
    # ax.imshow(img)

        # Draw bounding boxes and labels of detections
    if detections is not None:
        # Rescale boxes to original image
        detections = rescale_boxes(detections, img_size, img.shape[:2])
        unique_labels = detections[:, -1].cpu().unique()
        n_cls_preds = len(unique_labels)
        # bbox_colors = random.sample(colors, n_cls_preds)
        for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections:

            print("\t+ Label: %s, Conf: %.5f" % (classes[int(cls_pred)], cls_conf.item()))
            # box_w = x2 - x1
            # box_h = y2 - y1

            # color = bbox_colors[int(np.where(unique_labels == int(cls_pred))[0])]
                # Create a Rectangle patch
            # bbox = patches.Rectangle((x1, y1), box_w, box_h, linewidth=2, edgecolor=color, facecolor="none")
                # Add the bbox to the plot
            # ax.add_patch(bbox)
                # Add label
            # plt.text(
            #     x1,
            #     y1,
            #     s=classes[int(cls_pred)],
            #     color="white",
            #     verticalalignment="top",
            #     bbox={"color": color, "pad": 0},
            # )

        # Save generated image with detections
    # plt.axis("off")
    # plt.gca().xaxis.set_major_locator(NullLocator())
    # plt.gca().yaxis.set_major_locator(NullLocator())
    # filename = os.path.basename(img_path).split(".")[0]
    # output_path = os.path.join("./output", f"{filename}.png")
    # os.makedirs("./output" , exist_ok=True)
    # plt.savefig(output_path, bbox_inches="tight", pad_inches=0.0)
    # plt.close()
    
    
    return classes[int(cls_pred)]


# if __name__ == "__main__":
    # target = os.path.join('./img', "*")
    # files = [(f, os.path.getmtime(f)) for f in glob(target)]
    # img_path = sorted(files, key=lambda files: files[1])[-1]
    # img_path = img_path[0]
    # input_img = cv2.imread(img_path)

#     TelloDetect(input_img, img_path)
