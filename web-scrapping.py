import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv



def result(Region, Subregion, Station, SubregionText):
    driver.find_elements(By.CLASS_NAME, "tree-li")[RegionNumber[Region]].find_element(
        By.TAG_NAME, "ul").find_elements(
        By.TAG_NAME, "li")[Subregion].find_element(
        By.TAG_NAME, "ul").find_elements(
        By.TAG_NAME, "li")[Station].find_element(
        By.TAG_NAME, "a").click()

    driver.find_element(By.ID, "election-results-name").click()

    driver.get(driver.find_elements(By.CLASS_NAME, 'tdReport')[-1].find_element(
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

Region = str(input())
RegionResults = RegionResult(Region)
print(RegionResults)
#RegionResults.to_csv(f"D:/Miron/{Region}.csv")
