import cv2
import numpy as np

# Load the image
image = cv2.imread('img4.jpg')

# Convert the image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the range of blue color in HSV
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

# Create a mask using the defined range
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on the original image
contour_image = image.copy()
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

# Create a mask for the area outside the contours
outer_mask = np.ones_like(mask) * 255
cv2.drawContours(outer_mask, contours, -1, 0, cv2.FILLED)

# Fill the area outside the contours with blue in the original image
original_image = image.copy()
original_image[np.where(outer_mask == 255)] = [255, 0, 0]  # Blue color

# Display the result
cv2.imshow('Original Image with Contours and Outside Blue', original_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Convert the image to HSV color space
hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

# Define the range of blue color in HSV
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

# Create a mask using the defined range
mask = cv2.inRange(hsv, lower_blue, upper_blue)



mask = cv2.bitwise_not(mask)



# Define lower and upper bounds for blue color in HSV
blue_lower = np.array([100, 50, 50])  # Adjust these values as per your blue color range
blue_upper = np.array([140, 255, 255])

# Convert the image to HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Create a mask for blue pixels
blue_mask = cv2.inRange(hsv_image, blue_lower, blue_upper)

# Initialize a mask for pixels inside contour but not blue
non_blue_mask = np.zeros_like(mask)


# Perform dilation on the mask
kernel = np.ones((5,5),np.uint8)
dilated_mask = cv2.dilate(mask, kernel, iterations=1)

# Perform erosion on the mask
eroded_mask = cv2.erode(mask, kernel, iterations=1)

mask_resized = cv2.resize(mask, (100, 100))
dilated_mask_resized = cv2.resize(dilated_mask, (100, 100))
eroded_mask_resized = cv2.resize(eroded_mask, (100, 100))
# Display the dilated and eroded masks
cv2.imshow('Mask', mask)

cv2.imshow('Dilated Mask', dilated_mask)
cv2.imshow('Eroded Mask', eroded_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Display the original image with contours
cv2.imshow('Original Image with Contours', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Find the bounding box of the segmented region
x, y, w, h = cv2.boundingRect(eroded_mask)

# Crop the segmented region from the original image
segmented_region = eroded_mask[y:y+h, x:x+w]



# Display the cropped segmented region
cv2.imshow("Segmented Region", segmented_region)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Threshold the image to get binary representation
_, binary_image = cv2.threshold(segmented_region, 127, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through contours to find centers
centers = []
radii = []

for contour in contours:
    # Find the moments of the contour
    M = cv2.moments(contour)
    # Calculate centroid
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centers.append((cX, cY))
        area = cv2.contourArea(contour)
        radius = np.sqrt(area / np.pi)
        radii.append(radius)

median_radius = np.median(radii)
# Define a threshold as a multiple of MAD
# Remove outliers beyond the threshold
filtered_indices = [i for i, r in enumerate(radii) if abs(r - median_radius) < median_radius * 0.3]
centers = [centers[i] for i in filtered_indices]
radii = [radii[i] for i in filtered_indices]


# Draw circles on the original image for visualization
output_image = cv2.cvtColor(segmented_region, cv2.COLOR_GRAY2BGR)
for center, radius in zip(centers, radii):
    cv2.circle(output_image, center, 3, (0, 255, 0), -1)
    cv2.putText(output_image, f'Radius: {radius:.2f}', (center[0] - 50, center[1] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

min_x = min(point[0] for point in centers)
max_x = max(point[0] for point in centers)
min_y = min(point[1] for point in centers)
max_y = max(point[1] for point in centers)

def perform_homography(image, src_points):
    # Define the destination points (corners of a rectangle)
    dst_points = np.array([[0, 0], [0, image.shape[0] - 1], [image.shape[1] - 1, 0], [image.shape[1] - 1, image.shape[0] - 1]], dtype=np.float32)

    # Calculate the homography matrix
    homography_matrix, _ = cv2.findHomography(src_points, dst_points)

    # Apply the homography transformation
    transformed_image = cv2.warpPerspective(image, homography_matrix, (image.shape[1], image.shape[0]))

    return transformed_image

def find_coordinate_for_given_x(coordinates, given_x):
    for x, y in coordinates:
        if x == given_x:
            return x, y
    return None

def find_coordinate_for_given_y(coordinates, given_y):
    for x, y in coordinates:
        if y == given_y:
            return x, y
    return None

transformed_image = perform_homography(image, [find_coordinate_for_given_x(centers, min_x), find_coordinate_for_given_x(centers, max_x), find_coordinate_for_given_y(centers, min_y), find_coordinate_for_given_y(centers, max_y)])

# Display the result

# rows = 6
# cols = 7

# # Calculate the spacing for the grid lines
# height, width, _ = output_image.shape
# row_spacing = height // rows
# col_spacing = width // cols
#
# # Draw horizontal lines
# for i in range(1, rows):
#     cv2.line(output_image, (0, i * row_spacing), (width, i * row_spacing), (0, 255, 0), 2)
#
# # Draw vertical lines
# for j in range(1, cols):
#     cv2.line(output_image, (j * col_spacing, 0), (j * col_spacing, height), (0, 255, 0), 2)




cv2.imshow("Result", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Create a mask for the blue area
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Invert the blue mask
inv_blue_mask = cv2.bitwise_not(blue_mask)
# masked_non_blue_in_blue_region = cv2.bitwise_and(non_blue_in_blue_region_mask, contour_mask)

# Bitwise AND the inverted blue mask with the original mask

# Display the mask of everything that is not blue but only what is inside the blue area
cv2.imshow("Non-Blue Inside Blue Area", inv_blue_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

# import cv2
# import numpy as np
#
# # Load the image
# image = cv2.imread('img.png')
#
# # Convert the image to HSV color space
# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#
# # Define the range of blue color in HSV
# lower_blue = np.array([100, 50, 50])
# upper_blue = np.array([130, 255, 255])
#
# # Create a mask using the defined range
# mask = cv2.inRange(hsv, lower_blue, upper_blue)
#
# # Find contours in the mask
# contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
# # Get the largest contour
# largest_contour = max(contours, key=cv2.contourArea)
#
# # Get the bounding box of the largest contour
# x, y, w, h = cv2.boundingRect(largest_contour)
#
# # Get the four corner points of the bounding box
# pts_src = np.array([[x, y], [x+w, y], [x+w, y+h], [x, y+h]], dtype=np.float32)
#
# # Define the destination points for homography (400x400)
# pts_dst = np.array([[0, 0], [400, 0], [400, 400], [0, 400]], dtype=np.float32)
#
# # Calculate the homography matrix
# M = cv2.getPerspectiveTransform(pts_src, pts_dst)
#
# # Apply the homography
# warped_image = cv2.warpPerspective(image, M, (400, 400))
#
# # Display the warped image
# cv2.imshow('Warped Image', warped_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
