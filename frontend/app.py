#!/usr/bin/env python3
"""
Interface Streamlit pour Classico Foot LLM - Débat Personnalisé.
Cette application permet de configurer deux IA avec un choix étendu d'équipes (clubs et nationales),
leurs personnalités et tons personnalisables, et de lancer un débat interactif.
Les messages s'affichent sous forme de bulles de dialogue façon iMessage avec animation "typing".
"""

import os
import sys
import streamlit as st
import time
import logging
import re
from typing import List, Dict
import asyncio
from debate_engine.conversation_manager import generate_debate_response

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Ajout du dossier 'src' au PYTHONPATH pour les imports internes
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..", "src")
if src_path not in sys.path:
    sys.path.append(src_path)

# Importer la logique de débat depuis le module conversation_manager
from debate_engine.conversation_manager import start_debate

# Dictionnaire enrichi des ligues et équipes avec URLs d'images
teams_data = {
    "Ligue 1": {
        "Paris Saint-Germain": "https://upload.wikimedia.org/wikipedia/fr/7/76/Paris_Saint-Germain_logo.png",
        "Olympique de Marseille": "https://upload.wikimedia.org/wikipedia/fr/4/43/Logo_Olympique_de_Marseille.svg",
        "AS Monaco": "https://upload.wikimedia.org/wikipedia/fr/5/58/AS_Monaco_FC.png",
        "OGC Nice": "https://upload.wikimedia.org/wikipedia/fr/b/b1/Logo_OGC_Nice_2013.png",
        "LOSC Lille": "https://upload.wikimedia.org/wikipedia/fr/6/62/Logo_LOSC_Lille_2018.png",
        "Olympique Lyonnais": "https://upload.wikimedia.org/wikipedia/fr/e/e2/Olympique_lyonnais_%28logo%29.svg",
        "Stade Rennais": "https://upload.wikimedia.org/wikipedia/fr/8/8c/Logo_Stade_Rennais_FC.svg"
    },
    "Premier League": {
        "Manchester City": "https://upload.wikimedia.org/wikipedia/fr/b/ba/Logo_Manchester_City_2016.png",
        "Liverpool FC": "https://upload.wikimedia.org/wikipedia/fr/5/54/Logo_FC_Liverpool.png",
        "Arsenal FC": "https://upload.wikimedia.org/wikipedia/fr/5/53/Arsenal_FC.png",
        "Chelsea FC": "https://upload.wikimedia.org/wikipedia/fr/5/51/Logo_Chelsea.svg",
        "Manchester United": "https://upload.wikimedia.org/wikipedia/fr/b/b9/Logo_Manchester_United.svg",
        "Tottenham": "https://upload.wikimedia.org/wikipedia/fr/5/5c/Logo_Tottenham_Hotspur.png"
    },
    "LaLiga": {
        "Real Madrid": "https://upload.wikimedia.org/wikipedia/fr/c/c7/Logo_Real_Madrid.svg",
        "FC Barcelone": "https://upload.wikimedia.org/wikipedia/fr/a/a1/Logo_FC_Barcelona.svg",
        "Atlético Madrid": "https://upload.wikimedia.org/wikipedia/fr/9/93/Logo_Atletico_Madrid_2017.svg",
        "Séville FC": "https://upload.wikimedia.org/wikipedia/fr/f/f1/Logo_Sevilla_FC.svg",
        "Real Sociedad": "https://upload.wikimedia.org/wikipedia/fr/5/55/Real_Sociedad_logo.png"
    },
    "Bundesliga": {
        "Bayern Munich": "https://upload.wikimedia.org/wikipedia/fr/1/1b/Logo_FC_Bayern_Munich.svg",
        "Borussia Dortmund": "https://upload.wikimedia.org/wikipedia/fr/4/4d/Logo_Borussia_Dortmund.svg",
        "RB Leipzig": "https://upload.wikimedia.org/wikipedia/fr/0/04/RB_Leipzig_2014_logo.svg",
        "Bayer Leverkusen": "https://upload.wikimedia.org/wikipedia/fr/4/4a/Bayer_04_Leverkusen_logo.svg"
    },
    "Serie A": {
        "AC Milan": "https://upload.wikimedia.org/wikipedia/fr/d/d0/Logo_AC_Milan.svg",
        "Inter Milan": "https://upload.wikimedia.org/wikipedia/fr/8/89/Inter_Milan_2021.svg",
        "Juventus": "https://upload.wikimedia.org/wikipedia/fr/9/9f/Logo_Juventus.svg",
        "AS Roma": "https://upload.wikimedia.org/wikipedia/fr/0/0e/AS_Roma_Logo_2017.png",
        "Napoli": "https://upload.wikimedia.org/wikipedia/fr/2/2d/SSC_Napoli.svg"
    },
    "Équipes Nationales": {
        "France": "https://upload.wikimedia.org/wikipedia/fr/4/43/Logo_%C3%89quipe_France_Football_2018.svg",
        "Brésil": "https://upload.wikimedia.org/wikipedia/fr/3/31/Logo_CBF_2019.svg",
        "Argentine": "https://upload.wikimedia.org/wikipedia/fr/a/a6/Logo_%C3%89quipe_Argentine_Football_2014.png",
        "Allemagne": "https://upload.wikimedia.org/wikipedia/fr/e/e3/DFB_Logo_2017.svg",
        "Espagne": "https://upload.wikimedia.org/wikipedia/fr/a/a9/Logo_%C3%89quipe_Espagne_Football_-_2021.svg",
        "Portugal": "https://upload.wikimedia.org/wikipedia/fr/4/45/Logo_F%C3%A9d%C3%A9ration_Portugal_Football.svg",
        "Italie": "https://upload.wikimedia.org/wikipedia/fr/b/b4/Logo_%C3%89quipe_Italie_Football_2017.svg",
        "Angleterre": "https://upload.wikimedia.org/wikipedia/fr/4/4a/Logo_FA_Angleterre_2009.svg"
    }
}

def configure_page():
    st.set_page_config(
        page_title="Classico Foot LLM - Débat Football",
        page_icon="⚽",
        layout="wide"
    )

def apply_custom_css():
    st.markdown("""
        <style>
        /* Messages Container */
        .messages-container {
            height: 600px;
            overflow-y: auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 15px;
        }
        
        /* Message Wrapper */
        .message-wrapper {
            display: flex;
            margin: 10px 0;
            max-width: 80%;
        }
        
        .message-wrapper.team1-message {
            margin-left: auto;
        }
        
        .message-wrapper.team2-message {
            margin-right: auto;
        }
        
        /* Message */
        .message {
            padding: 15px;
            border-radius: 20px;
            position: relative;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        .team1-message .message {
            background-color: #007AFF;
            color: white;
            border-bottom-right-radius: 5px;
        }
        
        .team2-message .message {
            background-color: #E9E9EB;
            color: black;
            border-bottom-left-radius: 5px;
        }
        
        /* Message Header */
        .message-header {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
        }
        
        .team-logo {
            width: 24px;
            height: 24px;
            margin-right: 8px;
            border-radius: 12px;
        }
        
        /* Message Content */
        .message-content {
            font-size: 16px;
            line-height: 1.4;
        }
        
        /* Typing Indicator */
        .typing-indicator {
            padding: 10px;
            margin: 10px 0;
            display: inline-block;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    configure_page()
    apply_custom_css()
    
    st.title("⚽ Classico Foot LLM - Débat Football")
    
    # Configuration des équipes
    st.markdown('<div class="config-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Configuration du Débat</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Équipe 1
    with col1:
        st.markdown('<div class="team-config">', unsafe_allow_html=True)
        st.subheader("Équipe 1")
        league1 = st.selectbox(
            "Championnat",
            ["Ligue 1", "Premier League", "LaLiga", "Bundesliga", "Serie A", "Équipes Nationales"],
            key="league1"
        )
        team1 = st.selectbox("Équipe", get_teams_for_league(league1), key="team1")
        personality1 = st.selectbox(
            "Personnalité",
            ["Standard", "Ultra", "Commentateur", "Ancien joueur", "Expert Tactique", "Footix"],
            key="personality1"
        )
        style1 = st.selectbox(
            "Style de débat",
            ["Factuel", "Passionné", "Provocateur", "Humoristique"],
            key="style1"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Équipe 2
    with col2:
        st.markdown('<div class="team-config">', unsafe_allow_html=True)
        st.subheader("Équipe 2")
        league2 = st.selectbox(
            "Championnat",
            ["Ligue 1", "Premier League", "LaLiga", "Bundesliga", "Serie A", "Équipes Nationales"],
            key="league2"
        )
        team2 = st.selectbox("Équipe", get_teams_for_league(league2), key="team2")
        personality2 = st.selectbox(
            "Personnalité",
            ["Standard", "Ultra", "Commentateur", "Ancien joueur", "Expert Tactique", "Footix"],
            key="personality2"
        )
        style2 = st.selectbox(
            "Style de débat",
            ["Factuel", "Passionné", "Provocateur", "Humoristique"],
            key="style2"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Paramètres du débat
    st.markdown('<div class="debate-params">', unsafe_allow_html=True)
    st.subheader("Paramètres du Débat")
    col3, col4 = st.columns(2)
    with col3:
        topic = st.text_input("Sujet du débat", "Qui a la meilleure équipe actuellement ?")
        context = st.text_area("Contexte additionnel (optionnel)", "")
    with col4:
        max_exchanges = st.slider("Nombre d'échanges", 2, 10, 4)
        debate_tone = st.select_slider(
            "Ton général du débat",
            options=["Très calme", "Calme", "Normal", "Animé", "Très animé"],
            value="Normal"
        )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Lancement du débat
    if st.button("Lancer le Débat"):
        with st.spinner("Génération du débat en cours..."):
            simulate_debate(team1, team2, max_exchanges, topic)

def get_teams_for_league(league):
    teams = {
        "Ligue 1": [
            "Paris Saint-Germain", "Olympique de Marseille", "AS Monaco",
            "LOSC Lille", "Olympique Lyonnais", "Stade Rennais",
            "RC Lens", "OGC Nice", "RC Strasbourg", "Montpellier HSC"
        ],
        "Premier League": [
            "Manchester City", "Liverpool FC", "Arsenal FC",
            "Manchester United", "Chelsea FC", "Tottenham Hotspur",
            "Newcastle United", "West Ham United", "Brighton", "Aston Villa"
        ],
        "LaLiga": [
            "Real Madrid", "FC Barcelone", "Atlético Madrid",
            "Real Sociedad", "Villarreal CF", "Athletic Bilbao",
            "Séville FC", "Real Betis", "Valence CF", "Osasuna"
        ],
        "Bundesliga": [
            "Bayern Munich", "Borussia Dortmund", "RB Leipzig",
            "Bayer Leverkusen", "Eintracht Frankfurt", "VfL Wolfsburg",
            "Borussia M'gladbach", "SC Fribourg", "VfB Stuttgart"
        ],
        "Serie A": [
            "AC Milan", "Inter Milan", "Juventus Turin",
            "AS Roma", "SSC Napoli", "Lazio Rome",
            "Atalanta Bergame", "Fiorentina", "Torino", "Sassuolo"
        ],
        "Équipes Nationales": [
            "France", "Brésil", "Argentine", "Allemagne",
            "Espagne", "Portugal", "Italie", "Angleterre",
            "Belgique", "Pays-Bas", "Uruguay", "Croatie",
            "Danemark", "Mexique", "Colombie", "Sénégal"
        ]
    }
    return teams.get(league, [])

def simulate_typing():
    """Simule l'effet de frappe avec des points animés."""
    return st.markdown("""
        <div class="typing-indicator">
            <div class="typing-dots">
                <span>●</span><span>●</span><span>●</span>
            </div>
        </div>
        <style>
        .typing-indicator {
            padding: 10px;
            margin: 10px 0;
        }
        .typing-dots {
            text-align: left;
        }
        .typing-dots span {
            animation: typing 1s infinite;
            margin-right: 5px;
            font-size: 20px;
            color: #808080;
        }
        .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
        .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typing {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }
        </style>
    """, unsafe_allow_html=True)

async def generate_response_async(speaker: str, topic: str, personality: str, style: str) -> str:
    """Génère une réponse de manière asynchrone."""
    response = await generate_debate_response(speaker, topic, personality, style)
    return response

def simulate_debate(team1: str, team2: str, max_exchanges: int, topic: str):
    """
    Simule un débat entre deux équipes avec génération en temps réel des messages.
    
    Args:
        team1: Nom de la première équipe
        team2: Nom de la deuxième équipe
        max_exchanges: Nombre maximum d'échanges
        topic: Sujet du débat
    """
    messages_container = st.container()
    messages: List[Dict] = []
    
    for i in range(max_exchanges * 2):
        current_team = team1 if i % 2 == 0 else team2
        message_class = "team1-message" if i % 2 == 0 else "team2-message"
        
        with messages_container:
            # Affiche l'indicateur de frappe
            typing_placeholder = st.empty()
            typing_placeholder.markdown(simulate_typing(), unsafe_allow_html=True)
            
            # Génère la réponse
            response = generate_debate_response(
                speaker=current_team,
                topic=topic,
                personality=st.session_state.get(f"personality{i%2 + 1}", "Standard"),
                style=st.session_state.get(f"style{i%2 + 1}", "Factuel")
            )
            
            # Simule la génération caractère par caractère
            current_message = ""
            for char in response:
                current_message += char
                messages.append({
                    "speaker": current_team,
                    "message": current_message,
                    "class": message_class
                })
                display_messages(messages, messages_container)
                time.sleep(0.02)
            
            # Supprime l'indicateur de frappe une fois le message complet
            typing_placeholder.empty()
            
            # Petite pause entre les messages
            time.sleep(0.5)

def display_messages(messages: List[Dict], container):
    """
    Affiche les messages dans un style iMessage.
    
    Args:
        messages: Liste des messages à afficher
        container: Conteneur Streamlit pour l'affichage
    """
    container.markdown("""
        <div style="height: 600px; overflow-y: auto; padding: 20px;">
    """, unsafe_allow_html=True)
    
    for msg in messages:
        logo_url = teams_data.get(msg["speaker"], {}).get("logo", "")
        container.markdown(f"""
            <div class="message-wrapper {msg['class']}">
                <div class="message">
                    <div class="message-header">
                        <img src="{logo_url}" class="team-logo" onerror="this.style.display='none'"/>
                        <strong>{msg['speaker']}</strong>
                    </div>
                    <div class="message-content">
                        {msg['message']}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    container.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()