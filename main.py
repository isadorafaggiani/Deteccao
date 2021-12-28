import calibragem, captura, escalonamento, exibicao
from pathlib import Path
import json

CACHE_CALIBRAGEM = 'cache/calibragem.json'
CACHE_CAPTURA = 'cache/captura.json'

if __name__ == '__main__':

	# calibragem
	if Path(CACHE_CALIBRAGEM).exists():
		print('Obtendo calibragem do cache...')
		with open(CACHE_CALIBRAGEM, 'r') as f:
			resultado_calibragem = json.load(f)
	else:
		print('Realizando calibragem...')
		resultado_calibragem = calibragem.calibrar()
	escala_webcam = resultado_calibragem[:4]
	resolucao_tela = resultado_calibragem[4:]
	print(f'escala_webcam = {escala_webcam}')
	print(f'resolucao_tela = {resolucao_tela}')

	# captura
	if Path(CACHE_CAPTURA).exists():
		print('Obtendo captura do cache...')
		with open(CACHE_CAPTURA, 'r') as f:
			coords = json.load(f)
	else:
		coords = captura.capturar()
	print(f'coords(cap) = {coords}')

	# escalonamento
	coords = escalonamento.escalonar(escala_webcam, coords)
	print(f'coords(esc) = {coords}')
	coords = escalonamento.escalonar(resolucao_tela, coords)
	print(f'coords(tela) = {coords}')
	
	# exibicao
	exibicao.exibir(coords)
