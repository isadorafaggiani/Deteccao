# Eye Tracking 
Diretório destinado ao projeto da Iniciação Científica "Eye Tracking para auxiliar no diagnóstico de crianças com TEA".

## Descrição
O objetivo do projeto é auxilar no diagnosticos de crianças por meio do rastreamento e obtenção de dados da pupila do paciente, uma vez que o programa fornece um ** sistema de rastreamento ocular baseado em webcam ** e com isso é posível dar a posição exata das pupilas e a direção do olhar em tempo real. 

O projeto está sendo desenvolvindo na linguagem Python.

## Funcionalidades
A aplicação conta com algumas funcionalidades já implementadas:
- [x] Uso de um botão para auxiliar no funcionamento do programa.
- [x] Obtenção das coordenadas na pupila.
- [x] Analise de dados por meio de gráficos (Heapmap).
- [x] Analise de dados por meio de tabela.


## Instalação

Clone o projeto:

```
https://github.com/isadorafaggiani/Deteccao.git
```

Instale as dependências (NumPy, OpenCV, Dlib):

```
pip install -r requirements.txt
```


Run:

```
python example.py
```

## Projeto na forma basica

```python
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    _, frame = webcam.read()
    gaze.refresh(frame)

    new_frame = gaze.annotated_frame()
    text = ""

    if gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
    cv2.imshow("Demo", new_frame)

    if cv2.waitKey(1) == 27:
        break
```

## Documentação

Alguns exemplos são encontrados na classe "GazeTracking". Lá é possível compreender melhor o funcionamento do código.

### Posição da pupila esquerda

```python
gaze.pupil_left_coords()
```

Retorna as coodenadas (x,y) da pupila esquerda.

### Posição da pupila direita

```python
gaze.pupil_right_coords()
```

Retorna as coodenadas (x,y) da pupila direita.

### Looking to the left (Olhando para a esqueda)

```python
gaze.is_left()
```

Retorna `True` se a pessoa estiver olhando para a esqueda.

### Looking to the right (Olhando para a direita)

```python
gaze.is_right()
```

Retorna `True` se a pessoa estiver olhando para a direita.

### Looking at the center (Olhando para o centro)

```python
gaze.is_center()
```

Retorna `True` se a pessoa estiver olhando para o centro.

### Direção horizontal do Eye Tracking

```python
ratio = gaze.horizontal_ratio()
```

Retorna um número entre 0,0 e 1,0 que indica a direção horizontal do olhar. A extrema direita é 0,0, o centro é 0,5 e a extrema esquerda é 1,0.

### Direção vertical do Eye Tracking

```python
ratio = gaze.vertical_ratio()
```

Retorna um número entre 0,0 e 1,0 que indica a direção vertical do olhar. O topo extremo é 0,0, o centro é 0,5 e o fundo extremo é 1,0.

### Blinking

```python
gaze.is_blinking()
```

Retorna `True` se a pessoa estiver com os olhos fechados.

### Webcam frame

```python
frame = gaze.annotated_frame()
```

Retorna o frame principal com as pupilas destacadas.
