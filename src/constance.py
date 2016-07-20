# All importations go here
import cv2
import numpy as np
from threading import Thread
import time

# All global constants go here

MAX_PIXEL_VAL = 255

ALL_CONTOURS = -1

H_MAX = 179
S_MAX = 255
V_MAX = 255

TOLERANCE = 0.40

GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CONTOURS_THICKNESS = 3

K_SIZE = (5, 5)

MIN_VAL = 0
MAX_VAL = 255

MIN_TOLERANCE = 0
MAX_TOLERANCE = 100
