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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


"""
def result(Region, Subregion, Station, SubregionText):
    driver.find_elements(By.CLASS_NAME, "tree-li")[RegionNumber[Region]].find_element(
        By.TAG_NAME, "ul").find_elements(
        By.TAG_NAME, "li")[Subregion].find_element(
        By.TAG_NAME, "ul").find_elements(
        By.TAG_NAME, "li")[Station].find_element(
        By.TAG_NAME, "a").click()

    driver.find_element(By.ID, "election-results-name").click()

    driver.get(driver.find_elements(By.CLASS_NAME, 'tdReport')[6].find_element(
        By.TAG_NAME, "a").get_attribute("href"))

    People = driver.find_elements(By.TAG_NAME, 'tbody')[-2].find_elements(
        By.TAG_NAME, 'tr')[0].find_elements(
        By.TAG_NAME, 'td')[2].find_element(
        By.TAG_NAME, 'b').text

    InvalidBallots = driver.find_elements(By.TAG_NAME, 'tbody')[-2].find_elements(
        By.TAG_NAME, 'tr')[8].find_elements(
        By.TAG_NAME, 'td')[2].find_element(
        By.TAG_NAME, 'b').text

    ValidBallots = driver.find_elements(By.TAG_NAME, 'tbody')[-2].find_elements(
        By.TAG_NAME, 'tr')[9].find_elements(
        By.TAG_NAME, 'td')[2].find_element(
        By.TAG_NAME, 'b').text

    Putin = driver.find_elements(By.TAG_NAME, 'tbody')[-2].find_elements(
        By.TAG_NAME, 'tr')[16].find_elements(
        By.TAG_NAME, 'td')[2].find_element(
        By.TAG_NAME, 'b').text

    StationID = driver.find_elements(By.TAG_NAME, 'tbody')[-5].find_element(
        By.TAG_NAME, 'tr').find_elements(
        By.TAG_NAME, 'td')[1].find_element(
        By.TAG_NAME, 'b').text

    Ballots = float(InvalidBallots) + float(ValidBallots)

    Turnout = Ballots / float(People)

    Percentage = float(Putin) / Ballots

    return [Region, SubregionText, StationID, Turnout, Percentage]

def SubregionResult(link, Region, SubregionNumber):

    driver.get(link)

    Subregion = driver.find_elements(
        By.CLASS_NAME, "tree-li")[RegionNumber[Region]].find_element(
        By.TAG_NAME, "ul").find_elements(
        By.TAG_NAME, "li")[SubregionNumber].find_elements(
        By.TAG_NAME, "a")[1]
    print(Subregion.text)

    SubregionText = str(Subregion.text)

    Subregion.click()

    length = len(driver.find_elements(By.CLASS_NAME, "tree-li")[RegionNumber[Region]].find_element(
        By.TAG_NAME, "ul").find_elements(
        By.TAG_NAME, "li")[SubregionNumber].find_element(
        By.TAG_NAME, "ul").find_elements(
        By.TAG_NAME, "li"))
    l = []

    for j in range(length):
        l.append(result(Region, SubregionNumber, j, SubregionText))
    return l

def RegionResult(Region):
    q = []
    d = driver.find_elements(By.CLASS_NAME, "tree-li")
    link = d[RegionNumber[Region]].find_elements(By.TAG_NAME, "a")[1].get_attribute("href")
    driver.get(link)
    length = len(driver.find_elements(
        By.CLASS_NAME, "tree-li")[RegionNumber[Region]].find_element(
        By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li"))
    for i in range(length):
        q = q + SubregionResult(link, Region, i)
    r = pd.DataFrame(q, columns=['Region', 'Subregion', 'StationID', 'Turnout', 'Percentage'])
    return r

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.google.com")
driver.get("http://www.vybory.izbirkom.ru/region/izbirkom?action=show&root=0&tvd=100100084849066&vrn=100100084849062&prver=0&pronetvd=null&region=0&sub_region=0&type=0&report_mode=null")

RegionNumber = dict()
for i in range(1, 88):
    w = str(driver.find_elements(By.CLASS_NAME, "tree-li")[i].find_elements(By.TAG_NAME, "a")[1].text)
    RegionNumber[w] = i
"""
st.title('Визуализация выборов')
"""
Region = st.selectbox('Выберите регион', ['Регион не выбран'] + list(RegionNumber.keys()))
if Region != 'Регион не выбран':
    RegionResults = RegionResult(Region)
    st.write(RegionResults)

    RegionResults.to_csv(f"D:/Miron/{Region}.csv")

    fig1 = ff.create_distplot([RegionResults[a] for a in ['Turnout', 'Percentage']], ['Явка', 'Процент голосов за Путина'], colors=['#63F5EF', '#A6ACEC'], bin_size=.05)
    fig1.update_layout(title_text='Явка и процент голосов за Путина')

    st.write(fig1)

    TurnoutNP = np.array(RegionResults['Turnout'])
    PercentageNP = np.array(RegionResults['Percentage'])

    az.style.use("arviz-darkgrid")

    fig2 = az.plot_kde(
        TurnoutNP, PercentageNP,
        contour_kwargs={"colors": None, "cmap": plt.cm.viridis, "levels": 30},
        contourf_kwargs={"alpha": 0.5, "levels": 30},
    )
"""
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

#fig2 = sns.kdeplot(data=RegionResults, x='Turnout', y='Percentage')

#st.write(sns.FacetGrid(RegionResults, palette="icefire").map(sns.kdeplot, 'Turnout', 'Percentage', fill=True))

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
"""
with open('Адм-территориальные границы РФ в формате GeoJSON/admin_level_8.geojson', encoding='utf-8') as f:
    Subregions = json.load(f)
df = pd.json_normalize(Subregions['features'])[['id', 'name', 'geometry.coordinates']]
df['geometry.coordinates'] = df['geometry.coordinates'].apply(lambda x: Polygon(x[0][0]))
"""

entrypoint = "https://nominatim.openstreetmap.org/search"
params = {'q': set(RegionResults['Subregion']),
          'format': 'geojson'}
r = requests.get(entrypoint, params=params)
st.write(r)
SubregionPoly = geopandas.GeoDataFrame.from_features(r)
st.write(SubregionPoly)
#Poly = go.Figure(df['geometry.coordinates'][5])
#st.plotly_chart(Poly)

