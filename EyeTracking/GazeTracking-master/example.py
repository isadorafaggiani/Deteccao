import time
import cv2
#import datetime
import numpy as np
import pandas as pd
#from matplotlib import pyplot as plt
from gaze_tracking import GazeTracking
import seaborn as sns;

sns.set_theme()
#import tkinter
import plotly.express as px
from tkinter import *


root = Tk()
root.title('EYE TRACKING')
root.geometry('300x200')
root.configure(background="#BDE8EF")
# root.withdraw() # verificar se eh necessario
SCREEN_WIDTH, SCREEN_HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
# print(f'SCREEN_WIDTH = {SCREEN_WIDTH}')
# print(f'SCREEN_HEIGHT = {SCREEN_HEIGHT}')

var = False


def botao():
    global var
    var = True
    root.quit()


start_btnRedondo = PhotoImage(file='button.png')
img_label = Button(image=start_btnRedondo, background="#BDE8EF", borderwidth=0, command=botao)
img_label.pack(pady=30)
root.mainloop()

coords = []

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

time_results = []
res = 0
contador = 0
temp_ini = time.time()  # tempo que começa o programa
contadorRight = 0
contadorLeft = 0

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
            contadorRight += 1


        elif gaze.is_left():
            text = "Looking left"
            contadorLeft += 1


        elif gaze.is_center():
            text = "Looking center"

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        gaze_x = gaze.horizontal_ratio()
        gaze_y = gaze.vertical_ratio()

        if res >= 0.2:
            contador = contador + 200
            if gaze_x != None and gaze_y != None:
                gaze_x = int(gaze_x * SCREEN_WIDTH)
                gaze_y = int(gaze_y * SCREEN_HEIGHT)
                cv2.putText(frame, "Coords: " + str(gaze_x) + "," + str(gaze_y), (90, 130), cv2.FONT_HERSHEY_DUPLEX,
                            0.9, (147, 58, 31), 1)
                coords.append([pd.Timedelta(milliseconds=contador), gaze_x, gaze_y])
            else:
                print('valor nulo detectado -> x:{gaze_x}\tdir:{gaze_y}')
            temp_ini = ini
            print('contador: {contador}')
        print('res:{res} temp_ini:{temp_ini} ini:{ini}')
        cv2.imshow("Demo", frame)
        if cv2.waitKey(1) == 27:
            break


    # time.sleep (1)#delay de 1s


    df = pd.DataFrame(coords, columns=['time', 'gaze_x', 'gaze_y'])
    colors = np.random.rand(len(coords))
    fig = px.density_heatmap(df, x="gaze_x", y="gaze_y", nbinsx = 50, nbinsy=50)
    fig.show()

    import plotly.graph_objects  as  go

    labels = ['Left_Gaze', 'Right_Gaze']
    values = [contadorLeft, contadorRight]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.show()

else:
    print("nao roda")