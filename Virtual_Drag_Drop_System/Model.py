import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)  # Set height

# Initialize the hand detector
detector = HandDetector(detectionCon=0.8)

# Initial rectangle position and size
cx, cy, w, h = 100, 100, 200, 200
ColorR = (255, 0, 255)  # Default rectangle color

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    if ret:
        # Find hands in the frame
        hands, frame = detector.findHands(frame)

        if hands:
            # Get the landmark list from the first detected hand
            lmlist = hands[0]['lmList']  # Extract landmark positions
            cursor = lmlist[8]  # Index for the tip of the index finger

            # Ensure there are enough landmarks
            if len(lmlist) > 12:  # Ensure landmarks 8 and 12 exist
                point1 = lmlist[8][:2]  # Get coordinates of index finger tip
                point2 = lmlist[12][:2]  # Get coordinates of middle finger tip

                # Calculate distance between index and middle fingers
                distance, _, _ = detector.findDistance(point1, point2, frame)

                # Check if the distance is less than a threshold
                if distance < 30:
                    # Check if the cursor is inside the rectangle
                    if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
                        ColorR = (0, 255, 0)  # Change color to green
                        cx, cy = cursor[0], cursor[1]  # Update rectangle position
                    else:
                        ColorR = (255, 0, 255)  # Reset to default color

                # Display the distance on the frame (optional)
                cv2.putText(frame, f'Distance: {int(distance)}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                            2)

        # Draw the rectangle
        cv2.rectangle(frame, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), ColorR, cv2.FILLED)

        # Display the frame
        cv2.imshow("This is my image", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Failed to capture frame")

# Release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
