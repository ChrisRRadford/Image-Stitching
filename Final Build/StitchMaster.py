"""----------------------------------------------------
Program: 	Stitch Entire Folder of Images
Name:		Christopher Radford
Supervisor: Dr. Dongmei Chen

Function:	Serves as an easy method of stitching multiple images together by
			passing a single folder in containing SORTED images to be sorted.

Input:		Input command is program name followed by "--first "and path to 
			folder. If running in command promt or terminal must begin by 
			calling python. Path unique to computer and OS. If running from command 
			line prefix command with "python "
 
			python StitchMaster.py --imageSet /Users/chrisradford/Documents/Research/ImagesToPass/Stitch2 --featureDetection orb
			python StitchMaster.py --imageSet /Users/chrisradford/Documents/Research/ImagesToPass/Stitch4 --featureDetection orb

Output:		Stitched image of type .jpg. Path and file name to writen must be manually stated on 
			line 79 and is currently commented out

Notes:		 - When creating a folder containing images the images must be selected so that the 
			NORTH-EAST most image is first. 
			 - Images must be renamed by the order they will be passed
			 - This file will be accompanied with a read me file listing already created folders
			and their corresponding images based on their origional name.
			 - This file must be saved in the same directory as StitchingMaster.py
			 - When result image is shown press any key to continue
----------------------------------------------------"""
#--------CODE TO FOLLOW---------#
#import necessecary Packages
import os 
import cv2
import argparse
from StitchingMaster import Stitcher

#initalize objects
stitcher = Stitcher()
ap = argparse.ArgumentParser()
ap.add_argument("-1", "--imageSet", required=True)
ap.add_argument("-2", "--featureDetection", required=True)
args = vars(ap.parse_args())
#Define variables
imageSize = (1800,1200)						#size of image to be passed to stitcher
showMatches = True 							#True if wish to see matches; False otherwise
keypoints = []
descriptors = []
resultImageSize = (1200,900)				#Size of final image to be displated and saved
fileList = os.listdir(args["imageSet"])	#list of images in folder
path = os.path.abspath(args["imageSet"])		#Folder path
featureDetection = (args["featureDetection"])
featureDetection = featureDetection.upper()
imagesToStitch = []



# Ensure we do not get any hidden files taken from os.listdir().
# In OS X a .DS_Store file automatically created and is a hidden
# file that will be picked up.
for files in fileList:
	if not files.startswith('.'):
		imagesToStitch.append(files)

print "-------------------"
#----Base Case[0-1]----#
if len(imagesToStitch) < 2:
	print "Not enough images to stitch"
	quit()
#----Base Case[2]----#
else:
	print "Processing image: ",imagesToStitch[0]
	img1 =  cv2.resize(cv2.imread(os.path.join(path,imagesToStitch[0]),1),imageSize)
	print "Processing image: ",imagesToStitch[1]
	img2 = cv2.resize(cv2.imread(os.path.join(path,imagesToStitch[1]),1),imageSize)
	#result = stitched image
	(result,keypoints,descriptors) = stitcher.stitch([img1,img2],showMatches,keypoints,descriptors,featureDetection)
	#ensure good stitch
	if result is None:
		print "Couldnt complete iteration for image:", nextImage
		quit()
#----Base Case[3:n]----#
	if len(imagesToStitch) > 2:
		imagesToStitch = imagesToStitch[2:]
		#stitch remaining images to result
		for image in imagesToStitch:
			print "Processing image: ",image
			nextImage = cv2.resize(cv2.imread(os.path.join(path,image),1),imageSize)
			(result,keypoints,descriptors) = stitcher.stitch([result,nextImage],showMatches,keypoints,descriptors,featureDetection)
			#ensure good stitch
			if result is None:
				print "Couldnt complete iteration for image:", nextImage
				quit()

print "-------------------"
cv2.imwrite('/Users/chrisradford/Documents/Research/ImagesToPass/master.jpg',result)
#resize final images for better inital viewing
result = cv2.resize(result,resultImageSize)	
cv2.imshow("Result",result)
cv2.waitKey(0)
#save result image for later use. This must be decalred by user here
cv2.destroyAllWindows()


