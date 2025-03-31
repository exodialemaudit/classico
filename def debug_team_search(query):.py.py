def debug_team_search(query):
    url = f"{BASE_URL}teams"
    response = requests.get(url, headers=headers, params={'search': query})
    data = response.json()
    for team in data['response']:
     print(f"✅ Found: {team['team']['name']} (ID: {team['team']['id']})")

    debug_team_search("Paris")
    debug_team_search("Marseille")