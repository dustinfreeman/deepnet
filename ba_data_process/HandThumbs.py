import numpy as np
import struct
import random


#paths of bin files
paths = [ ]
paths.append("F:\\GroupActivityStudy\\HandThumbFiles\\Aug 27-Couch-handthumbs")
paths.append("F:\\GroupActivityStudy\\HandThumbFiles\\Aug 27-Chairs-handthumbs")
paths.append("F:\\GroupActivityStudy\\HandThumbFiles\\Aug 28 1900-Chairs-handthumbs")
paths.append("F:\\GroupActivityStudy\\HandThumbFiles\\Aug 28 1900-Couch-handthumbs")
paths.append("F:\\GroupActivityStudy\\HandThumbFiles\\Aug 28 2200-Chairs-handthumbs")
paths.append("F:\\GroupActivityStudy\\HandThumbFiles\\Aug 28 2200-Couch-handthumbs")
paths.append("F:\\GroupActivityStudy\\HandThumbFiles\\Aug 30 2100-Chairs-handthumbs")
paths.append("F:\\GroupActivityStudy\\HandThumbFiles\\Aug 30 2100-Couch-handthumbs")
paths.append("F:\\GroupActivityStudy\\HandThumbFiles\\Sept 4 2100-Chairs-handthumbs")
paths.append("F:\\GroupActivityStudy\\HandThumbFiles\\Sept 4 2100-Couch-handthumbs")

IMAGE_DIM = 32
IMAGE_SIZE = IMAGE_DIM*IMAGE_DIM

def parse_bin_line(bin_file):

	hand = 'u' #undefined
	image_array = np.zeros(IMAGE_SIZE)
	try:
		hand_str_len = struct.unpack('c',bin_file.read(1))
		hand_c = str(struct.unpack('c',bin_file.read(1))[0])
		
		r = bin_file.read(4*IMAGE_SIZE)
		#print len(r)
		if len(r) < 4096:
		 	print "last:"
		 	print r[-10:-1]

	 	if hand_c == 'h':
			hand = 1
		elif hand_c == 'n':
			hand = 0
		else: 
			print "Got other than h or n for hand: " + str(hand_c)
			print r
			raise EOFError

		file_tuple = struct.unpack('f'*IMAGE_SIZE,r)

		for i in range(IMAGE_SIZE):
			image_array[i] = file_tuple[i]

		#print image_array
	except EOFError as e:
		print e 
		return True, hand, image_array
	
	return False, hand, image_array

def parse_line(line):
	line_split = line.split(',')

	hand_str = line_split[0]

	hand = -1

	if "no hand" in hand_str:
		hand = 0
	elif "hand" in hand_str:
		hand = 1
	else:
		print "got unexpected hand: " + hand_str

	image_array = np.zeros(IMAGE_SIZE)
	for i in range(IMAGE_SIZE):
		image_array[i] = float(line_split[i+1])

	return False, hand, image_array

def print_stats():
	for path in paths:
		print "reading " + path

		bin_file = open(path+".bin","rb")
		_file = open(path + ".txt","r")

		hand_count = 0
		no_hand_count = 0

		eof = False

		for line in _file:
		#for i in range(1000):
		#while True:
			#eof, hand, image_array = parse_bin_line(bin_file)
			eof, hand, image_array = parse_line(line)

			if (eof):
				print "got eof"
				break

			if hand == 1:
				hand_count += 1
			if hand == 0:
				no_hand_count += 1

		# 	if eof:
		# 		break

		print "hand count: " + str(hand_count)
		print "no hand count: " + str(no_hand_count)


def create_np_arrays():
	#target sizes
	TARGET_TRAIN = 80000
	TARGET_TEST = 10000
	TARGET_VALIDATION = 10000

	#expect this fraction of the data to have a hand.
	hand_fraction = 0.025
	#in actual data, seems to be ~0.27.

	#create train, test and validation data array and labels
	train = np.zeros([TARGET_TRAIN,IMAGE_SIZE])
	train_labels = np.zeros(TARGET_TRAIN)
	train_hand_count = 0
	train_no_hand_count = 0

	test = np.zeros([TARGET_TEST,IMAGE_SIZE])
	test_labels = np.zeros(TARGET_TEST)
	test_hand_count = 0
	test_no_hand_count = 0

	validation = np.zeros([TARGET_VALIDATION,IMAGE_SIZE])
	validation_labels = np.zeros(TARGET_VALIDATION)
	validation_hand_count = 0
	validation_no_hand_count = 0

	files = []

	#load files into array
	for path in paths:
		files.append(open(path + ".txt","r"))

	while True:
		print "-------------"
		print "train_hand_count " + str(train_hand_count)
		print "train_no_hand_count " + str(train_no_hand_count)
		print "test_hand_count " + str(test_hand_count)
		print "test_no_hand_count " + str(test_no_hand_count)
		print "validation_hand_count " + str(validation_hand_count)
		print "validation_no_hand_count " + str(validation_no_hand_count)

		#test if done
		if train_hand_count + train_no_hand_count == TARGET_TRAIN and \
			test_hand_count + test_no_hand_count == TARGET_TEST and \
			validation_hand_count + validation_no_hand_count == TARGET_VALIDATION:
			break
		
		#choose random file to read from
		_file = files[random.randrange(len(files))]
		#read line
		line = _file.readline()
		eof, hand, image_array = parse_line(line)

		#print image_array

		#choose which array to place it in.
		placement_array = None
		placement_label_array = None
		placement_index = None
			
		if hand == 0:

			in_train = int(TARGET_TRAIN*(1-hand_fraction) - train_no_hand_count)
			in_test = int(TARGET_TEST*(1-hand_fraction) - test_no_hand_count)
			in_validation = int(TARGET_VALIDATION * (1-hand_fraction) - validation_no_hand_count)

			range_size = in_train + in_test + in_validation
			if range_size > 0:
				placement = random.randrange(range_size)

				if placement < in_train:
					placement_array = train
					placement_label_array = train_labels
					placement_index = train_no_hand_count + train_hand_count
					train_no_hand_count += 1
				elif placement < in_train + in_test:
					placement_array = test
					placement_label_array = test_labels
					placement_index = test_no_hand_count + test_hand_count
					test_no_hand_count += 1
				else:
					placement_array = validation
					placement_label_array = validation_labels
					placement_index = validation_no_hand_count + validation_hand_count
					validation_no_hand_count += 1

		elif hand == 1:
			in_train = TARGET_TRAIN*(hand_fraction) - train_hand_count
			in_test = TARGET_TEST*(hand_fraction) - test_hand_count
			in_validation = TARGET_VALIDATION * (hand_fraction) - validation_hand_count

			range_size = in_train + in_test + in_validation
			if range_size > 0:
				placement = random.randrange(range_size)

				if placement < in_train:
					placement_array = train
					placement_label_array = train_labels
					placement_index = train_no_hand_count + train_hand_count
					train_hand_count += 1
				elif placement < in_train + in_test:
					placement_array = test
					placement_label_array = test_labels
					placement_index = test_no_hand_count + test_hand_count
					test_hand_count += 1
				else:
					placement_array = validation
					placement_label_array = validation_labels
					placement_index = validation_no_hand_count + validation_hand_count
					validation_hand_count += 1

		#place in array
		if not placement_array is None:
			for i in range(IMAGE_SIZE):
				placement_array[placement_index][i] = image_array[i]
			placement_label_array[placement_index] = hand

	#close input files
	for _file in files:
		_file.close()

	#save out np arrays
	train_file = open("train.npy","wb")
	np.save(train_file,train)
	train_file.close()
	train_labels_file = open("train_labels.npy","wb")
	np.save(train_labels_file,train_labels)
	train_labels_file.close()

	test_file = open("test.npy", "wb")
	np.save(test_file,test)
	test_file.close()
	test_labels_file = open("test_labels.npy","wb")
	np.save(test_labels_file,test_labels)
	test_labels_file.close()

	validation_file = open("validation.npy", "wb")
	np.save(validation_file,validation)
	validation_file.close()
	validation_labels_file = open("validation_labels.npy","wb")
	np.save(validation_labels_file,validation_labels)
	validation_labels_file.close()

if __name__ == "__main__":
	#print_stats()
	create_np_arrays()