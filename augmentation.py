import os
import cv2
import random
import numpy as np
from PIL import Image

# Define the folder path for input images and output folder
input_folder = 'C:/Users/python/Desktop/CNN/dataset/Testing/no_tumor'
output_folder = 'C:/Users/python/Desktop/CNN/dataset/Testing/no_tumor'

# Define augmentation functions
def rotate(image, angle):
    rows, cols = image.shape[:2]
    M = cv2.getRotationMatrix2D((cols/2,rows/2), angle, 1)
    return cv2.warpAffine(image, M, (cols,rows))

def flip(image, axis):
    return cv2.flip(image, axis)

def zoom(image, scale):
    rows, cols = image.shape[:2]
    M = cv2.getRotationMatrix2D((cols/2,rows/2), 0, scale)
    return cv2.warpAffine(image, M, (cols,rows))

# Define list of augmentation functions
augmentations = [rotate, flip, zoom]

# Loop over all files in the input folder
for filename in os.listdir(input_folder):
    # Load image and convert to grayscale
    image_path = os.path.join(input_folder, filename)
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply random augmentation functions multiple times
    for i in range(5): # apply 5 sets of random augmentations
        augmented_image = gray.copy()
        for j in range(3): # apply three random augmentations per set
            fn = random.choice(augmentations)
            if fn == rotate:
                angle = random.randint(0, 360)
                augmented_image = fn(augmented_image, angle)
            elif fn == flip:
                axis = random.randint(-1, 1)
                augmented_image = fn(augmented_image, axis)
            else:
                scale = random.uniform(0.9, 1.1)
                augmented_image = fn(augmented_image, scale)

        # Save augmented image in output folder
        new_filename = filename.split('.')[0] + f'_aug_{i+1}.jpg'
        new_path = os.path.join(output_folder, new_filename)
        cv2.imwrite(new_path, augmented_image)
