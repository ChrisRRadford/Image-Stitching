Program: 	README
Name:		Christopher Radford
Supervisor: Dr. Dongmei Chen

-----------------
Intro
-----------------
This file will explain the installation processes for OpenCV - 3.1.0-dev 
and other packages which are necessecary in order to use provided programs.

Provided Programs and Folders
- StitchMaster.py		(Execution Program)
- StitchingMaster.py	(Main Program)
- ImagesToPass Folder 	(Folder containing Different configurations of Images to stitch) 
-----------------
Installation
-----------------
Nedded:
	Python 2.7.x
	Numpy - installed using pip command for python
	matplotlib - installed using pip command for python
	
	For install instructions for above packages see:
		https://www.youtube.com/watch?v=-llHYUMH9Dg&t=135s

	Imutils - download from github and installed using pip command for python

	For install instructions for imutils see:
		https://www.youtube.com/watch?v=-llHYUMH9Dg&t=135s


	OpenCV 3.1.0-dev - This will be that hardest packages to download:

	Our goal is to do a manually install of OpenCV in conjunction with OpenCV_Contrib extra modules 
	which we need to run program. We only need xfeatures2d module from Opencv_Contrib

	For install instructions for OpenCV with extra modules for windows see (Given in order of helpfullness:
		https://github.com/opencv/opencv_contrib
		https://putuyuwono.wordpress.com/2015/04/23/building-and-installing-opencv-3-0-on-windows-7-64-bit/
		http://docs.opencv.org/trunk/de/d25/tutorial_dnn_build.html
		http://l.facebook.com/l.php?u=http%3A%2F%2Fstackoverflow.com%2Fquestions%2F37517983%2Fopencv-install-opencv-contrib-on-windows&h=qAQHY5At5

	Tips for OpenCV Installation
	- Create a new folder to hold new build of opencv
	- Copy cv2.pyd found in Python2.7/Lib/site-packages to another folder to ensure you do not lose current version of OpenCV if you wish to keep it.
-----------------
Confrim Installation
-----------------
1. Ensure Python 2.7 installed and command prompt executable path exists.
	- Open cmd promt 
	- enter "python"
		If python opens in cmd promt you have secussefully installed python
	- to leave python enter "exit()"
2. Ensure numpy and umutils installed correctly
	- Open cmd promt 
	- enter "python"
	- in python, enter "import numpy as np"
		if no errors you have successfully installed numpy
	- still in python, enter "import imutils"
		if no errors you have successfully installed imutils
3. Ensure OpenCV installed correctly
    - Open cmd promt 
	- enter "python"
	- in python, enter "import cv2"	
		if no errors you have successfully installed OpenCV and now must check version installed
	- in python, enter "cv2 .__version__"
		if output is '3.1.0-dev' we have installed the correct version of Opencv and can run the program
-----------------
Installation Debug
-----------------
The main error encourntered when installing Opencv 3.1.0-dev was the ackages would build and install but when attempted to import in python
it would not be able to find DLL files. See following pages to work around
	http://stackoverflow.com/questions/40792521/opencv-3-1-0-with-extra-modules-throws-dll-load-failed-error
-----------------
Execute Program
-----------------
1. Open Command Window in folder containing program or opencv Command Window and navigate to folder
2. enter "python StitchMaster.py --first <folder containing images to stitch>"
	ex - python StitchMaster.py --first /Users/chrisradford/Documents/Research/ImagesToPass/Stitch2
-----------------
Setup ImagestoPass Folder
-----------------
You will recevied a zipped folder named "ImagesToPass" which will contain folder with images already ordered
for successful stitching. When creating a new "Stitch" folder inside "ImagesToPass" copy images in proper order 
to stich from soruce to this file and name them so they are ordered correctly. 
	See: ImagesToPass/Stitch4 for example

Here is the stitch image folders explained corresponding to their images from provided UAV Data
Stitch2
	_001.jpg - /avanetics-5775d1/_DSC0049.jpg
	-002.jpg - /avanetics-5775d1/_DSC0035.jpg
Stitch4
	_001.jpg - /avanetics-5775d1/_DSC0086.jpg
	-002.jpg - /avanetics-5775d1/_DSC0073.jpg
	_003.jpg - /avanetics-5775d1/_DSC0049.jpg
	-004.jpg - /avanetics-5775d1/_DSC0035.jpg
