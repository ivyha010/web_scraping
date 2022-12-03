from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import lxml
import time
import calendar
import pandas as pd
import os

def config_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    # Instantiate the Webdriver, and show the executable path of the webdriver you have downloaded
    s = Service('C:\\Users\\Minh Danh\\Downloads\\chromedriver_win32\\chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver


def getData(driver, given_url):
    driver.get(given_url)
    try:
        WebDriverWait(driver, 5).until(lambda s: s.find_element_by_id("tabContainer").is_displayed())
    except TimeoutException:
        print("TimeoutException: Element not found")
        return None
    # Create a parse tree of page sources
    soup = BeautifulSoup(driver.page_source, "lxml")
    # Get the time to fetch data
    current_time = calendar.timegm(time.gmtime())
    # Fetch info: Highlight coin, New listing, Top gainer coin, Top volume coin
    get_hinfo(soup, current_time)
    # Fetch info about All Cryptos: Name, Price, 24h Change, 24 Volume, Market Cap
    get_all_cryptos(soup, current_time)


def get_hinfo(s, ctime):
    for element in s.select("div.css-11mpucz"):
        try:
            title = element.next_element.next.contents[0]
            sub_element = element.select("div.css-yrp9yj")
            all_row = []
            for i in range(0,len(sub_element)):
                sub_cont = sub_element[i].contents
                row = []
                for j in range(0, len(sub_cont)):
                    row.append(sub_cont[j].text)
                all_row.append(row)
            # Save into a csv file:
            df = pd.DataFrame(all_row)
            df.to_csv(os.path.join('./', str(ctime) + '_' + title + '.csv'),index=False, header=False, encoding='utf-8')
        except Exception as e:
            print('Error: ', e)


def get_all_cryptos(s, ctime):
    print()
    all_rows = []
    all_rows.append(['Name', '', 'Price', '24h Change', '24h Volume', 'Market Cap'])
    for element in s.select("div.css-vlibs4"):
        try:
            cont = element.contents[0].contents
            # get coin_id
            cont0 = cont[0].contents
            row = []
            for e in cont0:
                if e.text != '':
                    row.append(e.text)
            # get values
            for i in range(1, len(cont)-1):
                row.append(cont[i].text)
            all_rows.append(row)
        except Exception as e:
            print('Error:', e)
    df = pd.DataFrame(all_rows)
    df.to_csv(os.path.join('./', str(ctime) + '_all_cryptos.csv'),index=False, header=False, encoding='utf-8')


if __name__=="__main__":
    url = "https://www.binance.com/en/markets/coinInfo"
    driver = config_driver()
    getData(driver, url)
    driver.close()