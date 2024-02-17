# importing dependencies
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

# Initialize video capture object
cap = cv2.VideoCapture(0)

# Initialize FaceMeshDetector object
detector = FaceMeshDetector(maxFaces=1)

# Initialize LivePlot object for plotting
plotY = LivePlot(640, 360, [20, 50], invert=True)

# List of facial landmark points corresponding to the eyes
idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]

# List to store vertical-to-horizontal eye opening ratios
ratioList = []

# Counter for blinking
blinkCounter = 0

# Counter for changing color of drawn circles
counter = 0

# Initial color for drawing circles
color = (255, 0, 255)

# Main loop to read frames from the camera
while True:
    # Check if the video has reached its end, reset if true
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Read frame from the camera
    success, img = cap.read()

    # Find facial landmarks in the frame
    img, faces = detector.findFaceMesh(img, draw=False)

    # If facial landmarks are found
    if faces:
        face = faces[0]

        # Draw circles on specific facial landmark points
        for id in idList:
            cv2.circle(img, face[id], 5, color, cv2.FILLED)

        # Calculate the length of vertical and horizontal eye opening
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lengthVer, _ = detector.findDistance(leftUp, leftDown)
        lengthHor, _ = detector.findDistance(leftLeft, leftRight)

        # Draw lines to show eye opening direction
        cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
        cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)

        # Calculate and update the vertical-to-horizontal eye opening ratio
        ratio = int((lengthVer / lengthHor) * 100)
        ratioList.append(ratio)

        # Keep only the last 3 ratios for averaging
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        # Check if a blink is detected
        if ratioAvg < 35 and counter == 0:
            blinkCounter += 1
            color = (0, 200, 0)
            counter = 1

        # Reset counter after blink
        if counter != 0:
            counter += 1

            if counter > 10:
                counter = 0
                color = (255, 0, 255)

        # Display blink count
        cvzone.putTextRect(img, f'Blinking Count: {blinkCounter}', (50, 100), colorR=color)

        # Update LivePlot object with the ratio average
        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
    
    # If no facial landmarks are found, duplicate the frame
    else:
        img = cv2.resize(img, (640, 360))
        imgStack = cvzone.stackImages([img, img], 2, 1)

    # Display the frame
    cv2.imshow("IMAGE", imgStack)
    cv2.waitKey(25)