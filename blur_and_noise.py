import cv2
import numpy as np
from skimage import io
from skimage.transform import rotate, AffineTransform, warp
import matplotlib.pyplot as plt
import random
from skimage import img_as_ubyte
import os
from skimage.util import random_noise
from screeninfo import get_monitors
import argparse

# Get desktop height
desk_width = get_monitors ()[0].width

# Set input args
ap = argparse.ArgumentParser ()
ap.add_argument ("-i", "--input", type = str, required = True,
	help = "directory to the input images")
ap.add_argument ("-o", "--output", type = str, required = False,
	help = "directory for the output images (if no set use input)")
ap.add_argument ("-a", "--action", type = str, required = True,
	choices = ["blur", "noise", "show"],
	help = "show or save images")
args = vars (ap.parse_args () )

# Args parse
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

# Blur image
def blur (image):
	x = int (image.shape[0] / 90 // 2 * 2 + 1)
	image_blur = cv2.GaussianBlur (image, (x, x), 0)
	return image_blur

# Noide image
def noise (image):
	image_noise = random_noise (image)
	image_noise = (255 * image_noise).astype (np.uint8)
	return image_noise

# Read only images in directory
def read_images_in_dir (path):
	images = []
	valid_images = [".jpg", ".jpeg", ".png"]
	for f in os.listdir (path):
		ext = os.path.splitext (f)[1]
		if ext.lower () in valid_images:
			images.append (os.path.join (path,f) )

	return images

# Preview blur and noise images
def show ():

	# Read only images in directory
	images_path = read_images_in_dir (input)

	# Read random image
	image = cv2.imread (random.choice (images_path) )
	print ("image.shape", image.shape)

	# Blur image
	image_blur = blur (image)
	# Noise image
	image_noise = noise (image)

	# Concate images in row
	image_x = np.concatenate ( (image, image_blur), axis = 1)
	image_x = np.concatenate ( (image_x, image_noise), axis = 1)

	# Calculate ratio deskop height / final image
	desk_ratio = image_x.shape[1] / desk_width

	# Show preview
	window_name = "Preview window"
	image_preview = cv2.resize (image_x, (int (image_x.shape[1] / desk_ratio), int (image_x.shape[0] / desk_ratio) ) )
	cv2.imshow (window_name, image_preview)
	cv2.moveWindow (window_name ,0 ,70)
	cv2.waitKey ()

# Save augmented images
def save ():

	# Read only images in directory
	images_path = read_images_in_dir (input)

	for image_name in images_path:
		# Read image
		image = cv2.imread (image_name)

		if action == "blur":
			image_aug = blur (image)

		if action == "noise":
			image_aug = noise (image)

		file_name = (os.path.join (output,
			os.path.splitext (os.path.basename (image_name) )[0]
			+ "_" + action
			+ os.path.splitext (os.path.basename (image_name) )[1])
		)
		print (file_name)
		cv2.imwrite (file_name, image_aug)

# Show augmented preview
if action == "show":
	show ()
# Save augmented images
elif (action == "blur") or (action == "noise"):
    save ()
