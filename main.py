import cv2
import numpy as np

# Load image
image = cv2.imread('img.png')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Apply Hough transform to detect lines
lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

# # Filter and draw lines
# for rho, theta in lines[:, 0]:
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a * rho
#     y0 = b * rho
#     x1 = int(x0 + 1000 * (-b))
#     y1 = int(y0 + 1000 * (a))
#     x2 = int(x0 - 1000 * (-b))
#     y2 = int(y0 - 1000 * (a))
#     cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)


lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 170, minLineLength=100, maxLineGap=10)

for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow('Detected Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
