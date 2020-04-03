from keras.preprocessing.image import ImageDataGenerator
import cv2
import numpy as np
import math
import argparse
from screeninfo import get_monitors
import os
import random

# Get desktop height
desk_height = get_monitors ()[0].height

# Set input args
ap = argparse.ArgumentParser ()
ap.add_argument ("-c", "--count", type = int, required = True,
	help = "count of images for augmentation")
ap.add_argument ("-i", "--input", type = str, required = True,
	help = "directory to the input images")
ap.add_argument ("-o", "--output", type = str, required = False,
	help = "directory for the output images (if no set use input)")
ap.add_argument ("-a", "--action", type = str, required = True,
	choices=['show', 'save'],
	help = "show or save images")
args = vars (ap.parse_args () )

###################################################
# PARAMETERS
###################################################

ROTATION_RANGE = 20
WIDTH_SHIFT_RANGE = (-10, 10)
HEIGHT_SHIFT_RANGE = (-10, 10)
BRIGHTNESS_RANGE = (0.5, 1.5)
SHEAR_RANGE = 10
ZOOM_RANGE = (0.8, 1.2)
FILL_MODE = 'nearest'
HORIZONTAL_FLIP = True
VERTICAL_FLIP = False

###################################################

# Args parse
# Count of images
count = args["count"]
# Input directory
input = args["input"]
# Output directory
output = args["output"]
if output:
	if not os.path.exists(output):
		os.makedirs(output)
else:
	output = input
# Action (show or save)
action = args["action"]

# Calculate the number of columns
count_columns = int (math.ceil (math.sqrt (count) ) )
# Calculate the number of rows
count_rows = math.ceil (count / count_columns)

# Read only images in directory
def read_images_in_dir (path):
	images = []
	valid_images = [".jpg", ".jpeg", ".png"]
	for f in os.listdir (path):
		ext = os.path.splitext (f)[1]
		if ext.lower () in valid_images:
			images.append (os.path.join (path,f))

	return images

# Preview augmented images
def show (data_generator):

	# Read only images in directory
	images_path = read_images_in_dir (input)

	# Read random image
	image = cv2.imread (random.choice(images_path))

	# Reshape images to (1, height, width, channels)
	images = image.reshape (1, image.shape[0], image.shape[1], image.shape[2])

	# Get images from generator
	data_generator.fit (images)
	image_iterator = data_generator.flow (images)

	# Make empty image for vertical images
	image_y = np.full ( (1, image.shape[1] * count_columns + 1, 3), 255, "uint8")
	# Make white image
	image_white = np.full ( (image.shape[0], image.shape[1] , 3), 255, "uint8")

	loop = 0
	# Loop rows
	for i in range (count_rows):
		# Make empty image for horizontal images
		image_x = np.full ( (image.shape[0], 1 , 3), 255, "uint8")

		# Loop columns
		for x in range (count_columns):
			# If loop > count - draw white images
			if loop < count:
				image_aug = image_iterator.next ()[0].astype ('uint8')
			else:
				image_aug = image_white

			# Concate images in row
			image_x = np.concatenate ( (image_x, image_aug), axis=1)
			loop += 1

		# Concate rows
		image_y = np.concatenate ( (image_y, image_x), axis=0)

	# Calculate ratio deskop height / final image
	desk_ratio = image_y.shape[0] / desk_height

	# Show preview
	window_name = "Preview window"
	image_y = cv2.resize (image_y, (int (image_y.shape[1] / desk_ratio) - 150, int (image_y.shape[0] / desk_ratio) - 150 ) )
	cv2.imshow (window_name, image_y)
	cv2.moveWindow (window_name ,0 ,0)
	cv2.waitKey ()

# Save augmented images
def save (data_generator):

	# Read only images in directory
	images_path = read_images_in_dir (input)

	for image_name in images_path:
		# Read image
		image = cv2.imread (image_name)
		# Reshape images to (1, height, width, channels)
		images = image.reshape (1, image.shape[0], image.shape[1], image.shape[2])

		# Get images from generator
		data_generator.fit (images)
		image_iterator = data_generator.flow (images)
		for i in range (count):
			image_aug = image_iterator.next ()[0].astype ('uint8')
			# ~ file_name = os.path.basename (image_name)[0] + '_' + str (i) + os.path.splitext (image_name)[1]
			file_name = (os.path.join(output,
				os.path.splitext (os.path.basename(image_name))[0]
				+ "_" + str(i)
				+ os.path.splitext (os.path.basename(image_name))[1])
			)
			print (file_name)
			cv2.imwrite (file_name, image_aug)

# Set transformation
data_generator = ImageDataGenerator (
	rotation_range = ROTATION_RANGE,
	width_shift_range = WIDTH_SHIFT_RANGE,
	height_shift_range = HEIGHT_SHIFT_RANGE,
	brightness_range = BRIGHTNESS_RANGE,
	shear_range = SHEAR_RANGE,
	zoom_range = ZOOM_RANGE,
	fill_mode = FILL_MODE,
	horizontal_flip = HORIZONTAL_FLIP,
	vertical_flip = VERTICAL_FLIP
)

# Show augmented preview
if action == "show":
	show (data_generator)
# Save augmented images
elif action == "save":
    save (data_generator)
