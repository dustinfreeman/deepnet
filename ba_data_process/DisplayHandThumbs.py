from HandThumbs import *
from PIL import Image
import numpy as np

#import of bunch of handthumbs and display them.
MAX_DISPLAY = 250
META_DIM = 16


def make_image(data_path, index_list, image_name):
	data_file = open (data_path,"rb")
	data = np.load(data_file)
	data_file.close()

	big_img = Image.new("F", (META_DIM*IMAGE_DIM,META_DIM*IMAGE_DIM), "black")
	big_pixels = big_img.load()

	for i in range(len(index_list)):
		big_x = i % META_DIM
		big_y = i / META_DIM

		for x in range(IMAGE_DIM):
			for y in range(IMAGE_DIM):
				val = data[index_list[i]][x + IMAGE_DIM*y]*255

				big_pixels[big_x*IMAGE_DIM + x, big_y*IMAGE_DIM + y] = val

	big_img = big_img.convert("RGB")
	big_img.save(image_name)



def displayThumbs(labels_path,data_path,trained_labels_path):
	trained_labels_file = open(trained_labels_path,"r")
	labels_file = open(labels_path,"r")
	data_file = open (data_path,"r")
	trained_labels = np.load(trained_labels_file)
	labels = np.load(labels_file)
	data = np.load(data_file)
	data_file.close()
	labels_file.close()
	trained_labels_file.close()

	hand_indices = []
	trained_hand_indices = []

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
			#big_trained_x = len(trained_hand_indices) % META_DIM
			#big_trained_y = len(trained_hand_indices) / META_DIM

			for x in range(IMAGE_DIM):
				for y in range(IMAGE_DIM):
					val = data[i][x + IMAGE_DIM*y]*255

					#HACK big_trained_pixels[big_trained_x*IMAGE_DIM + x, big_trained_y*IMAGE_DIM + y] = val

			trained_hand_indices.append(i)

	big_img = big_img.convert("RGB")
	big_img.save("pre-training_hand.png")

	same = 0
	new = 0
	new_labels = []
	lost = 0
	lost_labels = []
	for i in range(len(hand_indices)):
		if hand_indices[i] in trained_hand_indices:
			same += 1
		else:
			lost += 1
			lost_labels.append(i)

	for i in range(len(trained_hand_indices)):
		if not trained_hand_indices[i] in hand_indices:
			new += 1
			new_labels.append(i)

	big_trained_img = big_trained_img.convert("RGB")
	big_trained_img.save("training_hand.png")

	print "Original hand labels " + str(len(hand_indices))
	print "Trained hand labels " + str(len(trained_hand_indices))
	print "same " + str(same)
	print "new " + str(new)
	print "lost " + str(lost)

	make_image(data_path, new_labels, "new_labels.png")
	make_image(data_path, lost_labels, "lost_labels.png")

if __name__ == "__main__":
	#labels_path = "ba_batchsorted/validation_batchsorted_labels.npy"
	labels_path = "ba_unsorted/validation_labels.npy"
	#data_path = "ba_batchsorted/validation_batchsorted.npy"
	data_path = "ba_unsorted/validation.npy"
	trained_labels_path = "ba_batchsorted/results/validation_trained.npy"

	displayThumbs(labels_path,data_path,trained_labels_path)
