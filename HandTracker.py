import cv2
import mediapipe as mp


class HandDetectionModule():
    def __init__(self, static_mode=False, max_Hands=2, detection_Confidence=0.5, tracking_Confidence=0.5):
        self.static_mode = static_mode
        self.max_Hands = max_Hands
        self.detection_Confidence = detection_Confidence
        self.tracking_Confidence = tracking_Confidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=static_mode, max_num_hands=max_Hands, model_complexity=1,
                                        min_detection_confidence=detection_Confidence,
                                        min_tracking_confidence=tracking_Confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_landmarks, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img):
        landmarks_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[0]

            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks_list.append([id, cx, cy])
        if len(landmarks_list) != 0:
            if landmarks_list[8][2] < landmarks_list[7][2] and landmarks_list[12][2] > landmarks_list[11][2]:
                cv2.circle(img, (landmarks_list[8][1], landmarks_list[8][2]), 10, (255, 10, 10), cv2.FILLED)
            # if (landmarks_list[8][2] < landmarks_list[7][2]) and landmarks_list[12][2] < landmarks_list[11][2]:
            #     cv2.rectangle(img, (landmarks_list[8][1], landmarks_list[8][2]),
            #                   (landmarks_list[12][1], landmarks_list[12][2]), (0, 0, 255), cv2.FILLED)
        return landmarks_list


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetectionModule(detection_Confidence=0.8)

    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        cv2.imshow("image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
