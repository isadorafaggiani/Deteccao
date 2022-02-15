import cv2
import numpy as np
import time
from gaze_tracking import GazeTracking
import json
import tkinter

def obter_resolucao_tela():
    root = tkinter.Tk()
    root.withdraw()
    return root.winfo_screenwidth(), root.winfo_screenheight()

def capturar_cantos_webcam():
    print(f'entrou no metodo capturar_cantos()')
	
    print(f'Initializing calibration.')
    start_delay = 3  # seconds
    print(f'Calibration will start in {start_delay} seconds.')
    time.sleep(start_delay)

    time_delta = 0
    elapsed_time = 0
    temp_ini = time.time()  # tempo que começa o programa
    start_time = time.time()
    print('Main loop started.')

    window_name = "Gaze Tracking"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, 0, 0)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    lista_gaze_x = []
    lista_gaze_y = []
    elapsed_time = 0
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)

    WEBCAM_WIDTH = int(webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
    WEBCAM_HEIGHT = int(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f'WEBCAM_WIDTH = {WEBCAM_WIDTH}, WEBCAM_HEIGHT = {WEBCAM_HEIGHT}')
    blank_image = np.zeros((WEBCAM_HEIGHT,WEBCAM_WIDTH,3), dtype=np.uint8) + 255

    curr_pos = 'nenhuma'
    start_time = time.time()  # inicia tempo dentro do while
    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()
        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        current_time = time.time()
        elapsed_time = current_time - start_time

        gaze_x = gaze.horizontal_ratio()
        gaze_y = gaze.vertical_ratio()

        if gaze_x != None and gaze_y != None:

            # +------C------+
            # |             |
            # E             D
            # |             |
            # +------B------+

            last_pos = curr_pos
            if elapsed_time < 3.0:
                curr_pos = 'esquerda'
            elif 3.0 <= elapsed_time < 6.0:
                curr_pos = 'cima'
            elif 6.0 <= elapsed_time < 9.0:
                curr_pos = 'direita'
            elif 9.0 <= elapsed_time < 12.0:
                curr_pos = 'baixo'
            else:
                print(f'Main loop finished after {str(int(elapsed_time))} seconds.')
                break

            if curr_pos != last_pos:
                print(f'desenhando')
                cv2.imshow(window_name, cv2.imread(f'./assets/img_{curr_pos}.png'))

            print(f'elapsed_time = {elapsed_time} last_pos = {last_pos} curr_pos = {curr_pos}')

            lista_gaze_x.append(gaze_x)
            lista_gaze_y.append(gaze_y)
            
            time.sleep(0.1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(f'Main loop finished after {str(int(elapsed_time))} seconds.')
            break

    webcam.release()
    cv2.destroyAllWindows()

    return lista_gaze_x,lista_gaze_y

def obter_limites_webcam(vet,qtd=3):
    print(f'entrou no metodo obter_limites()')
    # ordenar o vetor de forma crescente
    vet.sort()
    # filtra o vetor removendo valores invalidos
    vet_filtered = [i for i in vet if i != None]
    # min = media dos 'qtd' primeiros valores
    v_min = np.mean(vet_filtered[:qtd])
    print(f'v_minimo = {v_min}')
    # max = media dos 'qtd' ultimos valores
    v_max = np.mean(vet_filtered[-qtd:])
    print(f'v_maximo = {v_max}')
    return v_min,v_max

def calibrar():
    print(f'entrou no metodo calibragem()')
    lista_gaze_x,lista_gaze_y = capturar_cantos_webcam()
    x_min,x_max = obter_limites_webcam(lista_gaze_x)
    y_min,y_max = obter_limites_webcam(lista_gaze_y)
    width,height = obter_resolucao_tela()
    ans = x_min,x_max,y_min,y_max,0,width,0,height
    with open("cache/calibragem.json", 'w') as f:
        json.dump(ans, f, indent=2)
    return ans
