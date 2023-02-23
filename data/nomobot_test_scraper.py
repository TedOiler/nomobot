from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from datetime import date
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def run_selenium_cycle(data: pd.DataFrame) -> pd.DataFrame:
    # op = webdriver.ChromeOptions()
    # op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # op.add_argument("--headless")
    # op.add_argument("--no-sandbox")
    # op.add_argument("--disable-dev-sh-usage")
    # browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)

    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.get("https://extapps.solon.gov.gr/mojwp/faces/TrackLdoPublic")
    data_out = []
    for _, row in data.iterrows():
        court = browser.find_element(By.XPATH, '//*[@id="courtOfficeOC::content"]')
        court.send_keys(Keys.COMMAND + 'a' + Keys.DELETE)
        # court.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
        court.send_keys(str(row['Court']) + Keys.RETURN)
        time.sleep(1)
        gak = browser.find_element(By.XPATH, '//*[@id="it1::content"]')
        gak.send_keys(Keys.COMMAND + 'a' + Keys.DELETE)
        # gak.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
        gak.send_keys(str(row['GAK']) + Keys.RETURN)
        time.sleep(1)
        year = browser.find_element(By.XPATH, '//*[@id="it2::content"]')
        year.send_keys(Keys.COMMAND + 'a' + Keys.DELETE)
        # year.send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
        year.send_keys(str(row['Year']) + Keys.RETURN)
        time.sleep(2)
        browser.find_element(By.XPATH, '//*[@id="ldoSearch"]/a/span').click()

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                         '#pc1\:ldoTable\:\:db > table > tbody > tr > td:nth-child(2) > div > table > tbody > tr > td:nth-child(7)')))
        condition = True
        while condition:
            try:
                time.sleep(15)
                scraped_number = browser.find_element(By.CSS_SELECTOR,
                                                      '#pc1\:ldoTable\:\:db > table > tbody > tr > td:nth-child(2) > div > table > tbody > tr > td:nth-child(1)')
                time.sleep(1)
                result = browser.find_element(By.CSS_SELECTOR,
                                              '#pc1\:ldoTable\:\:db > table > tbody > tr > td:nth-child(2) > div > table > tbody > tr > td:nth-child(7)')
                condition = False
            except:
                time.sleep(10)

        data_out.append([row['Court'], row['GAK'], row['Year'], scraped_number.text, result.text, date.today()])
        # browser.execute_script("location.reload()")
        # browser.get("https://extapps.solon.gov.gr/mojwp/faces/TrackLdoPublic")
    data_out_df = pd.DataFrame(data_out, columns=['Court', 'GAK', 'Year', 'Scraped_GAK', 'Result', 'Date'])
    # data_out_df.to_csv('./data/data_out.csv', index=False)
    time.sleep(1)
    browser.quit()
    return data_out_df
