import cv2
import numpy as np
import webcolors
import pyttsx3
import multiprocessing as mp
# from threading import Thread


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
        # engine.say(str(min_colours[min(min_colours.keys())]))
        # engine.runAndWait()
    return min_colours[min(min_colours.keys())]


# def say(str):
#     engine.say(str)
#     engine.runAndWait()


engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].__dict__.get('id'))
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
img = np.zeros((200, 200, 3), np.uint8)
size = 20


def loop_a():
    cap = cv2.VideoCapture(0)
    while 1:
        _, frame = cap.read()
        cv2.rectangle(img=frame,
                      pt1=(int((cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2) - (size + 1)),
                           int((cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2) - (size + 1))),
                      pt2=(int((cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2) + (size + 1)),
                           int((cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2) + (size + 1))),
                      color=(255, 255, 255),
                      thickness=2,
                      lineType=cv2.LINE_AA,
                      shift=0)
        r = 0
        g = 0
        b = 0
        for x in range(size * 2):
            for y in range(size * 2):
                b += frame[int((cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2) - size) + x][
                    int((cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2) - size) + y][0]
                g += frame[int((cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2) - size) + x][
                    int((cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2) - size) + y][1]
                r += frame[int((cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2) - size) + x][
                    int((cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2) - size) + y][2]
        avg = np.array(
            [int(round(r / ((size * 2) ** 2))), int(round(g / ((size * 2) ** 2))), int(round(b / ((size * 2) ** 2)))])
        img[:] = [avg[0], avg[1], avg[2]]
        color = closest_colour(avg)
        cv2.putText(img=img,
                    text="{}".format(color),
                    org=(0, 15),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(255, 255, 255),
                    thickness=1,
                    lineType=cv2.LINE_AA,
                    bottomLeftOrigin=False
                    )
        cv2.imshow('frame', frame)
        cv2.imshow("avg", img)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            # Thread(target=loop_b(str(closest_colour(avg))), daemon=True).start()
            mp.Process(target=loop_b(color)).start()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break


def loop_b(strg):
    engine.say(strg)
    # engine.runAndWait()


if __name__ == '__main__':
    mp.set_start_method('spawn')
    mp.Process(target=loop_a).start()
