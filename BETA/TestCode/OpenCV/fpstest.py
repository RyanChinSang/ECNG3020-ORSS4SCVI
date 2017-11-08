import cv2
import datetime
from BETA.TestCode.OpenCV.VidCap import VideoStream


# cap = cv2.VideoCapture(0)
cap = VideoStream().start()
c = 0
# start = datetime.datetime.now()
while 1:
    s = cv2.getTickCount()
    # _, frame = cap.read()
    frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if frame.any():
        c += 1
    # end = datetime.datetime.now()
    # print('{:.2f}'.format(c / (end - start).total_seconds()))
    f = cv2.getTickCount()
    print('{:.2f}'.format(cv2.getTickFrequency()/(f-s)))
    # fps.update()

# print("FPS:{:.2f}".format(fps.fps()))
# end = datetime.datetime.now()
# print('{:.2f}'.format(c / (end - start).total_seconds()))
# cap.release()
cap.stop()
cv2.destroyAllWindows()
