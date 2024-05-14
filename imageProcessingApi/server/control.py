import cv2
import numpy as np

def load_image(image_path):
    return cv2.imread(image_path)


def save_image(image, image_path):
    cv2.imwrite(image_path, image)

def apply_blur (filename:str):
    return cv2.GaussianBlur(load_image(filename), (5, 5), 0)

def service_blur(filename:str):
    save_image(apply_blur(filename), filename)
    load_image(filename)