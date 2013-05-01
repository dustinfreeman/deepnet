#takes in labelled npy-style data, 
# outputs it sorted into batches containing equal numbers of labels
# expects binary labels
import sys
import numpy as np

batchsize = 128

def batchsort(dataname):
	#load data

	#create sorted np array

	#save data

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: <dataname>"
		print "where the directory should contain <dataname>.npy and <dataname>_labels.npy"
		quit()

	dataname = sys.argv[1]
	batchsort(dataname)




