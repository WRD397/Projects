from customModules import handDetector
import cv2 as cv
import mediapipe as mp
import numpy as np
import time

def main() -> None:
    
    detectorObj = handDetector()
    detectorObj.showImage(fps=False)

if __name__=='__main__':
    main()