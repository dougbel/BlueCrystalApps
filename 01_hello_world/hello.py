import argparse
import logging
import os
import pandas as pd
import numpy as np
import cv2

from si.pipes.pipe import Pipe
from si.pipes.pipecalculatepropagator import PipeCalculatePropagator
from si.pipes.piperegistration import PipeRegistration
from si.pipes.pipesearchinvalidposes import PipeSearchInvalidPoses
from si.scannet.datascannet import DataScanNet
from si.pipes.pipepropagateonimg import PipePropagateOnImg



if __name__ == '__main__':
    img_scores_255 = np.zeros((800, 600), dtype=np.uint8)
    print("probando print")
    cv2.imwrite('/mnt/storage/home/csapo/projects/hello_world/scores_255.jpg', img_scores_255)
