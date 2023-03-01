from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from datetime import date
import pandas as pd


def run_selenium_cycle(data: pd.DataFrame) -> pd.DataFrame:
    def get_driver():
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=op)

    op = Options()
    # op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-sh-usage")
    browser = get_driver()
    # browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)
    # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    browser.get("https://extapps.solon.gov.gr/mojwp/faces/TrackLdoPublic")
    data_out = []
    for iteration, row in data.iterrows():
        court = browser.find_element(By.XPATH, '//*[@id="courtOfficeOC::content"]')
        # court.send_keys(Keys.COMMAND + 'a' + Keys.DELETE)
        court.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
        court.send_keys(str(row['Court']) + Keys.RETURN)
        time.sleep(1)
        gak = browser.find_element(By.XPATH, '//*[@id="it1::content"]')
        # gak.send_keys(Keys.COMMAND + 'a' + Keys.DELETE)
        gak.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
        gak.send_keys(str(row['GAK']) + Keys.RETURN)
        time.sleep(1)
        year = browser.find_element(By.XPATH, '//*[@id="it2::content"]')
        # year.send_keys(Keys.COMMAND + 'a' + Keys.DELETE)
        year.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
        year.send_keys(str(row['Year']) + Keys.RETURN)
        browser.find_element(By.XPATH, '//*[@id="ldoSearch"]/a/span').click()
        time.sleep(2)
        selector = '#pc1\:ldoTable\:\:db > table > tbody > tr > td:nth-child(2) > div > table > tbody > tr > td:nth-child(1) > span'
        gak_year = str(row['GAK']) + '/' + str(row['Year'])
        WebDriverWait(browser, 30).until(
            lambda browser: browser.find_element(By.CSS_SELECTOR, selector).text == gak_year)

        table_code = browser.find_element(By.CSS_SELECTOR, '#pb2\:\:content')
        scraped_number = browser.find_element(By.CSS_SELECTOR,
                                              '#pc1\:ldoTable\:\:db > table > tbody > tr > td:nth-child(2) > div > table > tbody > tr > td:nth-child(1)').text
        time.sleep(1)

        if iteration == 0:
            columns_xpaths_list = ['//*[@id="pc1:_shwClmc11"]/td[2]',
                                   '//*[@id="pc1:_shwClmc9"]/td[2]',
                                   '//*[@id="pc1:_shwClmc6"]/td[2]',
                                   '//*[@id="pc1:_shwClmc7"]/td[2]']

            for col in columns_xpaths_list:
                browser.find_element(By.XPATH, '//*[@id="pc1:_vw"]/div/table/tbody/tr/td[2]/a').click()
                time.sleep(1)
                browser.find_element(By.XPATH, '//*[@id="pc1:_clmns"]/td[2]').click()
                time.sleep(1)
                WebDriverWait(browser, 30).until(
                    lambda browser: browser.find_element(By.CSS_SELECTOR, selector).text == gak_year)
                browser.find_element(By.XPATH, col).click()
                time.sleep(5)

        time.sleep(3)
        result = browser.find_element(By.CSS_SELECTOR,
                                      '#pc1\:ldoTable\:\:db > table > tbody > tr > td:nth-child(2) > div > table > tbody > tr > td:nth-child(4)').text

        data_out.append([row['Court'], row['GAK'], row['Year'], scraped_number, result, date.today()])
    data_out_df = pd.DataFrame(data_out, columns=['Court', 'GAK', 'Year', 'Scraped_GAK', 'Result', 'Date'])
    # data_out_df.to_csv('./data/data_out.csv', index=False)
    time.sleep(1)
    browser.quit()
    return data_out_df
