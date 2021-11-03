import calibragem, captura, escalonamento, exibicao

escala = calibragem()
coords = captura(escala)
coords = escalonamento(escala, coords)
exibicao(coords)