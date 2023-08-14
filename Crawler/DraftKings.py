from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
import numpy as np

class DraftKingsScraper:
    def __init__(self):
        chromeOptions = webdriver.ChromeOptions() 
        chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
        chromeOptions.add_argument("--no-sandbox") 
        chromeOptions.add_argument("--disable-setuid-sandbox") 

        chromeOptions.add_argument("--remote-debugging-port=9222")  # this

        chromeOptions.add_argument("--disable-dev-shm-using") 
        chromeOptions.add_argument("--disable-extensions") 
        chromeOptions.add_argument("--disable-gpu") 
        chromeOptions.add_argument("start-maximized") 
        chromeOptions.add_argument("disable-infobars")
        chromeOptions.add_argument(r"user-data-dir=.\cookies\\test") 
        self.driver = webdriver.Chrome(chrome_options=chromeOptions)
        self.encoding = sys.stdout.encoding
        self.table = None
        self.tableRows = None

    def get_table_rows(self, table):
        xpath = table
        self.table = self.driver.find_element(By.XPATH, xpath)
        self.tableRows = self.table.find_elements(By.XPATH, './*')

    def get_info(self, tr):
        moneyPath = f'.//tr[{tr}]/td[3]/div/div/div/div/div[2]/span'
        teamPath = f'.//tr[{tr}]/th/a/div/div[2]/div/span/div/div'
        moneyLine = None
        teamName = None

        try:
            moneyline = self.table.find_element(By.XPATH, moneyPath)
            moneyline_text = moneyline.text.replace("−", "-")
            moneyLine = moneyline_text.encode(self.encoding, errors='replace').decode(self.encoding)
        except:
            moneyline = None

        try: 
            teamName = self.table.find_element(By.XPATH, teamPath).text
        except:
            teamName = None

        return [teamName, moneyLine]


    def create_pairs(self):
        combinedList = []
        divNum = 1

        while True:
            try:
                table = f'//*[@id="root"]/section/section[2]/div[2]/section[2]/section[3]/div/div[2]/div/div/div[4]/div[1]/div/div/div[1]/div/div[2]/div/div/div/div[{divNum}]/table/tbody'
                self.get_table_rows(table)
                teams = []

                for row in range(1, len(self.tableRows) + 1):
                    teams.append(self.get_info(row))

                for x in range(0, len(teams), 2):
                    if x+1 < len(teams):
                        pair = [teams[x], teams[x+1]]
                    else:
                        pair = [teams[x], None]

                    combinedList.append(pair)

                divNum += 1

            except:
                break

        # pairs = np.array(combinedList, dtype=object)
        return combinedList

    def run(self):
        self.driver.get('https://sportsbook.draftkings.com/featured?category=game-lines&subcategory=baseball')
        result = self.create_pairs()
        self.driver.quit()
        return result
