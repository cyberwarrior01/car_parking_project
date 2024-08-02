import cv2
import pickle
import os

width, height = 107, 48
positions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/CarParkPos'))
image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/carParkImg.png'))

# Load or initialize positions list
if os.path.exists(positions_path):
    with open(positions_path, 'rb') as f:
        posList = pickle.load(f)
else:
    posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                break

    with open(positions_path, 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Unable to open image file: {image_path}")

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
