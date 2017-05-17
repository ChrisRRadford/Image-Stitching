//g++ `pkg-config --cflags --libs opencv` KeyPoints.cpp -o KeyPoints
//./KeyPoints /Users/chrisradford/Documents/Research/ImagesToPass/Stitch2/_001.jpg /Users/chrisradford/Documents/Research/ImagesToPass/Stitch2/_002.jpg

#include <stdio.h>
#include <iostream>
#include <locale>
#include "opencv2/core.hpp"
#include "opencv2/features2d.hpp"
#include "opencv2/xfeatures2d.hpp"
#include "opencv2/highgui.hpp"

using namespace cv;
using namespace cv::xfeatures2d;

void readme(); 

/** @function main */
int main( int argc, char** argv )
{
  if( argc != 3 )
    { readme(); return -1; }

  Mat image1 = imread( argv[1],1);
  Mat image2 = imread( argv[2],1);
  if( !img_1.data || !img_2.data ){ 
    std::cout<< " --(!) Error reading images " << std::endl; return -1; }
  String featureDetection = argv[3];


}
  //if( !img_1.data || !img_2.data )
  //{ std::cout<< " --(!) Error reading images " << std::endl; return -1; }

int KeyPointDescriptor(mat image, string featureDetection){
  cvtColor(image,image,COLOR_BGR2GRAY);
  int minHessian = 400;
  if(featureDetection == "surf"){
    //-- Step 1: Detect the keypoints using SURF Detector
    Ptr<SURF> detector = SURF::create(minHessian);
    std::vector<KeyPoint> keypoints;
    detector->detect(image, keypoints); 
  }
  else{
    std::cout<< " --(!) Error: unspecified keypoint descriptor " << std::endl; return ; 
  }
}
  
  //-- Step 1: Detect the keypoints using SURF Detector
  

  //-- Show detected (drawn) keypoints
  imshow("Keypoints 1", img_keypoints_1 );
  imshow("Keypoints 2", img_keypoints_2 );

  waitKey(0);

  return 0;


  /** @function readme */
void readme()
{ std::cout << " Usage: ./SURF_detector <img1> <img2>" << std::endl; }