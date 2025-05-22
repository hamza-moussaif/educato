# Système d'Automatisation de Création de Contenu Éducatif

Une application web permettant aux enseignants de générer automatiquement des supports pédagogiques variés en utilisant des modèles d'IA open source.

## Fonctionnalités

- Génération de QCM, exercices, fiches et infographies
- Interface utilisateur minimaliste et élégante
- Utilisation de modèles d'IA open source (Llama 3, Mistral, SOLAR)
- Exportation en PDF et DOCX
- Système de gestion des utilisateurs
- Historique des générations

## Prérequis

- Python 3.10+
- Node.js 16+
- Ollama (pour les modèles LLM locaux)
- Stable Diffusion (pour la génération d'images)

## Installation

1. Cloner le repository :
```bash
git clone [URL_DU_REPO]
cd educational-content-generator
```

2. Installer les dépendances Python :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r requirements.txt
```

3. Installer les dépendances Node.js :
```bash
npm install
```
ollama pull mistral

4. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

5. Lancer l'application :
```bash
# Terminal 1 (Backend)
python app.py

# Terminal 2 (Frontend)
npm start
```

## Structure du Projet

```
educational-content-generator/
├── backend/
│   ├── app.py
│   ├── models/
│   ├── routes/
│   └── services/
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       └── styles/
└── tests/
```

## Technologies Utilisées

- **Frontend :**
  - React
  - Material-UI
  - Bootstrap 5
  - Framer Motion

- **Backend :**
  - Flask
  - SQLAlchemy
  - LangChain
  - Transformers

- **Base de données :**
  - SQLite

## Contribution

Les contributions sont les bienvenues ! Veuillez consulter le fichier CONTRIBUTING.md pour les directives.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails. 