import cv2

# Select the capturing device/webcam installed on your system
cap = cv2.VideoCapture(0)

# while cv2.waitKey(1) & 0xFF != ord('q'):
while True:
    ret, frame = cap.read()

    # Convert normal video feed into gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
