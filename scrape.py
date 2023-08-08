import requests
from bs4 import BeautifulSoup

def get_player_club_history(player_url):
    response = requests.get(player_url)
    soup = BeautifulSoup(response.content, "html.parser")

    club_history = set()
    for club_link in soup.find_all(class_="player-club-history__team-name player-club-history__team-name--short"):
        club_name = club_link.text
        club_history.add(club_name)

    return club_history

def main():
    player_urls = [
        "https://www.premierleague.com/players/3452/Danny-Welbeck/overview"
    ]

    for player_url in player_urls:
        club_history = get_player_club_history(player_url)
        print(player_url, club_history)

if __name__ == "__main__":
    main()
