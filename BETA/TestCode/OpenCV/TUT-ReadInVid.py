import cv2

# Select the capturing device/webcam installed on your system
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    # Convert normal video feed into gray
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', frame)
    # cv2.imshow('gray', gray)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

cap.release()  # Stop capturing from device
cv2.destroyAllWindows()
