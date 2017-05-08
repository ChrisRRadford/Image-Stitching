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

	def stitch(self,imgSet,showMatches,keypoints,descriptors,featureDetection): 
		#Base Case[2]
		if keypoints == []:
			first,second = imgSet
			#detect keypoints in each image
			descriptorType = "SIFT"
			(kp1,desc1) = self.keypointDescriptor(first,featureDetection)
			(kp2,desc2) = self.keypointDescriptor(second,featureDetection)
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
			#print("keypoints")
			#print(keypoints)
			#rint("matches")
			#print(matches)
			# if asked to draw the matches between images
			if showMatches:
				self.drawMatches(first,kp1,second,kp2,matches)
			

			#Base Case[3:n]
		else:
			first,second = imgSet
			#detect keypoints in each image
			(kp,desc) = self.keypointDescriptor(second,featureDetection)
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
		"""------------------------------------------
FUNCTION:	Detects and describes keypoints and their corresponding
			descriptor
ARGUMENTS:  image of any type - self.keypointDescriptor(image)
RETURNS:    Keypoints and descriptors in tuple form - (kp,desc)
NOTES:      Can modify to use any type of descriptor sush as SIFT, ORB, etc.
----------------------------------------------------"""
	def keypointDescriptor(self,image,featureDetection):
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		#setting the hessian threshold for determining keypoints. 0 Default
		#notworking
		if(featureDetection == "ORB"):
			cv2.ocl.setUseOpenCL(False)
			detector = cv2.ORB_create()
			#(kp, desc) = detector.detectAndCompute(gray, None)
			kp = detector.detect(gray, None)
			kp, desc = detector.compute(gray, kp)
			desc = np.float32(desc)
			cv2.ocl.setUseOpenCL(True)
			return (kp,desc)
		elif(featureDetection == "SURF"):
			detector = cv2.xfeatures2d.SURF_create(1800)
		elif(featureDetection == "SIFT"):
			detector = cv2.xfeatures2d.SIFT_create(1800)
			#not working
		elif(featureDetection == "FAST"):
			detector = cv2.FastFeatureDetector_create()
			kp = detector.detect(gray, None)
			kp, des = detector.compute(gray, kp)
			return (kp,desc)
			#not working
		elif(featureDetection == "STAR"):
			detector = cv2.xfeatures2d.StarDetector_create()
		else:
			print("Not a listed feature dectector: ORB, SIFT, or SURF. Check spelling. Terminating exection")
			exit()

		(kp, desc) = detector.detectAndCompute(gray, None)
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

		#print(goodMatches)
		#good matches found. must have minimum number to compute homgraphy
		if len(goodMatches) > 4:
		    master = np.float32([ kp1[m.queryIdx].pt for m in goodMatches ])
		    new = np.float32([ kp2[m.trainIdx].pt for m in goodMatches ])
		    H, mask = cv2.findHomography(master, new, cv2.RANSAC, 4.0)
		    #cv2.imshow("homography mask",mask)
		    #cv2.waitKey(0)
		    #cv2.destroyAllWindows()
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
		drawing = cv2.resize(drawing,(1200,600))#,fx=0.5,fy=0.5)
		cv2.imshow("matched",drawing)
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
		result = cv2.warpPerspective((image1),homography,blank_image.shape[:2])
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

	def overlay(self,image1,image2, perspective,blank):
		grayed = cv2.cvtColor(perspective,cv2.COLOR_BGR2GRAY)
		(_,thresh) = cv2.threshold(grayed,1,255,cv2.THRESH_BINARY)
		result, contours, _= cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		src1 = np.zeros((blank.shape[1],blank.shape[0]),np.uint8)
		src1[0:image2.shape[0], 0:image2.shape[1]] = 1
		src2 = cv2.drawContours(result, contours,cv2.FILLED,(255,255,255)) 
		"""----
		for x in range(src2.shape[0]):
			for y in range(src2.shape[1]):
				if src2[x,y] == 255:
					src2[x,y] = 1
		----"""
		overlap = src1+src2

		print len(image1.shape)
		print src1.shape[0], src1.shape[1]
		print src2.shape[0], src2.shape[1]

		src1 = cv2.resize(src1,(1200,900))
		src2 = cv2.resize(src2,(1200,900))
		overlap = cv2.resize(overlap,(1200,900))
		cv2.imshow("src1",src1*255)
		cv2.imshow("src2",src2)
		cv2.imshow("overlap",overlap*255)
		cv2.waitKey(0)
		cv2.destroyAllWindows()


