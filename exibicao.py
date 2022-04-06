import numpy as np
import pandas as pd
import seaborn as sns
sns.set_theme()
import plotly.express as px
import plotly.graph_objects as go
import tkinter as tk
from tkinter import filedialog as fd
from datetime import datetime, timedelta
from scipy.stats import iqr

def freedman_diaconis_rule(data_x,data_y):

    bin_width_x = 2.0 * iqr(data_x) / np.power(len(data_x), 1.0/3.0)
    bin_count_x = int(np.ceil((np.max(data_x) - np.min(data_x)) / bin_width_x))
    # print(f'bin_width_x = {bin_width_x}\tbin_count_x = {bin_count_x}')

    bin_width_y = 2.0 * iqr(data_y) / np.power(len(data_y), 1.0/3.0)
    bin_count_y = int(np.ceil((np.max(data_y) - np.min(data_y)) / bin_width_y))
    # print(f'bin_width_y = {bin_width_y}\tbin_count_y = {bin_count_y}')

    return bin_count_x,bin_count_y

def exibir(coords):


    data_x,data_y = [v[1] for v in coords],[v[2] for v in coords]
    bin_count_x,bin_count_y = freedman_diaconis_rule(data_x,data_y)
    fig = px.density_heatmap(coords, x=data_x, y=data_y, nbinsx=bin_count_x, nbinsy=bin_count_y)
   
    fig.add_traces(go.Scatter(
        x=[610,875],y=[610,625],mode="markers", marker=dict(color='LightSkyBlue', size=20), name="Ground Truth", hoverinfo="skip")
    )
    fig.show()

    #print('Showing pizza plot.')
    #labels = ['Left_Gaze', 'Right_Gaze']
    #values = [contadorLeft, contadorRight]
    #fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    #fig.show()
