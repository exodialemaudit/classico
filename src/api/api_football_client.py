import requests
import os

API_KEY = os.getenv("API_FOOTBALL_KEY", "your_api_key_here")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

def get_team_info(team_id):
    url = f"{BASE_URL}/teams?id={team_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_team_stats(team_id, season):
    url = f"{BASE_URL}/teams/statistics?team={team_id}&season={season}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

if __name__ == "__main__":
    team_info = get_team_info(33)
    print(team_info)