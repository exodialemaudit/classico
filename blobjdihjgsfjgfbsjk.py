import requests
import pandas as pd

# Votre clé API personnelle
API_KEY = '77a267023c9f88575f9f2af73036fcc0'
BASE_URL = 'https://v3.football.api-sports.io/'

# En-têtes pour l'authentification
headers = {
    'x-apisports-key': API_KEY
}

# Fonction pour obtenir l'ID d'une équipe par son nom
def get_team_id(team_name):
    response = requests.get(f"{BASE_URL}teams", headers=headers, params={'search': team_name})
    data = response.json()
    if data['response']:
        return data['response'][0]['team']['id']
    else:
        raise ValueError(f"Équipe '{team_name}' non trouvée.")

# Fonction pour récupérer les informations d'une équipe
def get_team_info(team_id):
    response = requests.get(f"{BASE_URL}teams", headers=headers, params={'id': team_id})
    return response.json()

# Fonction pour récupérer les joueurs d'une équipe
def get_team_players(team_id):
    response = requests.get(f"{BASE_URL}players", headers=headers, params={'team': team_id, 'season': 2024})
    return response.json()

# Obtenir les IDs des équipes PSG et OM
psg_id = get_team_id("Paris Saint Germain")
om_id = get_team_id("Marseille")

# Récupérer les informations des équipes
psg_info = get_team_info(psg_id)
om_info = get_team_info(om_id)

# Récupérer les joueurs des équipes
psg_players = get_team_players(psg_id)
om_players = get_team_players(om_id)

# Déboguer la réponse de l'API
print("\nRéponse API pour les joueurs du PSG:")
print(psg_players)

# Afficher les informations
print("Informations sur le PSG :", psg_info)
print("Informations sur l'OM :", om_info)

# Vérifier si nous avons des données avant de créer le DataFrame
if not psg_players.get('response'):
    print("Aucune donnée de joueur trouvée pour le PSG")
else:
    psg_players_df = pd.DataFrame([
        {
            'name': player['player']['firstname'] + ' ' + player['player']['lastname'],
            'position': player['statistics'][0]['games']['position'] if player['statistics'] else 'Unknown',
            'age': player['player']['age']
        }
        for player in psg_players['response']
    ])
    print("\nJoueurs du PSG :")
    print(psg_players_df[['name', 'position', 'age']].head())

if not om_players.get('response'):
    print("Aucune donnée de joueur trouvée pour l'OM")
else:
    om_players_df = pd.DataFrame([
        {
            'name': player['player']['firstname'] + ' ' + player['player']['lastname'],
            'position': player['statistics'][0]['games']['position'] if player['statistics'] else 'Unknown',
            'age': player['player']['age']
        }
        for player in om_players['response']
    ])
    print("\nJoueurs de l'OM :")
    print(om_players_df[['name', 'position', 'age']].head())