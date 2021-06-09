import time
import cv2
import datetime
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from gaze_tracking import GazeTracking
import seaborn as sns; sns.set_theme()
import tkinter
from tkinter import *

root =Tk()
root.title ('EYE TRACKING')
root.geometry ('300x200')
root.configure(background= "#BDE8EF")

var = False

def botao():
    global var
    var = True
    root.quit()

start_btnRedondo = PhotoImage(file='button.png' )
img_label = Button (image = start_btnRedondo, background= "#BDE8EF", borderwidth = 0, command = botao)
img_label.pack (pady = 30)
root.mainloop()

coords = []

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

time_results = []
res = 0
contador = 0
temp_ini = time.time()  # tempo que começa o programa

if var == True:
    while True:

        ini = time.time()  # inicia tempo dentro do while
        res = ini - temp_ini  # diferença do tempo inicial e o tempo dentro do while
        time_results.append(res)  # colocar res no vetor
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9,
                    (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9,
                    (147, 58, 31), 1)
        if res >= 0.2:
            contador = contador + 200
            if left_pupil != None and right_pupil != None:
                coords.append([pd.Timedelta(milliseconds=contador), left_pupil[0], left_pupil[1], right_pupil[0],
                               right_pupil[1]])
            else:
                print(f'valor nulo detectado -> esq:{left_pupil}\tdir:{right_pupil}')
            temp_ini = ini
            print(f'contador: {contador}')
        print(f'res:{res} temp_ini:{temp_ini} ini:{ini}')
        cv2.imshow("Demo", frame)

        if cv2.waitKey(1) == 27:
            break
        # time.sleep (1)#delay de 1s

    # prepare data to be saved
    df = pd.DataFrame(coords, columns=['time', 'left_pupil_x', 'left_pupil_y', 'right_pupil_x', 'right_pupil_y'])
    # df = pd.DataFrame(time_results, columns= ['tempo'])

    # save data to filesystem
    # df.to_csv('coords.csv', index=False)

    colors = np.random.rand(len(df.index))

    # uniform_data = np.random.rand(10,12)
    # ax = sns.heatmap(uniform_data, center = 0)
    # df = sns.load_dataset('df')
    # df = df.pivot('left_pupil', 'time','temp')
    # ax = sns.heatmap(df)

    # uniform_data = np.random.rand(10, 12)
    # ax = sns.heatmap(uniform_data, vmin=0, vmax=1)
    # plt.scatter(df['left_pupil_x'], df['left_pupil_y'], c=colors, alpha=0.5)
    # plt.title('left_pupil')
    # plt.show()

    df = pd.read_csv('coords.csv')

    import plotly.express as px

    fig = px.density_heatmap(df, x="left_pupil_x", y="left_pupil_x")
    fig.show()

    fig = px.density_heatmap(df, x="right_pupil_x", y="right_pupil_y")
    fig.show()

else :
    print("nao roda")



