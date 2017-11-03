from BETA.TestCode.OpenCV.VidCap import VideoStream
import cv2

cap = VideoStream(src=0).start()
# cap = cv2.VideoCapture(0)

while 1:
    frame = cap.read()
    # _, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.stop()
# cap.release()
cv2.destroyAllWindows()
