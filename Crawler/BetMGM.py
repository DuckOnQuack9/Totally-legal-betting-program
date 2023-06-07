from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import numpy as np
import time
import sys

class BetMGMScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.encoding = sys.stdout.encoding
        self.table = None
        self.tableRows = None

    def get_table_rows(self):
        try:
            self.table = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-view"]/ms-widget-layout/ms-widget-slot/ms-composable-widget/ms-widget-slot[2]/ms-tabbed-grid-widget/ms-grid/div/ms-event-group[1]')))
        except TimeoutException:
            pass

        self.tableRows = self.table.find_elements(By.XPATH, './*')

    def get_info(self, tr):
        moneyPath1 = f'//*[@id="main-view"]/ms-widget-layout/ms-widget-slot/ms-composable-widget/ms-widget-slot[2]/ms-tabbed-grid-widget/ms-grid/div/ms-event-group[1]/ms-six-pack-event[{tr}]/div/div/div/ms-option-group[3]/ms-option[1]/ms-event-pick/div/div[2]/ms-font-resizer'
        moneyPath2 = f'//*[@id="main-view"]/ms-widget-layout/ms-widget-slot/ms-composable-widget/ms-widget-slot[2]/ms-tabbed-grid-widget/ms-grid/div/ms-event-group[1]/ms-six-pack-event[{tr}]/div/div/div/ms-option-group[3]/ms-option[2]/ms-event-pick/div/div[2]/ms-font-resizer'
        teamPath1 = f'//*[@id="main-view"]/ms-widget-layout/ms-widget-slot/ms-composable-widget/ms-widget-slot[2]/ms-tabbed-grid-widget/ms-grid/div/ms-event-group[1]/ms-six-pack-event[{tr}]/div/a/ms-event-detail/ms-event-name/ms-inline-tooltip/div/div[1]/div/div'
        teamPath2 = f'//*[@id="main-view"]/ms-widget-layout/ms-widget-slot/ms-composable-widget/ms-widget-slot[2]/ms-tabbed-grid-widget/ms-grid/div/ms-event-group[1]/ms-six-pack-event[{tr}]/div/a/ms-event-detail/ms-event-name/ms-inline-tooltip/div/div[2]/div/div'
        moneyLine1 = None
        teamName1 = None
        moneyLine2 = None
        teamName2 = None

        try:
            moneyLine1 = self.driver.find_element(By.XPATH, moneyPath1).text
            moneyLine2 = self.driver.find_element(By.XPATH, moneyPath2).text
        except:
            moneyLine1 = None
            moneyLine2 = None

        try: 
            teamName1 = self.driver.find_element(By.XPATH, teamPath1).text
            teamName2 = self.driver.find_element(By.XPATH, teamPath2).text
        except:
            teamName1 = None
            teamName2 = None

        return [[teamName1, moneyLine1], [teamName2, moneyLine2]]

    def run(self):
        self.driver.get('https://sports.in.betmgm.com/en/sports/baseball-23/betting/usa-9/mlb-75')
        self.get_table_rows()
        pyResult = [self.get_info(row) for row in range(1, len(self.tableRows) + 1)]
        result = np.array(pyResult, dtype=object)
        self.driver.quit()
        return result
