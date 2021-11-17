from sklearn.preprocessing import MinMaxScaler

def escalonamento(escala, coords):

	x_min, x_max, y_min, y_max = escala[0], escala[1], escala[2], escala[3]
	data_x = coords['gaze_x']
	scaler = MinMaxScaler(feature_range=(x_min, x_max))
	data_x = scaler.fit_transform(data_x)

	# repetir o processo para y
	data_y = coords['gaze_y']
	scaler = MinMaxScaler(feature_range=(y_min, y_max))
	data_y = scaler.fit_transform(data_y)

	# repetir oS processoS para o outro olho

	coords['gaze_x'] = data_x
	coords['gaze_y'] = data_y

	return coords