//g++ `pkg-config --cflags --libs opencv` KeyPoints.cpp -o KeyPoints
//./KeyPoints /Users/chrisradford/Documents/Research/ImagesToPass/Stitch2/_001.jpg /Users/chrisradford/Documents/Research/ImagesToPass/Stitch2/_002.jpg

#include <stdio.h>
#include <iostream>
#include <locale>
#include <tuple>
#include <utility>
#include <opencv2/opencv.hpp>
#include "opencv2/core.hpp"
#include "opencv2/features2d.hpp"
#include "opencv2/xfeatures2d.hpp"


using namespace cv;
using namespace cv::xfeatures2d;
using namespace std;

std::tuple<std::vector<KeyPoint>,Mat> KeyPointDescriptor(Mat image, String featureDetection){
  cvtColor(image,image,COLOR_BGR2GRAY);
  int minHessian = 700;
  std::vector<KeyPoint> keypoints;
  Mat descriptor;
  if(featureDetection == "surf"){
  //-- Step 1: Detect the keypoints using SURF Detector
    Ptr<SURF> detector = SURF::create(minHessian);
    detector->detectAndCompute(image,noArray(),keypoints,descriptor);
    return keypoints;
  }
  if(featureDetection == "sift"){
  //-- Step 1: Detect the keypoints using SIFT Detector
    Ptr<SIFT> detector = SIFT::create(minHessian);
    detector->detectAndCompute(image,noArray(),keypoints,descriptor);
    return {keypoints,descriptor};
  }

  return keypoints;
}
/** @function main */
int main( int argc, char** argv )
{
  
  Mat image1 = imread( argv[1],1);
  Mat image2 = imread( argv[2],1);
  std::vector<KeyPoint> kp1, kp2;
  Mat desc1, desc2,img_keypoints_1,img_keypoints_2;
  if( !image1.data || !image2.data ){ 
    std::cout<< " --(!) Error reading images " << std::endl; return -1; }
    String featureDetection = argv[3];
    std::tie(kp1,desc1) = KeyPointDescriptor(image1, featureDetection);
    //std::tie(kp2,desc2) = KeyPointDescriptor(image2, featureDetection);
    

  drawKeypoints( image1, kp1, img_keypoints_1, Scalar::all(-1), DrawMatchesFlags::DEFAULT );
  drawKeypoints( image2, kp2, img_keypoints_2, Scalar::all(-1), DrawMatchesFlags::DEFAULT );
  resize(img_keypoints_1,img_keypoints_1,Size(1200,900));
  //resize(img_keypoints_2,img_keypoints_2,Size(1200,900));

  //-- Show detected (drawn) keypoints
  imshow("Keypoints 1", img_keypoints_1 );
  waitKey(0);
  destroyAllWindows();
  //imshow("Keypoints 2", img_keypoints_2 );
  //waitKey(0);
  //destroyAllWindows();
    

    return 0;
  }
  //if( !img_1.data || !img_2.data )
  //{ std::cout<< " --(!) Error reading images " << std::endl; return -1; }

    

//else{
//  std::cout<< " --(!) Error: unspecified keypoint descriptor " << std::endl; return -1; 
//}