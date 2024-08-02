import cv2
import pickle
import cvzone
import numpy as np
import pyttsx3  # Import the pyttsx3 library

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Video feed
cap = cv2.VideoCapture('../data/carPark.mp4')

with open('../data/CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48
spaceCounter = 0  # Initialize spaceCounter

def checkParkingSpace(imgPro):
    global spaceCounter
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=5, offset=20, colorR=(0,200,0))

def announce_space():
    announcement = f"Free spaces for parking car is : {spaceCounter}"
    print(announcement)  # Print to console
    engine.say(announcement)  # Convert text to speech
    engine.runAndWait()  # Wait until the speech is finished

def mouseClick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        announce_space()

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouseClick)

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    success, img = cap.read()
    if not success:
        break
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    
    cv2.imshow("Image", img)
    
    key = cv2.waitKey(10)
    if key == 27:  # ESC key to exit
        break

cv2.destroyAllWindows()
cap.release()
