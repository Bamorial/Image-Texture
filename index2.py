import os

import cv2 as cv
import numpy as np

windowSize = 20
padding = 2

originImage = cv.imread("PATH_TO_YOUR_IMAGE")
orig_height, orig_width, _ = originImage.shape

newHeight = round(orig_height / windowSize)
newWidth = round(orig_width / windowSize)

originImage = cv.resize(
    originImage, (newWidth, newHeight), interpolation=cv.INTER_NEAREST_EXACT
)


def calculate_average_color(image):
    return np.mean(image.reshape(-1, 3), axis=0)


color_images = {}
folder_path = "PATH_TO_THE_TEXTURE_FOLDER"
for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        color_image = cv.imread(os.path.join(folder_path, filename))
        color_image = cv.resize(
            color_image, (windowSize, windowSize), interpolation=cv.INTER_NEAREST_EXACT
        )
        avg_color = calculate_average_color(color_image)
        color_images[filename] = (color_image, avg_color)

output_height = newHeight * windowSize
output_width = newWidth * windowSize

img = np.full((output_height, output_width, 3), 255, dtype="uint8")

for i in range(newHeight):
    for j in range(newWidth):
        current_color = originImage[i, j]

        closest_image = None
        min_distance = float("inf")
        for name, (color_image, avg_color) in color_images.items():
            distance = np.linalg.norm(current_color - avg_color)
            if distance < min_distance:
                min_distance = distance
                closest_image = color_image

        x, y = i * windowSize, j * windowSize
        img[x : x + windowSize, y : y + windowSize] = closest_image

cv.imshow("Display window", img)
cv.imwrite("output_image.png", img)
cv.waitKey(0)
cv.destroyAllWindows()
