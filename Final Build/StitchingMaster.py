"""----------------------------------------------------
Program: 	Stitcher
Name:		Christopher Radford
Supervisor: Dr. Dongmei Chen

Function:	Serves as the main program that stitches two images together. Should be used by another
			program that calls it to stitch desired images.

Input:		Input must be provided by another program an is not meant to be run as a stand alone
			code. Input function "stitch" requires two images of any type followed by a Bool
			defining showMatches

			stitcher.stitch([img1,img2],showMatches)

Output:		Stitched image of type .jpg. This output should be returned to a varialbe defined in 
			another program. In example below result is where the output will be stored.

				result = stitcher.stitch([img1,img2],showMatches)

Notes:		 - 
----------------------------------------------------"""
#--------CODE TO FOLLOW---------#
#import necessecary Packages
import cv2
import imutils
import numpy as np


class Stitcher:
	def __init__(self):
		# determine if we are using OpenCV v3.X
		self.isv3 = imutils.is_cv3()

		"""------------------------------------------
FUNCTION:	Main stitch function that stores all necessary and found data
			to stitch images
ARGUMENTS:  a set of two images of any type and Bool stating showMatches condition.
			This function will be called from another program and therefore require
			constructor
			- stitcher.stitch([img1,img2],showMatches)
RETURNS:    Returns resulting image that has been stitched
			- return Result
----------------------------------------------------"""

	def stitch(self,imgSet,showMatches,keypoints,descriptors):
		#Base Case[2]
		if keypoints == []:
			first,second = imgSet
			#detect keypoints in each image
			(kp1,desc1) = self.keypointDescriptor(first)
			(kp2,desc2) = self.keypointDescriptor(second)
			keypoints.extend(kp1)
			keypoints.extend(kp2)
			desTotal = np.concatenate((desc1,desc2),axis=0)
			# match based on kepoints and their descritpors
			#returns found matches homography matrix built from the good matches
			M = self.matchFeatures(kp1,desc1,kp2,desc2)
			#Ensure there were enough matches
			if M is None:
				return None
			(matches,H) = M

			# if asked to draw the matches between images
			if showMatches:
				self.drawMatches(first,kp1,second,kp2,matches)
			

			#Base Case[3:n]
		else:
			first,second = imgSet
			#detect keypoints in each image
			(kp,desc) = self.keypointDescriptor(second)
			keypoints.extend(kp)
			desTotal = np.concatenate((descriptors,desc),axis=0)
			# match based on kepoints and their descritpors
			#returns found matches homography matrix built from the good matches
			M = self.matchFeatures(keypoints,descriptors,kp,desc)
			#Ensure there were enough matches
			if M is None:
				return None
			(matches,H) = M

			# if asked to draw the matches between images
			if showMatches:
				self.drawMatches(first,keypoints,second,kp,matches)
			
		#Take the two images and the homography matrix computed from
		result = self.stitchMatches(first,second,H)
		croppedResult = self.crop(result)
		return (croppedResult,keypoints,desTotal)

	def stitchOld(self,imgSet,showMatches):	
		first,second = imgSet
		#detect keypoints in each image
		(kp1,desc1) = self.keypointDescriptor(first)
		(kp2,desc2) = self.keypointDescriptor(second)
		print type(kp1)
		print type(desc1)
		desTotal = np.concatenate((desc1,desc2),axis=0)
		print desTotal
		
		print desTotal
		# match based on kepoints and their descritpors
		#returns found matches homography matrix built from the good matches
		M = self.matchFeatures(kp1,desc1,kp2,desc2)
		#Ensure there were enough matches
		if M is None:
			return None
		(matches,H) = M

		# if asked to draw the matches between images
		if showMatches:
			self.drawMatches(first,kp1,second,kp2,matches)
		
		#Take the two images and the homography matrix computed from
		result = self.stitchMatches(first,second,H)
		croppedResult = self.crop(result)
		return croppedResult


		"""------------------------------------------
FUNCTION:	Detects and describes keypoints and their corresponding
			descriptor
ARGUMENTS:  image of any type - self.keypointDescriptor(image)
RETURNS:    Keypoints and descriptors in tuple form - (kp,desc)
NOTES:      Can modify to use any type of descriptor sush as SIFT, ORB, etc.
----------------------------------------------------"""
	def keypointDescriptor(self,image):
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		surf = cv2.xfeatures2d.SURF_create(700)
		(kp, desc) = surf.detectAndCompute(gray, None)
		#print "number of keypoints: ",len(kp)
		return (kp,desc)

		"""-----------------------------------------
FUNCTION:	Generates matches between images based on their keypoints
			and descriptors and computes the homography between images.
ARGUMENTS:  keypoints and descriptors of image one and two respectively.
			- self.matchFeatures(kp1,desc1,kp2,desc2)
RETURNS:    Returns the found matches and homography matrix in tuple form
			- (matches,homography)
NOTES:      Function can be modified to use any Matcher found in OpenCV 3.X
----------------------------------------------------"""
	def matchFeatures(self,kp1,desc1,kp2,desc2):
		#FLANN params
		FLANN_INDEX_KDTREE = 0
		index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
		search_params = dict(checks=50)
		
		flann = cv2.FlannBasedMatcher(index_params,search_params)
		matches = flann.knnMatch(desc1,desc2,k=2)

		# store all the good matches as per Lowe's ratio test.
		goodMatches = []
		for m,n in matches:
		    if m.distance < 0.6*n.distance:
		        goodMatches.append(m)

		#good matches are 
		if len(goodMatches) > 4:
		    master = np.float32([ kp1[m.queryIdx].pt for m in goodMatches ])
		    new = np.float32([ kp2[m.trainIdx].pt for m in goodMatches ])
		    H, _ = cv2.findHomography(master, new, cv2.RANSAC, 4.0)
		#If not enough good matches found
		else:
			print "Not enough matches"
			return None
		return (matches,H)

		"""-----------------------------------------
FUNCTION:	Draw matches between two images 
ARGUMENTS:  Keypoints of each image, each image, and keypoint matches
			- self.drawMatches(self,image1,kp1,image2,kp2,matches)
RETURNS:    N/A
----------------------------------------------------"""
	def drawMatches(self,image1,kp1,image2,kp2,matches):
		drawGoodMatches= [[0,0] for i in xrange(len(matches))]

		#ratio rest as per Lowe's paper
		#-----used for cv2.drawMatchesKnn
		for i,(m,n) in enumerate(matches):
			if m.distance < 0.4*n.distance:
				drawGoodMatches[i]=[1,0]

		#Params for drawing matches
		draw_params = dict(matchColor = (-1),
						singlePointColor = (-1),
						matchesMask = drawGoodMatches,
						flags = 2)

		drawing = cv2.drawMatchesKnn(image1,kp1,image2,kp2,matches,2,**draw_params)
		#resize for easy viewing
		resizedDrawing = cv2.resize(drawing,(1200,900))#,fx=0.5,fy=0.5)
		cv2.imshow("matched",resizedDrawing)
		cv2.imwrite('C:\Users\cradford\Documents\Research\homography.jpg',drawing)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		
		"""-----------------------------------------
FUNCTION:	Stitch images based on homography matrix using warpPerspective
ARGUMENTS:  Each image and computed homography matrix between two images.
			- self.stitchMatches(self,image1,image2,homography)
RETURNS:    Returns resultant stitched image.
			- return result
NOTES:      Function partially complete in that it can only stitch images 
			in two directions and therefore requires that images must still be
			manually ordered
----------------------------------------------------"""		
	def stitchMatches(self,image1,image2,homography):
		#gather x and y axis of images that will be stitched
		height1, width1 = image1.shape[0], image1.shape[1]
		height2, width2 = image2.shape[0], image2.shape[1]
		#create blank image that will be large enough to hold stitched image
		blank_image = np.zeros(((width1 + width2),(height1 + height2),3),np.uint8)
		#stitch image two into the resulting image while using blank_image 
		#to create a large enough frame for images
		result = cv2.warpPerspective((image1),homography,blank_image.shape[0:2])
		#numpy notation for slicing a matrix together allows you to see the image
		result[0:image2.shape[0], 0:image2.shape[1]] = image2
		return result


		"""-----------------------------------------
FUNCTION:	Crop the stitched image to remove excess black space
ARGUMENTS:  Stitched image
RETURNS:    Croped stitched image
----------------------------------------------------"""
	def crop(self,image):
		grayed = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		(_,thresh) = cv2.threshold(grayed,1,255,cv2.THRESH_BINARY)
		result, contours, _= cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		x, y = [], []
		for i in range(len(contours)):
		    for j in range(len(contours[i])):
		        x.append(contours[i][j][0][0])
		        y.append(contours[i][j][0][1])
		x1, x2, y1, y2 = min(x), max(x), min(y), max(y)
		cropped = image[y1:y2, x1:x2]
		return cropped

