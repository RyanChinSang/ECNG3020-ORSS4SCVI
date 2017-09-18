import cv2

cap = cv2.VideoCapture(0)

# Codec we want to use
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# Specification for the output video file; cv2.VideoWriter([FileName], [Codec], [FPS], [Resolution(h,v)])
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# while cv2.waitKey(1) & 0xFF != ord('q'):
while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    out.write(frame)  # Color Video

    # Gray Video
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray', gray)
    # out.write(gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()  # Stop outputting/recording
cv2.destroyAllWindows()
