import numpy as np
import cv2
from skimage.measure import regionprops


def DetectDiscsOnReversiBoard(Im, showPieceDetectionStages):
    # Detect Discs (both white and orange) on a given Reversi Board
    # The function uses thresholding on red channel for initial segmentation,
    # followed by binary erosion and dilation for noise removal and
    # analysis of the resulting connected components

    # Red channel thresholding
    I_red = Im[:, :, 0] > 200

    # Display
    if showPieceDetectionStages:
        cv2.imshow("Original Image", Im)
        cv2.imshow("Red Channel Thresholding", I_red.astype(np.uint8) * 255)

    # Perform binary erosion and dilation for noise removal
    s = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    newIm_red = cv2.erode(I_red.astype(np.uint8), s)
    newIm_red = cv2.dilate(newIm_red, s)

    # Analyze connected components
    props = regionprops(newIm_red.astype(int), coordinates='xy')
    Discs = []
    for prop in props:
        if 500 < prop.area < 1500 and prop.eccentricity < 0.5:
            Discs.append(prop)

    # Display final results
    if showPieceDetectionStages:
        cv2.imshow("Filtered Image", newIm_red.astype(np.uint8) * 255)
        for disc in Discs:
            center = disc.centroid
            radius = np.sqrt(disc.area / np.pi)
            cv2.circle(Im, (int(center[1]), int(center[0])), int(radius), (0, 255, 0), 2)
        cv2.imshow("Final Result", Im)

    return Discs

