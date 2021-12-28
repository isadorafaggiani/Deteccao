from sklearn.preprocessing import MinMaxScaler
import numpy as np
from datetime import datetime, timedelta
import json

def default(o):
    if isinstance(o, (timedelta)):
        return o / timedelta(milliseconds=1) # in millis

def escalonar(escala, coords):
    coords = np.array(coords)
    x_min, x_max, y_min, y_max = escala[0], escala[1], escala[2], escala[3]

    print('coords = ', coords)
    data_x = coords[:, 1] #Pega a coluna do número x
    scaler = MinMaxScaler(feature_range=(x_min, x_max))
    data_x = data_x.reshape(-1, 1)#Transforma o array original em duas dimensões pq a função pede
    data_x = scaler.fit_transform(data_x)#Escalona os valores de x para dentro do intervalo
    data_x = data_x[:,0]#Volta o array de duas dimensões pra um array simples
    print(f'DataX:{data_x}')#Mostra a lista de x escalonado

    #TODO: repetir o processo para y
    data_y = coords[:, 2]
    scaler = MinMaxScaler(feature_range=(y_min, y_max))
    data_y = data_y.reshape(-1, 1)#Transforma o array original em duas dimensões pq a função pede
    data_y = scaler.fit_transform(data_y)#Escalona os valores de y para dentro do intervalo
    data_y = data_y[:,0]#Volta o array de duas dimensões pra um array simples
    print(f'DataY:{data_y}')#Mostra a lista de y escalonado
    #data_y = scaler.fit_transform(data_y)

    coords[:, 1] = data_x
    coords[:, 2] = data_y

    with open("cache/escalonamento.json", 'w') as f:
        json.dump(coords.tolist(), f, indent=2)
    return coords