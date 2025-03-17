Voici une version sans balises bash ou python pour que vous puissiez copier-coller plus facilement :

Classico Foot LLM

Ce projet a pour objectif de faire débattre localement deux LLM (supporters OM & supporters PSG), basés sur des données factuelles, grâce à OLLAMA. Vous trouverez ici :
	•	Une installation Python isolée (via venv).
	•	Des modèles de langage localement (Llama 2).
	•	Des données relatives à l’OM et au PSG.
	•	Un moteur de conversation permettant de faire s’affronter les deux LLM.

Sommaire
	1.	Prérequis
	2.	Installation
	3.	Utilisation
	4.	Organisation du Projet
	5.	Contribuer
	6.	Licence
	7.	Auteurs / Crédits

Prérequis
	1.	Python 3.9 ou supérieur
	•	Vérifiez votre version :
python3 –version
	•	Mettez à jour ou installez Python si nécessaire (par ex. via Homebrew sur macOS).
	2.	Git
	•	Pour cloner et partager le projet.
	•	Vérifiez :
git –version
	3.	OLLAMA
	•	Pour exécuter localement les modèles Llama 2.
	•	Sur macOS, installez-le avec Homebrew :
brew install ollama
	4.	Connexion Internet (pour la première installation)
	•	Les modèles Llama 2, qui peuvent peser plusieurs Go, seront téléchargés en local.

Installation

Étape 1. Cloner le dépôt et se positionner dedans :

git clone <URL_de_votre_dépôt.git>
cd classico-foot-llm

Étape 2. Créer et activer un environnement virtuel Python :

python3 -m venv venv
source venv/bin/activate      (macOS / Linux)

(Sur Windows PowerShell : .\venv\Scripts\activate)

Étape 3. Installer les dépendances Python :

pip install -r requirements.txt

Étape 4. Installer le modèle Llama 2 avec OLLAMA :

ollama pull llama2-7b

(Selon votre version d’Ollama, vous pourriez utiliser par exemple :
ollama pull llama2-7b-chat
ou un autre nom. Vérifiez la documentation ou faites ollama help pull.)

Étape 5. Vérifier que tout fonctionne :

ollama run –model llama2-7b “Bonjour, qui es-tu ?”

Vous devriez voir une réponse générée par le modèle.

Utilisation
	1.	Lancement du script principal
	•	Un fichier src/main.py (ou équivalent) pourra servir de démonstration.
	•	Exemple d’exécution :
python src/main.py
	2.	Intégration / Moteur de débat
	•	Dans le dossier src/debate_engine/, vous trouverez la logique pour alterner les tours de parole, injecter les données factuelles, etc.
	3.	Logs
	•	Les échanges (questions, réponses) peuvent être sauvegardés dans un fichier log, selon la configuration dans le code.

Organisation du Projet

classico-foot-llm/
├── data/
│   ├── om/
│   │   ├── stats_om.csv
│   │   ├── historique_om.json
│   └── psg/
│       ├── stats_psg.csv
│       ├── historique_psg.json
├── src/
│   ├── data_processing/
│   │   ├── data_loader.py
│   │   └── data_cleaning.py
│   ├── debate_engine/
│   │   ├── conversation_manager.py
│   │   ├── persona_manager.py
│   │   └── knowledge_retriever.py
│   ├── llm_interface/
│   │   ├── ollama_interface.py
│   │   └── local_llm_controller.py
│   └── main.py
├── tests/
│   ├── test_data_processing.py
│   ├── test_debate_engine.py
│   └── test_llm_interface.py
├── requirements.txt
├── .gitignore
└── README.md

Licence

(À compléter selon vos choix : MIT, Apache, GPL, etc.)

Auteurs / Crédits
	•	Personne A (Responsable Intégration LLM et Architecture)
	•	Personne B (Spécialiste Données et Moteur de Connaissance)
	•	Personne C (Orchestrateur du Débat, Interface & Tests)

N’hésitez pas à ajouter ou mentionner d’autres contributeurs !