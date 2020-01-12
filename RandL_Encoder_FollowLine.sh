#!/bin/bash

#This will start the program for the Right wheel Encoder
#As well as send it to a text file for post processing
echo "Right Wheel Job"
python R_Encoder.py > R_Encoder.txt &

#This will start the program for the left wheel Encoder
#As well as send it to a text file for post processing
echo "Left Wheel Job"
python L_Encoder.py > L_Encoder.txt &

# This will send the output of the Line follow to a dumb buffer file
echo "Line Follow Job"
python Drive3.py > Speed.txt &
