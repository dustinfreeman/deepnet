#!/bin/bash
# Trains a feed forward net on MNIST.
train_deepnet='python ../../trainer.py'
${train_deepnet} model_conv.pbtxt train.pbtxt eval.pbtxt
