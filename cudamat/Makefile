# attempting to get it to run with gcc-4.4
CC=/usr/bin/gcc-4.4/

cudamat:
	nvcc -O --ptxas-options=-v --compiler-options '-fPIC' -o libcudamat.so --shared cudamat.cu cudamat_kernels.cu -lcublas -L$(CUDA_LIB)
	nvcc -O --ptxas-options=-v --compiler-options '-fPIC' -o libcudalearn.so --shared learn.cu learn_kernels.cu -lcublas -L$(CUDA_LIB)


clean:
	rm *.linkinfo *.pyc *.so
