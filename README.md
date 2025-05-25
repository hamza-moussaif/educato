# Système d'Automatisation de Création de Contenu Éducatif

Une application web permettant aux enseignants de générer automatiquement des supports pédagogiques variés en utilisant des modèles d'IA open source.

## Fonctionnalités

- Génération de QCM et exercices
- Interface utilisateur moderne et intuitive
- Utilisation de modèles d'IA open source (Llama 3, Mistral, SOLAR)
- Exportation en PDF et DOCX
- Système de gestion des utilisateurs
- Historique des générations
- Base de données MySQL pour une meilleure performance

## Prérequis

- Python 3.10+
- Node.js 16+
- MySQL/MariaDB
- phpMyAdmin (optionnel, pour la gestion de la base de données)
- Ollama (pour les modèles LLM locaux)

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
cd frontend
npm install
```

4. Configurer la base de données MySQL :

- Installer MySQL/MariaDB si ce n'est pas déjà fait
- Créer une base de données nommée `dbedu`
- Configurer les variables d'environnement dans `.env` :

```
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_NAME=dbedu
```

5. Initialiser la base de données :

```bash
python backend/reset_db.py
```

6. Lancer l'application :

```bash
# Terminal 1 (Backend)
python backend/app.py

# Terminal 2 (Frontend)
cd frontend
npm start
```

## Structure du Projet

```
educational-content-generator/
├── backend/
│   ├── app.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── reset_db.py
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── contexts/
│       └── utils/
└── tests/
```

## Technologies Utilisées

- **Frontend :**

  - React
  - Chakra UI
  - React Router
  - React Icons

- **Backend :**

  - Flask
  - SQLAlchemy
  - PyMySQL
  - Flask-JWT-Extended

- **Base de données :**
  - MySQL/MariaDB

## Fonctionnalités Principales

1. **Authentification**

   - Inscription et connexion des utilisateurs
   - Protection des routes avec JWT
   - Gestion des sessions

2. **Génération de Contenu**

   - Création de QCM personnalisés
   - Sélection du niveau scolaire
   - Choix de la matière
   - Interface intuitive pour la génération

3. **Interface Utilisateur**
   - Design moderne avec Chakra UI
   - Thème personnalisé
   - Responsive design
   - Animations fluides

## Contribution

Les contributions sont les bienvenues ! Veuillez consulter le fichier CONTRIBUTING.md pour les directives.

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
