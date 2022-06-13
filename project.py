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
import geopandas as gpd
from bs4 import BeautifulSoup
import xml
import fiona
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components


st.title('Визуализация аномалий на выборах')
st.write("В данном приложении можно увидеть аномалии на президенстких выборах в России "
         "(а именно, положительную корреляцию явки и процента голосов за Путина, а также отклонения "
         "распределений явки и процента от гауссовского распределения). Данные были получены веб-скреппингом "
         "с сайта Центральной избирательной комиссии. В первой части проекта приводится пример для республики Адыгея в 2018, в "
         "последней - считается регрессия для Ненецкого автономного округа в 2018. Но данный анализ можно применить к любому региону, "
         "используя приложенный код со скреппингом.")
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

st.pyplot()

#Машинное обучение: линейная регрессия

df_2008 = pd.read_csv('Ненецкий автономный округ 2008.csv', encoding='utf-8')
df_2012 = pd.read_csv('Ненецкий автономный округ 2012.csv', encoding='utf-8')
df_2018 = pd.read_csv('Ненецкий автономный округ 2018.csv', encoding='utf-8')

df = pd.concat([df_2008, df_2012, df_2018], keys = [2008, 2012, 2018])
df = df.reset_index(level=[0,1])
df = df.drop(columns = ["level_1", "Unnamed: 0"])
df = df.rename(columns = {"level_0": "Year"})
reg = LinearRegression()
reg.fit(df[["Turnout"]], df["Percentage"])

fig4 = df.plot.scatter(x="Turnout", y="Percentage")
x = pd.DataFrame(dict(Turnout=np.linspace(0, 1)))
plt.plot(x["Turnout"], reg.predict(x), color="C1", lw=2)

st.pyplot()

#Регулярные выражения
df_adv = pd.get_dummies(df, columns = ["Year", "Subregion"], drop_first = True)
years = df_adv.filter(regex=r'^Year*').columns
subregions = df_adv.filter(regex=r'^Subregion*').columns
reg_fe = LinearRegression()
reg_fe.fit(df_adv[["Turnout"] + list(years) + list(subregions)], df_adv["Percentage"])

st.write("Результат оценивания регрессии процента за В.В.Путина на явку по УИКам")
st.write("Коэффициент влияния явки на процент голосов за Путина", reg_fe.coef_[1])
st.write("Константа:", reg_fe.intercept_)

