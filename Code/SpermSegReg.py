from __future__ import print_function
import argparse
import numpy as np
import os
import scipy.io as sio
import SimpleITK as sitk
import sys

from Step1 import * 
from Step2 import *
from Step3 import *
from Step4 import *
from Step5 import *

def main():
    # Define arguments. #
    parser = argparse.ArgumentParser( description = "Sperm Segmentation and Registration")
        # step 1 -- correcting nonuniform illumination #
    parser.add_argument('-i', '--input_file_name', type=str,
                        help='The input file name.')
    parser.add_argument('-o', '--output_path', type=str,
                        help='The output path.')
    parser.add_argument('-n', '--starting_step', type=int,
                        help='1-correcting nonuniform illumination, 2-blurring,'
                        '3-thresholding, 4-image analysis')
        # step 2 -- blurring #
    parser.add_argument('-mf', '--median_filter_radius', type=int,
                        help='Neighborhood radius of the median filter.');
        # step 3 -- thresholding #
    parser.add_argument('-tr', '--threshold_radius', type=int,
                        help='Neighborhood radius of the threshold algorithm.')
    parser.add_argument('-tv', '--threshold_value', type=int,
                        help='Threshold value of the threshold algorithm.')
    parser.add_argument('-rs', '--regions_of_stains', type=int, nargs='+',
                        help='The regions of the stains.'
                        'Format: xmin1,xmax1,ymin1,ymax1,xmin2,xmax2,ymin2,ymax2,...')
        # step 4 -- image analysis #
    parser.add_argument('-dt', '--deltaT', type=float,
                        help='Time elapsed between two consecutive frames (unit: second).')
    parser.add_argument('-sc', '--scale', type=float,
                        help='Scale of a pixel (unit: nm/pixel).')
    parser.add_argument('-hbr', '--headbodyratio', type=float,
                        help='If the ratio of head length to body length exceeds 2*hbr,'
                        'the frame is considered as a valid frame.')
    args = parser.parse_args()
    

    # Read the image. #
    imread = sitk.ImageFileReader()
    imread.SetFileName( args.input_file_name )
    movie = imread.Execute()
    

    # Define the regions of stains. #
    stains = args.regions_of_stains
    ns = len(stains)/4
    stains = np.asarray(stains)
    stains = np.reshape(stains,(ns,4))

    
    # Define a loop for the job. #
    def func_wrapper(func, args):
        return func(*args)       
    job_list = [ [PreProcessing, args.output_path],
                 [Blurring, args.output_path, args.median_filter_radius],
                 [Thresholding, args.output_path, args.threshold_radius, args.threshold_value, stains]]

    # Steps 1-3. Perform image processing. #
    for i in range(args.starting_step - 1, len(job_list)):
        job = job_list[i][0]
        job_args = job_list[i][1:]
        job_args.insert(0, movie)
        movie = func_wrapper(job, job_args)

    # Step 4. Do calculations. #
    threshold1 = 2.75
    maxheadwidth = 80
    threshold2 = 135
    movie,sperm = DetectingSpermBody( movie, args.output_path, args.deltaT, args.scale,
                                threshold1, maxheadwidth, args.headbodyratio, threshold2 )
    sio.savemat(args.output_path+"SpermInfo.mat", sperm)

    # Step 5. Make a summary. #
    Summary( movie, args.output_path, sperm )

    print("  Program done!  ")
    
    return

if __name__ == '__main__':
    main()
