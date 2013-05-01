from HandThumbs import *
from PIL import Image
import numpy as np

#import of bunch of handthumbs and display them.

def displayThumbs(labels_path,data_path,trained_labels_path):
	trained_labels_file = open(trained_labels_path,"r")
	labels_file = open(labels_path,"r")
	data_file = open (data_path,"r")
	trained_labels = np.load(trained_labels_file)
	labels = np.load(labels_file)
	data = np.load(data_file)

	hand_indices = []
	trained_hand_indices = []

	META_DIM = 16
	big_img = Image.new("F", (META_DIM*IMAGE_DIM,META_DIM*IMAGE_DIM), "black")
	big_pixels = big_img.load()

	big_trained_img = Image.new("F", (META_DIM*IMAGE_DIM,META_DIM*IMAGE_DIM), "black")
	big_trained_pixels = big_trained_img.load()

	for i in range(len(labels)):
		if (labels[i] == 1): #hand

			img = Image.new("F", (IMAGE_DIM,IMAGE_DIM), "black")
			pixels = img.load() #a reference

			big_x = len(hand_indices) % META_DIM
			big_y = len(hand_indices) / META_DIM

			for x in range(IMAGE_DIM):
				for y in range(IMAGE_DIM):
					val = data[i][x + IMAGE_DIM*y]*255
					#print str(val) + "," ,
					pixels[x,y] = val

					big_pixels[big_x*IMAGE_DIM + x, big_y*IMAGE_DIM + y] = val

			#img.show()
			img = img.convert("RGB")
			img.save("local_output/hand" + str(i) +".png")

			hand_indices.append(i)

		if (trained_labels[i][1] > trained_labels[i][0]):
			big_trained_x = len(trained_hand_indices) % META_DIM
			big_trained_y = len(trained_hand_indices) / META_DIM

			for x in range(IMAGE_DIM):
				for y in range(IMAGE_DIM):
					val = data[i][x + IMAGE_DIM*y]*255

					big_trained_pixels[big_trained_x*IMAGE_DIM + x, big_trained_y*IMAGE_DIM + y] = val

			trained_hand_indices.append(i)

	big_img = big_img.convert("RGB")
	big_img.save("pre-training_hand.png")


	big_trained_img = big_trained_img.convert("RGB")
	big_trained_img.save("training_hand.png")

	print len(hand_indices)
	print len(trained_hand_indices)

if __name__ == "__main__":
	labels_path = "validation_labels.npy"
	data_path = "validation.npy"
	trained_labels_path = "trained/validation_trained.npy"

	displayThumbs(labels_path,data_path,trained_labels_path)
