from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import numpy as np

class DraftKingsScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.encoding = sys.stdout.encoding
        self.table = None
        self.tableRows = None

    def get_table_rows(self):
        self.table = self.driver.find_element(By.XPATH, '//*[@id="root"]/section/section[2]/div[2]/section[2]/section[3]/div/div[2]/div/div/div[4]/div[1]/div/div/div[1]/div/div[2]/div/div/div/div[1]/table/tbody')
        self.tableRows = self.table.find_elements(By.XPATH, './*')

    def get_info(self, tr):
        moneyPath = f'//*[@id="root"]/section/section[2]/div[2]/section[2]/section[3]/div/div[2]/div/div/div[4]/div[1]/div/div/div[1]/div/div[2]/div/div/div/div[1]/table/tbody/tr[{tr}]/td[3]/div/div/div/div/div[2]/span'
        teamPath = f'//*[@id="root"]/section/section[2]/div[2]/section[2]/section[3]/div/div[2]/div/div/div[4]/div[1]/div/div/div[1]/div/div[2]/div/div/div/div[1]/table/tbody/tr[{tr}]/th/a/div/div[2]/div/span/div/div'
        moneyLine = None
        teamName = None

        try:
            moneyline = self.driver.find_element(By.XPATH, moneyPath)
            moneyline_text = moneyline.text.replace("−", "-")
            moneyLine = moneyline_text.encode(self.encoding, errors='replace').decode(self.encoding)
        except:
            moneyline = None

        try: 
            teamName = self.driver.find_element(By.XPATH, teamPath).text
        except:
            teamName = None

        return [teamName, moneyLine]

    def create_pairs(self):
        self.get_table_rows()
        teams = [self.get_info(row) for row in range(1, len(self.tableRows) + 1)]
        pyPairs = [[teams[x], teams[x+1]] if x+1 < len(teams) else [teams[x], None] for x in range(0, len(teams), 2)]
        pairs = np.array(pyPairs, dtype=object)
        return pairs

    def run(self):
        self.driver.get('https://sportsbook.draftkings.com/featured?category=game-lines&subcategory=baseball')
        result = self.create_pairs()
        self.driver.quit()
        return result
