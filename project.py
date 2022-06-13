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

st.write(reg_fe.coef_[1])
st.write(reg_fe.intercept_)


#Граф

moscow = pd.read_csv('город Москва 2018.csv', encoding='utf-8')

net = Network()

for i in set(moscow['Subregion']):
    net.add_node(i)
    RegionNodes = moscow.iloc[moscow.index[moscow['Subregion'] == i].tolist()]['StationID']
    net.add_nodes(RegionNodes)
    net.add_edges(i, RegionNodes)

neighbor_map = net.get_adj_list()

for node in net.nodes:
    node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
    node['value'] = len(neighbor_map[node['id']])
    

fig, ax = plt.subplots()
    pos = nx.kamada_kawai_layout(net)
    nx.draw(net, pos, with_labels=True)
    st.pyplot(fig)

#net.add_nodes(moscow['StationID'])


"""
st.sidebar.title('Choose your favorite Graph')
option=st.sidebar.selectbox('select graph',('Simple','Karate', 'GOT'))
physics=st.sidebar.checkbox('add physics interactivity?')
got.simple_func(physics)

nodes = 
st.network(nodes, edges)
"""
'''
with open("https://www.dropbox.com/s/cgcyo11ua5md9r8/admin_level_8.geojson", encoding = 'utf-8') as f:
    a = json.load(f)
df = pd.json_normalize(a['features'])[['id', 'name', 'geometry.coordinates']]
df['geometry.coordinates'] = df['geometry.coordinates'].apply(lambda x: Polygon(x[0][0]))

st.write(df)
'''

#russia_adm4 = gpd.read_file("admin_level_4.shp", encoding='ISO8859-1')
#russia_adm4 = gpd.read_file("https://drive.google.com/file/d/1is_oe9o6S3EaDf0hyOxzT1_QJGfhaJUX/view?usp=sharing", encoding='CP1251')
#russia_adm4 = gpd.read_file("admin_level_4.shp", encoding='Windows-1251')
#st.write(russia_adm4.crs)
#map4 = russia_adm4.to_crs("ESRI:102012")
#fig4 = map4.plot()
#st.pyplot()

"""
fp = get_data("moscow")
osm = OSM(fp)
boundaries = osm.get_boundaries()
fig4 = boundaries.plot()
st.pyplot()

moscow_center = boundaries[boundaries["name"] == "Центральный административный округ"]
bbox_geom = moscow_center['geometry'].values[0]
osm = OSM(fp, bounding_box=bbox_geom)


entrypoint = "https://nominatim.openstreetmap.org/search"
params = {'state': RegionResults['Region'][0],
          'format': 'xml',
          'polygon_geojson': 1
         }
r = requests.get(entrypoint, params=params)

st.write(r)
st.write(r.text)
soup = BeautifulSoup(r.text, features='xml')
soup1 = soup.find("place").find("Polygon").find("coordinates")
st.write(soup1.prettify())

#RegionJson = r.json()
#RegionPoly = geopandas.GeoDataFrame.from_features(RegionJson)
#st.write(RegionPoly)

for i in set(RegionResults['Subregion']):
    st.write(i)
    j = i
    if str(i[-2:])=='ая':
        j = i[:-2]+'ий'
    st.write(j)
    params = {'q': j,
              'format': 'geojson'}
    r = requests.get(entrypoint, params=params)
    st.write(r)
    st.write(r.text)
    Sub = r.json()
    SubregionPoly = geopandas.GeoDataFrame.from_features(Sub)
    st.write(SubregionPoly)
"""
