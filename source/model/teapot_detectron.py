import torch, torchvision

print(torch.__version__, torch.cuda.is_available())
assert torch.__version__.startswith("1.9")

import detectron2
from detectron2.utils.logger import setup_logger

setup_logger()

import numpy as np
# import os, json, cv2, random

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog


class TeapotDetectron(object):
    def __init__(self, model_path="../source/ext/model_final.pth"):
        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
        self.cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 1
        self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
        self.cfg.MODEL.WEIGHTS = model_path

        self.predictor = DefaultPredictor(self.cfg)

    def predict(self, im):
        with torch.no_grad():
            outputs = self.predictor(im)
            outputs = outputs['instances'].get_fields()
            return outputs['scores'].to("cpu") >= 0.7

    def get_points(self, im, bs=1):
        with torch.no_grad():
            outputs = self.predictor(im)
            if bs == 1:
                print("Pred scores", outputs['instances'].get_fields()['scores'])
                mask = outputs['instances'].get_fields()['pred_masks'][0].to('cpu')
                print("Mask and im shape", mask.shape, im.shape)
                mask = mask.reshape([mask.shape[1], mask.shape[2]]).unsqueeze(2)
                print("Mask and im shape", mask.shape, im.shape)
                return torch.cat([torch.tensor(im), mask], axis=2)
            else:
                mask = outputs['instances'].get_fields()['pred_masks'][0].to('cpu')
                mask = mask.reshape([bs, mask.shape[0], mask.shape[1], 1])
                return torch.cat([torch.tensor(im), mask], axis=3)
