#takes in labelled npy-style data, 
# outputs it sorted into batches containing equal numbers of labels
# expects binary labels
import sys
import numpy as np
from HandThumbs import *

batchsize = 128

def copyarr(dst,src):
	for i in range(len(src)):
		dst[i] = src[i]


def batchsort(dataname,outputpath):
	#load data
	f = open(dataname + ".npy","rb")
	data = np.load(f)
	f.close()
	fl = open(dataname + "_labels.npy","rb")
	data_labels = np.load(fl)
	fl.close()

	count_1 = np.count_nonzero(data_labels)
	count_0 = len(data_labels) - count_1
	
	#load data into temporary arrays by type
	index_0 = 0
	index_1 = 0
	data_0 = np.zeros([count_0, IMAGE_SIZE])
	data_1 = np.zeros([count_1, IMAGE_SIZE])
	for i in range(len(data_labels)):
		if data_labels[i] == 0:
			#np.copyto(data_0[index_0],data[i])
			copyarr(data_0[index_0],data[i])
			index_0+=1
		else: #data_labels[i] == 1:
			#np.copyto(data_1[index_1],data[i])
			copyarr(data_1[index_1],data[i])
			index_1+=1

	#create sorted np array
	batchsort_len = 2 * max(count_0,count_1) + (batchsize - (2 * max(count_0,count_1)) % batchsize)
	data_batchsort = np.zeros([batchsort_len, IMAGE_SIZE])
	data_batchsort_labels = np.zeros(batchsort_len)

	data_index = 0
	index_0 = 0
	index_1 = 0
	final_batch = False

	while True:
		if (index_0 + batchsize/2 > count_0 + 1 and count_0 > count_1) or \
			(index_1 + batchsize/2 > count_1 + 1 and count_1 > count_0):
			final_batch = True
			#print index_0
			#print count_0
			#print index_1
			#print count_1
			#print data_index
		
		#copy the zeros
		for i in range(batchsize/2):
			copyarr(data_batchsort[data_index],data_0[index_0])
			data_batchsort_labels[data_index] = 0
			data_index += 1
			index_0 += 1
			if index_0 == count_0:
				index_0 = 0
		#copy the ones
		for i in range(batchsize/2):
			copyarr(data_batchsort[data_index],data_1[index_1])
			data_batchsort_labels[data_index] = 1
			data_index += 1
			index_1 += 1
			if index_1 == count_1:
				index_1 = 0

		if final_batch:
			break

	#save data
	f = open(outputpath + dataname + "_batchsorted.npy","wb")
	np.save(f,data_batchsort)
	f.close()
	fl = open(outputpath + dataname + "_batchsorted_labels.npy","wb")
	np.save(fl,data_batchsort_labels)
	fl.close()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: <dataname> <outputpath>"
		print "where the directory should contain <dataname>.npy and <dataname>_labels.npy"
		quit()

	dataname = sys.argv[1]
	outputpath = sys.argv[2]
	batchsort(dataname,outputpath)




