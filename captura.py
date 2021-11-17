import cv2
import math
import numpy as np
import os
import pandas as pd
import subprocess
import sys
import time
from gaze_tracking import GazeTracking
import seaborn as sns
sns.set_theme()
import plotly.express as px
import plotly.graph_objects as go
import tkinter as tk
from tkinter import filedialog as fd

def get_platform():
    if sys.platform == 'linux':
        try:
            proc_version = open('/proc/version').read()
            if 'Microsoft' in proc_version:
                return 'wsl'
        except:
            pass
    return sys.platform

def open_with_default_app(filename):
    platform = get_platform()
    if platform == 'darwin':
        subprocess.call(('open', filename))
    elif platform in ['win64', 'win32']:
        os.startfile(filename.replace('/', '\\'))
    elif platform == 'wsl':
        subprocess.call('cmd.exe /C start'.split() + [filename])
    else:                                   # linux variants
        subprocess.call(('xdg-open', filename))

def get_video_duration(filename):
    # create video capture object
    data = cv2.VideoCapture(filename)
    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(data.get(cv2.CAP_PROP_FPS))
    # calculate duration of the video
    seconds = int(math.ceil(frames / fps))
    return seconds

def capturar():
    # create the root window
    root = tk.Tk()
    SCREEN_WIDTH = root.winfo_screenwidth()
    SCREEN_HEIGHT = root.winfo_screenheight()
    root.withdraw()
    #print('oi')

    filetypes = (
        ('Arquivos de video', '*.avi *.mov *.mp4 *.mpeg *.mpg'),
        ('Todos os arquivos', '*.*')
    )

    filename = fd.askopenfilename(
        title='Abrir um arquivo',
        initialdir='/',
        filetypes=filetypes)

    print(f'Initializing gaze tracking.')
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)

    start_delay = 3 # seconds
    print(f'Video will start in {start_delay} seconds.')
    time.sleep(start_delay)
    open_with_default_app(filename)
    cv2.setWindowProperty(filename, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    duration = get_video_duration(filename)

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

    start_time = time.time()
    print('Main loop started.')

    while True:

        current_time = time.time()
        elapsed_time = current_time - start_time

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


        if res >= 0.1:
            contador = contador + 100
            if gaze_x != None and gaze_y != None:
                if gaze_x < menor_x:
                    menor_x = gaze_x

                if gaze_x > maior_x:
                    maior_x = gaze_x

                lista_tempo.append(pd.Timedelta(milliseconds=contador))
                lista_gaze_x.append(gaze_x)
                lista_gaze_y.append(gaze_y)

                print(f'x = {gaze_x:.3f} (min = {menor_x:.3f}, max = {maior_x:.3f})\ty = {gaze_y:.3f}')
                gaze_x = int(gaze_x * SCREEN_WIDTH)
                gaze_y = int(gaze_y * SCREEN_HEIGHT)
                coords.append([pd.Timedelta(milliseconds=contador), gaze_x, gaze_y])

            if elapsed_time > duration:
                print(f'Main loop finished after {str(int(elapsed_time))} seconds.')
                break

    return coords