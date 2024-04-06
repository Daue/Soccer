from selenium import webdriver
from selenium.webdriver.common.by import By
from base_page import BasePage
import csv
import os
import requests


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\dawid\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2")
    #options.add_argument("--headless")
    #options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)


class MainPage(BasePage):
    DestinationFolder = 'data'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_index = 0

        if not os.path.exists(self.DestinationFolder):
            os.makedirs(self.DestinationFolder)

    def wrap(self):
        matches_data = []
        all_matches = self.wait_for_elements(By.XPATH, "//div[contains(@class,'match-item-container')]")
        for match in all_matches:
            matches_data.append(self._collect_match_data(match))
        self._save_results(matches_data)
        return True

    def _collect_match_data(self, match_element):
        match_data = {}
        # date
        match_data['date'] = match_element.find_element(By.XPATH, ".//span[@class='status']").text
        # team names
        team_info = match_element.find_elements(By.XPATH, ".//div[@class='team-info']")
        match_data['team1_name'] = team_info[0].text
        match_data['team2_name'] = team_info[1].text
        # scores
        score_info = match_element.find_elements(By.XPATH, ".//span[@class='score']")
        match_data['team1_score'] = score_info[0].text
        match_data['team2_score'] = score_info[1].text
        # icons
        pictures = match_element.find_elements(By.XPATH, ".//picture/img")
        match_data['match_icon'] = pictures[0].get_attribute('data-src')
        match_data['team1_icon'] = pictures[1].get_attribute('data-src')
        match_data['team2_icon'] = pictures[2].get_attribute('data-src')
        # link to match
        match_data['link'] = match_element.find_element(By.XPATH, ".//a[@class='match-link']").get_attribute('href')
        return match_data

    def _save_results(self, data):
        for row_data in data:
            row_data['match_icon'] = self._save_icon(row_data['match_icon'])
            row_data['team1_icon'] = self._save_icon(row_data['team1_icon'])
            row_data['team2_icon'] = self._save_icon(row_data['team2_icon'])

        fieldnames = ['date', 'team1_name', 'team2_name', 'team1_score', 'team2_score', 'match_icon', 'team1_icon',
                      'team2_icon', 'link']
        with open(os.path.join(self.DestinationFolder, 'result.csv'), 'w', encoding='utf8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def _save_icon(self, ulr):
        img = requests.get(ulr).content
        file_name = str(self.icon_index) + '.png'
        with open(os.path.join(self.DestinationFolder, file_name), 'wb') as f:
            f.write(img)
        self.icon_index += 1
        return file_name


page = MainPage(get_driver(), "https://www.meczyki.pl/mecze")
page.wrap()
