# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 13:26:36 2018

@author: Stuart Watt
"""
import numpy as np
import cv2

def select_train_images(image):
    starts, ends, ii = [], [], 0
    img_BGR = cv2.imread(image)
    cv2.namedWindow("image")
    clone = img_BGR.copy()
    
    def select_region(event, x, y, flags, params):
        nonlocal starts, ends, ii

        if event == cv2.EVENT_LBUTTONDOWN:
            starts.append((x, y))

        elif event == cv2.EVENT_LBUTTONUP:
            ends.append((x, y))

            cv2.rectangle(img_BGR, starts[ii], ends[ii], (0, 255, 0), 2)
            cv2.imshow("image", img_BGR)
            ii += 1
    
    cv2.setMouseCallback("image", select_region)

    
    # keep looping until the 'q' key is pressed
    while True:

        # display the image and wait for a keypress
        cv2.imshow("image", img_BGR)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the training regions
        if key == ord("r"):
            img_BGR = clone.copy()
            starts, ends, ii = [], [], 0   

        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break

    cv2.destroyAllWindows()
    
    plants = []
    
    # create BGR, HSV and LAB copies of the image. each pixel has 9 features
    img_BGR = clone
    img_HSV = cv2.cvtColor(clone, cv2.COLOR_BGR2HSV)
    img_LAB = cv2.cvtColor(clone, cv2.COLOR_BGR2LAB)

    # concatenate the 3 images to create the input data for the model.
    img_final = np.concatenate((img_BGR, img_HSV, img_LAB), axis=2)
    
    for start, end in zip(starts, ends):
        plants.append(img_final[start[1]:end[1], start[0]:end[0]])
        
    return(plants)


def prepare_train_data(image):
    print('Obtaining plant parts...')
    plant_img = select_train_images(image)
    
    for k in range(len(plant_img)):
        plant_img[k] = plant_img[k].reshape(-1, plant_img[k].shape[-1])

    train_plants = np.concatenate(plant_img, axis=0)
    train_plants = np.concatenate((train_plants, np.ones((len(train_plants), 1))), axis=1)
    
    print('Obtaining background parts...')
    back_img = select_train_images(image)
    
    for k in range(len(back_img)):
        back_img[k] = back_img[k].reshape(-1, back_img[k].shape[-1])

    train_back = np.concatenate(back_img, axis=0)
    train_back = np.concatenate((train_back, np.zeros((len(train_back), 1))), axis=1)
    
    train_set = np.concatenate((train_plants, train_back), axis=0)
    np.random.shuffle(train_set)
    
    return(train_set[:,:-1], train_set[:,-1])