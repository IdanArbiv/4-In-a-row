import numpy as np
import cv2


def FindGreenBoard(Im, showResults):
    if showResults:
        cv2.imshow('Red Channel', Im[:, :, 0])
        cv2.imshow('Green Channel', Im[:, :, 1])
        cv2.imshow('Blue Channel', Im[:, :, 2])
        cv2.imshow('Grayscale', cv2.cvtColor(Im, cv2.COLOR_RGB2GRAY))

    redMask = Im[:, :, 0] < 80
    greenMask = Im[:, :, 1] > 80
    blueMask = Im[:, :, 2] < 80
    grayMask = cv2.cvtColor(Im, cv2.COLOR_RGB2GRAY) < 150

    if showResults:
        cv2.imshow('Red Mask', redMask.astype(np.uint8) * 255)
        cv2.imshow('Green Mask', greenMask.astype(np.uint8) * 255)
        cv2.imshow('Blue Mask', blueMask.astype(np.uint8) * 255)
        cv2.imshow('Gray Mask', grayMask.astype(np.uint8) * 255)

    BW = (redMask + greenMask + blueMask + grayMask) > 3

    if showResults:
        cv2.imshow('Combined Mask', BW.astype(np.uint8) * 255)

    kernel = np.ones((20, 20), np.uint8)
    BW = cv2.dilate(BW.astype(np.uint8), kernel)
    BW = cv2.erode(BW, kernel)

    if showResults:
        cv2.imshow('Processed Mask', BW.astype(np.uint8) * 255)

    num_labels, labels = cv2.connectedComponents(BW)
    unique, counts = np.unique(labels, return_counts=True)
    largest_component = np.argmax(counts[1:]) + 1
    res = np.argwhere(labels == largest_component)

    return res

