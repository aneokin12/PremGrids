import requests
import selenium
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 

def get_player_club_history(player_url):
    response = requests.get(player_url)
    soup = BeautifulSoup(response.content, "html.parser")

    club_history = set()
    for club_link in soup.find_all(class_="player-club-history__team-name player-club-history__team-name--short"):
        club_name = clean_club_name(club_link.text)
        club_history.add(club_name)

    return club_history

def get_player_links():
    """Scrapes entire PL directory of players for club history and URL"""
    options = webdriver.ChromeOptions() 
    options.headless = True 
    driver = webdriver.Chrome(service=ChromeService( 
        ChromeDriverManager().install()), options=options) 
    
    # load target website 
    url = 'https://www.premierleague.com/players' 
    
    # get website content 
    driver.get(url) 
    
    # instantiate player_urls 
    player_urls = [] 
    
    # instantiate height of webpage 
    last_height = driver.execute_script('return document.body.scrollHeight') 
    
    # set target count 
    itemTargetCount = 30

    # scroll to bottom of webpage 
    while True: 
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') 
    
        # wait for content to load 
        time.sleep(1) 
    
        new_height = driver.execute_script('return document.body.scrollHeight') 
    
        if new_height == last_height: 
            break 
    
        last_height == new_height 
    
    # select elements by XPath
    time.sleep(3)
    elements = driver.find_elements(By.CLASS_NAME, "player__name") 
    links = [link.get_attribute("href") for link in elements] 

    player_urls.extend(links)
    
    return player_urls


def clean_club_name(club_name):
  """Cleans a Premier League club name by removing whitespace from the end and the word 'loan' if it is present."""

  loan_popped = re.sub(r"\((Loan)\)", '', club_name) # removes '(Loan)'
  return re.sub(r"\s+$", '', loan_popped) # removes whitespace

def main():
    player_urls = get_player_links()
    for player_url in player_urls:
        club_history = get_player_club_history(player_url)
        print(player_url, club_history)

if __name__ == "__main__":
    main()
