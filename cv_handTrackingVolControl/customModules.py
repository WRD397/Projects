import cv2 as cv
import mediapipe as mp
import numpy as np
import time

class handDetector:
    def __init__(self,
                 static_image_mode=False,
                 max_num_hands=2,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5) -> None:
        
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.capture = cv.VideoCapture(0)
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.static_image_mode,
                                        max_num_hands=self.max_num_hands,
                                        min_detection_confidence=self.min_detection_confidence,
                                        min_tracking_confidence = self.min_tracking_confidence
                                        )
        ### mediapipe solution to draw lines between landmarks
        self.mpDrawUtils = mp.solutions.drawing_utils

        return None


    def detect(self) -> callable:
        ret, img = self.capture.read()
        if ret:
            imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            self.results = self.hands.process(imgRGB)

            if self.results.multi_hand_landmarks:
                for hand_lm in self.results.multi_hand_landmarks:
                    print(hand_lm)
                    for id, lm in enumerate(hand_lm.landmark):
                        print(id,lm)
            
                    self.mpDrawUtils.draw_landmarks(img, hand_lm, self.mpHands.HAND_CONNECTIONS)

        return img
    
    def showImage(self, fps:bool=True) -> None:
        pastTime=0
        while True:
            img = self.detect()
            if fps:
                presentTime = time.time()
                fps = 1/(presentTime - pastTime)
                pastTime = presentTime

                cv.putText(img, str(int(fps)), (10,70), cv.FONT_HERSHEY_COMPLEX,3,(255,0,0),3 )
            
            cv.imshow('ada', img)
            cv.waitKey(1)
        
        return None
    

    def returnPositions(self, img, handNo) -> None:
        landmarkList = []
        if self.results.multi_hand_landmarks:
            ### Here we are choosing the hand on the basis of the number we provide as an input
            myHand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand):
                height, width, _ = img.shape
                centerX, centerY = int(lm.x * width), int(lm.y * height)
                landmarkList.append([id, centerX, centerY])

        return landmarkList



if __name__ == '__main__':
    pass
