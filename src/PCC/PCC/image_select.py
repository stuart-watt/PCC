# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 13:26:36 2018

@author: Stuart Watt
"""

import time

import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier


def select_train_images(image):
    """
    User interface for selecting training data from image.

    Click, drag and release to draw a rectangle over desired training area.
    Select as many samples as you want.
    Press 'c' to finish selection.
    Press 'r' to refresh image and select again.

    Returns a list of selected samples from the image
    """

    starts, ends, ii = [], [], 0
    img_BGR = cv2.imread(image)
    clone = img_BGR.copy()

    # Resize the image to fit the screen before training segment selection.
    # Resize so height is 1000 pixels.
    # Save the original dimensions for conversion back to original resolution.
    scale_factor = img_BGR.shape[0] / 700
    img_BGR = cv2.resize(img_BGR, (0, 0), fx=1 / scale_factor, fy=1 / scale_factor)
    cv2.namedWindow("image")

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

    # Scale back the rectangles to match the original image.
    starts = [(int(scale_factor * x), int(scale_factor * y)) for x, y in starts]
    ends = [(int(scale_factor * x), int(scale_factor * y)) for x, y in ends]

    # create BGR, HSV and LAB copies of the image. each pixel has 9 features
    img_BGR = clone
    img_HSV = cv2.cvtColor(clone, cv2.COLOR_BGR2HSV)
    img_LAB = cv2.cvtColor(clone, cv2.COLOR_BGR2LAB)

    # concatenate the 3 images to create the input data for the model.
    img_final = np.concatenate((img_BGR, img_HSV, img_LAB), axis=2)

    for start, end in zip(starts, ends):
        plants.append(img_final[start[1] : end[1], start[0] : end[0]])

    return plants


def get_training(image):
    """
    Select first the plant images, then the background images.
    Returns flattened array of pixels for each class (plant or background).
    Each pixel has 9 features.
    """
    if image is not None:
        print("Obtaining plant parts...")
        plant_img = select_train_images(image)

        for k in range(len(plant_img)):
            plant_img[k] = plant_img[k].reshape(-1, plant_img[k].shape[-1])

        train_plants = np.concatenate(plant_img, axis=0)

        print("Obtaining background parts...")
        back_img = select_train_images(image)

        for k in range(len(back_img)):
            back_img[k] = back_img[k].reshape(-1, back_img[k].shape[-1])

        train_back = np.concatenate(back_img, axis=0)

        return (train_plants, train_back)

    else:
        raise ValueError("No file passed")


def prepare_training(train_p, train_b):
    """
    Function for assigning classification values (0 - background, 1 - plant)
    to the pixels. The arrays are then merged and randomly shuffled.

    Returns randomised training features and training classes as arrays.
    """

    train_p = np.concatenate((train_p, np.ones((len(train_p), 1))), axis=1)
    train_b = np.concatenate((train_b, np.zeros((len(train_b), 1))), axis=1)

    train_set = np.concatenate((train_p, train_b), axis=0)
    np.random.shuffle(train_set)
    return (train_set[:, :-1], train_set[:, -1])


def train_plants(file):
    """
    Function for obtaining training data and
    training a classifier on training data.
    The classifier is a Random Forrest classifier.
    n_estimators=100
    """

    plant, back = get_training(file)
    X_train, y_train = prepare_training(plant, back)

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)

    return clf


def remove_back(image, classifier):
    """
    Perform background removal on image.
    image is passed into the trained classifier and each pixel is classified.
    Returns and displays image free of background
    """

    start = time.perf_counter()

    img_BGR = cv2.imread(image)
    img_HSV = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2HSV)
    img_LAB = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2LAB)
    img_final = np.concatenate((img_BGR, img_HSV, img_LAB), axis=2).reshape((-1, 9))

    test_pred = classifier.predict(img_final)
    test_pred = test_pred.reshape((len(test_pred), 1))
    test_pred = np.concatenate((test_pred, test_pred, test_pred), axis=1).reshape(
        (img_BGR.shape[0], img_BGR.shape[1], 3)
    )

    new_image = np.multiply(img_BGR, test_pred).astype(np.uint8)

    end = time.perf_counter()
    print(end - start)

    # cv2.imshow('trained image', new_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return new_image
