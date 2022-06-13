import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import seaborn as sns
import plotly.express as px
import json
import geojson
import plotly.graph_objs as go
from shapely.geometry import Polygon
import numpy as np
import requests
import geopandas


st.title('Визуализация выборов')

with open('Республика Адыгея (Адыгея).csv', encoding='utf8') as o:
    RegionResults = pd.read_csv(o)
st.write(RegionResults)
fig1 = ff.create_distplot([RegionResults[a] for a in ['Turnout', 'Percentage']],
                          ['Явка', 'Процент голосов за Путина'], colors=['#63F5EF', '#A6ACEC'], bin_size=.05)
fig1.update_layout(title={
        'text': "Явка и процент голосов за Путина",
        'y': 0.9,
        'x': 0.4,
        'xanchor': 'center',
        'yanchor': 'top'})

st.write(fig1)

fig2 = px.scatter(RegionResults, x='Turnout', y='Percentage',
                  color_discrete_sequence=['#A6ACEC'], hover_name='StationID', labels={
                     "Turnout": "Явка",
                     "Percentage": "Процент за Путина",
                     "StationID": "StationID"
                 })
fig2.update_layout(
    title={
        'text': "Диаграмма рассеивания",
        'y': 1,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
st.plotly_chart(fig2)

sns.set_theme(palette="icefire", font="Calibri")
fig3 = sns.kdeplot(data=RegionResults, x='Turnout', y='Percentage', fill=True)
fig3.axes.set_title("Плотность двумерного вектора (график KDE)", fontsize=20)
fig3.set_xlabel("Явка", fontsize=10)
fig3.set_ylabel("Процент за Путина", fontsize=10)

#, height=6
st.pyplot()

entrypoint = "https://nominatim.openstreetmap.org/search"
for i in set(RegionResults['Subregion']):
    params = {'q': i,
              'format': 'geojson'}
    r = requests.get(entrypoint, params=params)
    st.write(r)
    Sub = r.geojson()
    SubregionPoly = geopandas.GeoDataFrame.from_features(Sub)
    st.write(SubregionPoly)

