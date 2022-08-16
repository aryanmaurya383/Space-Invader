import cv2
import mediapipe as mp  # the module by google storing information of recognizing hands
import time
import pyautogui

pyautogui.FAILSAFE = False


# we are storing the code systematically sp that we can use it in any project


class handDetector():
    def __init__(self, mode=False, max_hands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands  # mp recognises hand by 21 landmarks on hands

        # arguments of the following Hands() are: static img mode ie detects if confidence is low
        # otherwise just tracks(default =False), max_num_hands, min_detection_confidence,
        # ,min_tracking_confidence
        self.hands = self.mpHands.Hands(
            self.mode, self.max_hands, self.modelComplexity, self.detectionCon, self.trackCon)

        # used to connect all those landmarks as per wish
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        img = cv2.flip(img, 1)

        # because hands class only uses RGB not BGR
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # print(results.multi_hand_landmarks)
        # checking if multiple hands and using them on bye one
        if (self.results.multi_hand_landmarks):
            for handLms in self.results.multi_hand_landmarks:
                # getting index info of each point
                # draws the 21 points on hand and HAND_CONNECTIONS connects all of them with a straight line
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):  # to get the position of points

        lmList = []  # will contain all the landmark positions
        if (self.results.multi_hand_landmarks):
            # to which hand info to show
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):

                # print(id, lm)
                # the output is in decimals and not in pixel, so we multiply right width amd channels to
                # get in pixels
                h, w, c = img.shape
                # centre of x and centre of y
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 255, 0), cv2.FILLED)
        return lmList


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        lmList = detector.findPosition(img)
        # if (len(lmList) != 0):
        #     pyautogui.moveTo(((lmList[8][1]) %
        #                       1918, (lmList[8][2]) % 1078))
        # if (abs(lmList[8][2] - lmList[12][2]) < 40):
        # pyautogui.click()
        # print(lmList[8])
        # print(lmList[12])

        cTime = time.time()

        if cTime == pTime:
            fps = 1 / (cTime + 0.0001 - pTime)
        else:
            fps = 1 / (cTime - pTime)

        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), thickness=3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
