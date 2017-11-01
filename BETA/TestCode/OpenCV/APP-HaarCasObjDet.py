import cv2
import winsound

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale3(roi_gray, outputRejectLevels=True)
        # eyes = eye_cascade.detectMultiScale2(roi_gray)
        # print(eyes[1], len(eyes[1]))
        # print(eyes[2], len(eyes[2]))
        s = 0
        a = 0
        for i in eyes[2]:
            s = s + i[0]
            a = s/len(eyes[2])
            if a < 0.25:
                frequency = 1500  # Set Frequency To 2500 Hertz
                duration = 1000  # Set Duration To 1000 ms == 1 second
                winsound.Beep(frequency, duration)

        for (ex, ey, ew, eh) in eyes[0]:
            # advance_frame(roi_color, img, eyes[0])
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            # print(rectList)
            # cv2.groupRectangles(rectList, 3, 0.2)
    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
