def exibicao(coords):

	print('Showing heatmap.')
    df = pd.DataFrame(coords, columns=['time', 'gaze_x', 'gaze_y'])
    colors = np.random.rand(len(coords))
    fig = px.density_heatmap(df, x="gaze_x", y="gaze_y", nbinsx=50, nbinsy=50)
    fig.show()

    print('Showing pizza plot.')
    labels = ['Left_Gaze', 'Right_Gaze']
    values = [contadorLeft, contadorRight]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.show()