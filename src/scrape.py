import requests
import re
from bs4 import BeautifulSoup

def get_player_club_history(player_url):
    response = requests.get(player_url)
    soup = BeautifulSoup(response.content, "html.parser")

    club_history = set()
    for club_link in soup.find_all(class_="player-club-history__team-name player-club-history__team-name--short"):
        club_name = clean_club_name(club_link.text)
        club_history.add(club_name)

    return club_history

def clean_club_name(club_name):
  """Cleans a Premier League club name by removing whitespace from the end and the word 'loan' if it is present."""

  loan_popped = re.sub(r"\((Loan)\)", '', club_name) # removes '(Loan)'
  return re.sub(r"\s+$", '', loan_popped) # removes whitespace

def main():
    player_urls = [
        "https://www.premierleague.com/players/3452/Danny-Welbeck/overview"
    ]
    

    for player_url in player_urls:
        club_history = get_player_club_history(player_url)
        print(player_url, club_history)

if __name__ == "__main__":
    main()
