import calibragem, captura #, escalonamento, exibicao

if __name__ == '__main__':

	escala = calibragem.calibrar()
	print(f'escala = {escala}')

	coords = captura.capturar()
	print(f'coords = {coords}')

	#coords = escalonamento(escala, coords)
	#exibicao(coords)