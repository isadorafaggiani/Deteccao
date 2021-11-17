import calibragem, captura #, escalonamento, exibicao
from pathlib import Path
import json

CACHE_CALIBRAGEM = 'cache/calibragem.json'

if __name__ == '__main__':

	# calibragem
	if Path(CACHE_CALIBRAGEM).exists():
		print('Obtendo calibragem do cache...')
		with open(CACHE_CALIBRAGEM, 'r') as f:
			escala = json.load(f)
	else:
		print('Realizando calibragem...')
		escala = calibragem.calibrar()
	print(f'escala = {escala}')

	# captura
	coords = captura.capturar()
	print(f'coords = {coords}')

	#coords = escalonamento(escala, coords)
	
	#exibicao(coords)