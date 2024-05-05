import cv2 as cv
import mediapipe as mp
import numpy as np
import time
### volume control
from subprocess import call


class handDetector:
    def __init__(self,
                 static_image_mode=False,
                 max_num_hands=2,
                 min_detection_confidence=0.7,
                 min_tracking_confidence=0.5) -> None:
        aspectWidth, aspectHeight = 640, 480
        
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.capture = cv.VideoCapture(0)
        self.capture.set(3,aspectWidth)
        self.capture.set(4,aspectHeight)
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
                    #print(hand_lm)
                    #for id, lm in enumerate(hand_lm.landmark):
                    #    print(id,lm)
            
                    self.mpDrawUtils.draw_landmarks(img, hand_lm, self.mpHands.HAND_CONNECTIONS)

        return img
    
    
    def returnPositions(self, img, handNo) -> None:
        landmarkList = []
        if self.results.multi_hand_landmarks:
            ### Here we are choosing the hand on the basis of the number we provide as an input
            myHand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                height, width, _ = img.shape
                centerX, centerY = int(lm.x * width), int(lm.y * height)
                landmarkList.append([id, centerX, centerY])

        return landmarkList
    

    def calculateLength(self, pointA:tuple, pointB:tuple)-> float:
        x1,y1 = pointA
        x2,y2 = pointB
        dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        return dist


    def audioTweak(self, fingerTipDist:float)->tuple[float, float, float]:
        fingerTipDistanceMax = 200
        fingerTipDistanceMin = 50        
        
        volRangeSystem = [0,100]
        volRangeBar = [400,150]
        volRangePercent = [0,100]

        ## converting the finger tip distance scale onto volRangeSystem
        fingerTipDistConverted = np.interp(fingerTipDist, [fingerTipDistanceMin, fingerTipDistanceMax], volRangeSystem)
        fingerTipDistConvertedBar = np.interp(fingerTipDist, [fingerTipDistanceMin, fingerTipDistanceMax], volRangeBar)
        fingerTipDistConvertedPer = np.interp(fingerTipDist, [fingerTipDistanceMin, fingerTipDistanceMax], volRangePercent)

        #volume.SetMasterVolumeLevel(fingerTipDistConverted, None)
        volume = int(fingerTipDistConverted)
        call(["amixer", "-D", "pulse", "sset", "Master", str(volume)+"%"])

        return fingerTipDistConverted, fingerTipDistConvertedBar, fingerTipDistConvertedPer

    def volControl(self, landmarkList:list[list], img) -> None:
        if len(landmarkList)>0:
            ## putting a volume Bar left side
            cv.rectangle(img, (50, 150), (60, 400), (0,0,0), 3)    

            ## thumb
            x1, y1 = landmarkList[4][1], landmarkList[4][2]
            ## index
            x2, y2 = landmarkList[8][1], landmarkList[8][2]

            ### drawing a circle to mark the two finger-tips of interest
            cv.circle(img, (x1, y1), 10, (255,0,255), cv.FILLED)
            cv.circle(img, (x2, y2), 10, (255,0,255), cv.FILLED)

            ### Line in between two finger tips
            cv.line(img, (x1,y1), (x2,y2), (255,0,255), 3)

            ## Distance of the Line: 
            thumbTip = (x1, y1)
            indexTip = (x2, y2)
            dist = self.calculateLength(pointA=indexTip, pointB=thumbTip)
            print(dist)

            ## Center of the line
            centerLineX, centerLineY = (x1 + x2) // 2 , (y1 + y2) // 2
            if dist < 50 :
                cv.circle(img, (centerLineX, centerLineY), 15, (255,0,0), cv.FILLED)
            else : pass


            ### Tweaking the Volume :
            volDist, barDist, volPer = self.audioTweak(dist)

            ## overlapping the same volume Bar - but filling with Distance value now.
            
            if volPer < 80 :
                cv.rectangle(img, (50, int(barDist)), (60, 400), (50,50,50), cv.FILLED)
                cv.putText(img, str(int(volPer)) + ' %', (40,440), cv.FONT_HERSHEY_COMPLEX,0.5,(20,20,20),2)
            else :
                cv.rectangle(img, (50, int(barDist)), (60, 400), (0,0,255), cv.FILLED)
                cv.putText(img, str(int(volPer)) + ' %', (40,440), cv.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),2)
            

            print(volDist)

        else: pass

        return None

    
    def showImage(self, fps:bool=True, volControlSwitch:bool=False, handNo:int=0) -> None:
        pastTime=0
        while True:
            img = self.detect()

            if volControlSwitch:
                landmarkList = self.returnPositions(img, handNo)
                self.volControl(landmarkList=landmarkList, img=img)
                
            else : pass

            if fps:
                presentTime = time.time()
                fps = 1/(presentTime - pastTime)
                pastTime = presentTime

                cv.putText(img, str(int(fps)), (10,30), cv.FONT_HERSHEY_COMPLEX,0.5,(80,80,80),1)
            else:pass 


            cv.imshow('handDetection', img)
            cv.waitKey(1)
        
        return None
    





if __name__ == '__main__':
    pass
