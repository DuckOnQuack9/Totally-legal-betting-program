from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
import numpy as np
import pprint

class DraftKingsScraper:
    def __init__(self):
        chromeOptions = webdriver.ChromeOptions() 
        chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
        # chromeOptions.add_argument("--no-sandbox")
        # chromeOptions.add_argument('--headless')
        chromeOptions.add_argument("--disable-setuid-sandbox") 

        chromeOptions.add_argument("--remote-debugging-port=9222")

        chromeOptions.add_argument("--disable-dev-shm-using") 
        chromeOptions.add_argument("--disable-extensions") 
        chromeOptions.add_argument("--disable-gpu") 
        chromeOptions.add_argument("start-maximized") 
        chromeOptions.add_argument("disable-infobars")
        self.driver = webdriver.Chrome(options=chromeOptions)
        self.encoding = sys.stdout.encoding
        self.table = None
        self.tableRows = None

    # Creates a path for the table that is being crawled
    def get_table_rows(self, tablePath):
        xpath = tablePath
        self.table = self.driver.find_element(By.XPATH, xpath)
        self.tableRows = self.table.find_elements(By.XPATH, './*') #./* means that it will select all the child elements

    # Creates an array of the teamName and moneyLine of a single row
    def get_info(self, tr):
        moneyPath = f'.//tr[{tr}]/td[3]/div/div/div/div/div[2]/span'
        teamPath = f'.//tr[{tr}]/th/a/div/div[2]/div/div/div/div'

        # Complete xpaths for the moneyPath and the teamPath
        # //*[@id="root"]/section/section[2]/div[2]/section[2]/section[3]/div/div[2]/div/div/div[4]/div[1]/div/div/div/div/div[2]/div/div/div/div[1]/table/tbody/tr[1]/th/a/div/div[2]/div/div/div/div
        # //*[@id="root"]/section/section[2]/div[2]/section[2]/section[2]/div/div[2]/div/div/div[4]/div[1]/div/div/div/div/div[2]/div/div/div/div/table/tbody/tr[1]/th/a/div/div[2]/div/div/div/div
        
        moneyLine = None
        teamName = None

        try:
            moneyline = self.table.find_element(By.XPATH, moneyPath)
            # Fixes an error with the - character that they use
            moneyline_text = moneyline.text.replace("−", "-")
            moneyLine = moneyline_text.encode(self.encoding, errors='replace').decode(self.encoding)
        except:
            moneyline = None

        try: 
            teamName = self.table.find_element(By.XPATH, teamPath).text
        except:
            teamName = None

        return [teamName, moneyLine]

    # Populates an array with the return of get_info
    def create_pairs(self):
        combinedList = []
        divNum = 1

        # Run the get_info function until it runs out of rows via throwing an error
        while True:
            try:
                tablePath = f'//*[@id="root"]/section/section[2]/div[2]/section[2]/section[3]/div/div[2]/div/div/div[4]/div[1]/div/div/div[1]/div/div[2]/div/div/div/div[{divNum}]/table/tbody'
                self.get_table_rows(tablePath)
                teams = []

                # Get all the team and money info and put it into an array
                # The loop starts at one because xpaths are not indexed from 0
                for row in range(1, len(self.tableRows) + 1):
                    teams.append(self.get_info(row))

                # Creates the actual match pairs from the teams array
                # Incriments by 2 so that it creates the pairs without an out of bounds error
                for item in range(0, len(teams), 2):
                    if item + 1 < len(teams):
                        pair = [teams[item], teams[item+1]]

                    # Appends none to the pair if the site is missing a number for any reason i.e. updating the odds
                    else:
                        pair = [teams[item], None]

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

# A way to run the scraper for debugging purposes
scraper = DraftKingsScraper()
pprint.pprint(scraper.run())