import cv2
import numpy as np

# Load image
image = cv2.imread('chess_24.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find chessboard corners
ret, corners = cv2.findChessboardCorners(gray, (7, 7), None)

# If corners are found, draw them
if ret == True:
    # Refine corners for better accuracy
    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))

    # Draw corners on the image
    cv2.drawChessboardCorners(image, (8, 8), corners, ret)

    # Show the image with corners
    cv2.imshow('Chessboard Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Chessboard not found in the image.")
