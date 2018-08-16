Title: 		Modeling Bull Sperm Motility Using Methods in Image Analysis
Author: 	Linan Zhang
		Department of Mathematical Sciences
		Carnegie Mellon University
Date:		April 2017
Language:	Python



------------------------------------------------------------------------------------
		CONTENTS OF THIS FILE
------------------------------------------------------------------------------------
 * Introduction
 * Checklist
 * Requirements
 * Examples
 * Acknowledgement
 * References



------------------------------------------------------------------------------------
		INTRODUCTION
------------------------------------------------------------------------------------
	Based on the information released by Centers for Disease Control and Prevention, about 15% of couples in US have infertility problems. This situation leads to researches including the study of sperm motility. Sperm motility is of great interest to biologists studying sperm function and to medical engineers evaluating and treating male infertility. Animal sperm are also studied by agriculturalists engaged in industrial animal husbandry. 

	An experiment was designed to study sperm motility. Bull sperm were put in a chamber with a given medium. The movement of bull sperm was then recorded into a movie by taking high speed images from a microscope. The goal was to develop male contraceptives by studying how chemicals change bending and swimming of sperm.

	To analyze sperm motility, people usually measure the following quantities:- swimming velocity;- head centerline deviation, which measures how far the sperm is from being swimming straight; 
- flagellum curvature, which measures the degree of bending of the flagellum;- bending and sliding energies, which are stored in the sperm body to support the swimming.

	Calculating above quantities requires that we obtain a segmentation of the sperm head and flagellum, which accurately represent the location of the sperm. This project focuses on how to segment the sperm from laboratory data (Steps 1-3). It also includes an simple algorithm to separate the sperm head and flagellum from the segmentation result (Step 4).
	
	---------------------------------------------------------------------------------
	| Step 1: movie from the laboratory						|
	|		|								|
	|		|	Pre-prossessing: correcting nonuniform illumination	|
	|		V								|
	| Step 2: movie with uniform illumination					|
	|		|								|
	|		|	Smoothing						|
	|		V								|
	| Step 3: movie after blurring							|
	|		|								|
	|		|	Segmentation						|
	|		V								|
	| Step 4: movie with segmented result						|
	|		|								|
	|		|	Analysis: determining good frames			|
	|		|		  splitting head and flagellum			|
	|		V								|
	| Step 5: (i) movie with segmented result of the good frames only		|
	|	  (2) dictionary that contains some basic information about the sperm	|
	|	      in each frame, i.e. head pixels, flagellum pixels. 		|
	|		|								|
	|		|	Summary: plotting head and flagellum separately		|
	|		|		 plotting head trajectory			|
	|		V								|
	|	     the end								|
	---------------------------------------------------------------------------------



------------------------------------------------------------------------------------
		CHECKLIST
------------------------------------------------------------------------------------
- Code:
	- ReadMe.txt (this file)
	- SpermSegReg.m (main)
	- Step1.m
	- Step2.m
	- Step3.m
	- Step4.m
	- Step5.m
	- Step4Helpers.m
- Documentation:
	- ReadMe.txt
	- Step01_CorrectingIllumination.pdf
	- Step02_RemovingNoise.pdf
	- Step03_Thresholding.pdf
	- Step04_DetectingSpermBody.pdf
	- Step05_Summary.pdf
- Movie:
	- movie20.mha (data)
	- SpermStep1_CorrectingIllumination.mha
	- SpermStep2_Blurring.mha
	- SpermStep3_Thresholding.mha
	- SpermStep4_GoodFramesOnly.mha
	- SpermStep5_HeadFlagellum.mha.mha
	- SpermStep5_HeadTrajectory.png
	- SpermInfo.mat



------------------------------------------------------------------------------------
		REQUIREMENTS
------------------------------------------------------------------------------------
(1) Install ITK-SNAP, or other softwares that support images in mha format.
(2) Download the folders Code and Movie into one folder from SVN.
	- Code contains all the Python files needed for the program.
	- Movie contains some movies for the examples.
	


------------------------------------------------------------------------------------
		EXAMPLES
------------------------------------------------------------------------------------
(1) To see how the filters and parameters were chosen, and line-by-line explanations of the program, please read the pdf files in the folder Documentation.
(2) Create a new folder with name Output.
(3) To perform
		Pre-processing -> Blurring -> Thresholding -> Analysis -> Summary,
run the following command
		python SpermSegReg.py -i ../Movie/movie20.mha -o ../Movie/ -mf 3 -tr 2 -tv 10 -rs 1 61 221 271 361 411 46 76 166 221 381 421 391 451 391 431 -dt 0.005 -sc 0.1625 -hbr 0.25 -n 1
Please expect about 10 minutes for the program to complete.
(4) To perform
		Blurring -> Thresholding -> Analysis -> Summary,
run the following command
		python SpermSegReg.py -i ../Movie/SpermStep1_CorrectingIllumination.mha -o ../Movie/ -mf 3 -tr 2 -tv 10 -rs 1 61 221 271 361 411 46 76 166 221 381 421 391 451 391 431 -dt 0.005 -sc 0.1625 -hbr 0.25 -n 2
Please expect about 5 minutes for the program to complete.
(5) To perform
		Thresholding -> Analysis -> Summary,
run the following command
		python SpermSegReg.py -i ../Movie/SpermStep2_Blurring.mha -o ../Movie/ -mf 3 -tr 2 -tv 10 -rs 1 61 221 271 361 411 46 76 166 221 381 421 391 451 391 431 -dt 0.005 -sc 0.1625 -hbr 0.25 -n 3
Please expect about 5 minutes for the program to complete.
(6) To perform
		Analysis -> Summary,
run the following command
		python SpermSegReg.py -i ../Movie/SpermStep3_Thresholding.mha -o ../Movie/ -mf 3 -tr 2 -tv 10 -rs 1 61 221 271 361 411 46 76 166 221 381 421 391 451 391 431 -dt 0.005 -sc 0.1625 -hbr 0.25 -n 4



------------------------------------------------------------------------------------
		ACKNOWLEDGEMENT
------------------------------------------------------------------------------------
 * Doctor John Galeotti, Carnegie Mellon University
	- advisor for this project
 * Professor Sarah Olson, Worcester Polytechnic Institute
	- advisor for a similar project in the past, which focused more on modeling 
 * Professor Susan Suarez, Cornell University
	- provider of the movie which was used in this project * Zhiang Zhang, Carnegie Mellon University
	- peer mentor who helped me polish the code



------------------------------------------------------------------------------------
		REFERENCES
------------------------------------------------------------------------------------
The order of the references is based on the order of appearance of each function.
(1) How to add 2D images into a 3D image:
	- http://stackoverflow.com/questions/30237024/operate-on-slices-of-3d-image-in-simpleitk-and-create-new-3d-image
(2) How to delete rows of zeros in a 2D bumpy array:
	- http://stackoverflow.com/questions/11188364/remove-zero-lines-2-d-numpy-array
(3) How to correct nonuniform illumination:
	- https://www.mathworks.com/help/images/examples/correcting-nonuniform-illumination.html
(4) How to organize input arguments:
	- https://docs.python.org/3/library/argparse.html
(5) How to remove all rows in a numpy.ndarray that contain nan:
	- http://stackoverflow.com/questions/11453141/how-to-remove-all-rows-in-a-numpy-ndarray-that-contain-non-numeric-values
(6) How to test whether each element of a 1-D array is also present in a second array:
	- https://docs.scipy.org/doc/numpy/reference/generated/numpy.in1d.html
(7) How to remove some rows from an array:
	- https://docs.scipy.org/doc/numpy/reference/generated/numpy.delete.html
(8) How to attach two arrays:
	- https://docs.scipy.org/doc/numpy/reference/generated/numpy.concatenate.html
(9) How to remove rows of zeros from an array:
	- http://stackoverflow.com/questions/11188364/remove-zero-lines-2-d-numpy-array
(10) How to save a mathplot as a png file:
	- http://stackoverflow.com/questions/9622163/save-plot-to-image-file-instead-of-displaying-it-using-matplotlib-so-it-can-be

