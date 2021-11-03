import cv2
import math
import numpy as np
import os
import pandas as pd
import subprocess
import sys
import time
import tkinter as tk
from gaze_tracking import GazeTracking

# create the root window
root = tk.Tk()
# SCREEN_WIDTH = root.winfo_screenwidth()
# SCREEN_HEIGHT = root.winfo_screenheight()
root.withdraw()

print(f'Initializing calibration.')
start_delay = 3  # seconds
duration = 12000  # milliseconds
print(f'Calibration will start in {start_delay} seconds.')
time.sleep(start_delay)

coords = []
time_results = []
res = 0
contador = 0
temp_ini = time.time()  # tempo que começa o programa
contadorRight = 0
contadorLeft = 0
menor_x = 5000
maior_x = -5000
lista_tempo = []
lista_gaze_x = []
lista_gaze_y = []
# gaze = GazeTracking()
# webcam = cv2.VideoCapture(0)

start_time = time.time()
print('Main loop started.')
x_min = 0
x_max = 0
y_min = 0
y_max = 0


def calibragem():
    print("entrou na função calibragem")
    """
    calibra bla bla
    :return:
    """
    contador = 0
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)

    SCREEN_WIDTH = webcam.get(cv2.CAP_PROP_FRAME_WIDTH)
    SCREEN_HEIGHT = webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()
        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()

        current_time = time.time()
        elapsed_time = current_time - start_time

        ini = time.time()  # inicia tempo dentro do while
        res = ini - temp_ini  # diferença do tempo inicial e o tempo dentro do while
        time_results.append(res)  # colocar res no vetor

        # text = ""
        # if gaze.is_blinking():
        #     text = "Blinking"
        # elif gaze.is_right():
        #     text = "Looking right"
        #     # contadorRight += 1
        # elif gaze.is_left():
        #     text = "Looking left"
        #     # contadorLeft += 1
        # elif gaze.is_center():
        #     text = "Looking center"

        #cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        gaze_x = gaze.horizontal_ratio()
        gaze_y = gaze.vertical_ratio()

        if res >= 0.1:

            contador = contador + 100
            if gaze_x != None and gaze_y != None:

                # +-------------+
                # |             |
                # |             |
                # |             |
                # +-------------+

                if contador < 3000:
                    cv2.putText(frame, "*", (0, int(SCREEN_HEIGHT)), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31),
                                1)  # esq

                elif 3000 <= contador < 6000:
                    print("entrou")
                    cv2.putText(frame, "*", (int(5), int(20)), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)  # cima

                elif 6000 <= contador < 9000:
                    cv2.putText(frame, "*", (int(SCREEN_WIDTH - 15), int(20)), cv2.FONT_HERSHEY_DUPLEX, 0.9,
                                (147, 58, 31), 1)  # di

                elif 9000 <= contador < 12000:
                    cv2.putText(frame, "*", (int(SCREEN_WIDTH - 17), int(SCREEN_HEIGHT)), cv2.FONT_HERSHEY_DUPLEX, 0.9,
                                (147, 58, 31), 1)  # baixo
                else:
                    break

                lista_gaze_x.append(gaze_x)
                lista_gaze_y.append(gaze_y)

                # print(f'x = {gaze_x:.3f} (min = {menor_x:.3f}, max = {maior_x:.3f})\ty = {gaze_y:.3f}')
                print(contador)
                coords.append([pd.Timedelta(milliseconds=contador), gaze_x, gaze_y])

        cv2.imshow("Demo", frame) and elapsed_time > duration
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(f'Main loop finished after {str(int(elapsed_time))} seconds.')
            break

    # ordenar os x de forma crescente
    lista_gaze_x.append(lista_gaze_x.sort())
    lista_gaze_x.pop()

    # pegar 10 primeiros numeros
    menores_x = lista_gaze_x[:10]
    # pegar 10 ultimos numeros
    maiores_x = lista_gaze_x[-10:]

    # x_min = media dos 10 primeiros gaze_x
    x_min = sum(menores_x) / len(menores_x)
    print('X min ', x_min)
    # x_max = media dos 10 ultimos gaze_x
    x_max = sum(maiores_x) / len(maiores_x)
    print('X max ', x_max)

    # print (lista_gaze_x)

    # ordenar os y de forma crescente
    lista_gaze_y.append(lista_gaze_y.sort())
    lista_gaze_y.pop()

    # y_min = media dos 10 primeiros gaze_y
    menores_y = lista_gaze_y[:10]
    # y_max = media dos 10 ultimos gaze_y
    maiores_y = lista_gaze_y[-10:]

    y_min = sum(menores_y) / len(menores_y)
    print('Y min ', y_min)
    # x_max = media dos 10 ultimos gaze_x
    y_max = sum(maiores_y) / len(maiores_y)
    print('Y max ', y_max)

    # return [x_min, x_max, y_min, y_max]


# apenas para testes
if __name__ == '__main__':
    calibragem()