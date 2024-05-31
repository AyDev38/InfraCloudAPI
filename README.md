# Système d'Information sur les Pays

Ce projet fournit une API sur les pays, comprenant un frontend construit avec Node.js et API backend construite avec FastAPI et une base de données en SQLite.

## Table des Matières

- [Installation](#installation)
  - [Frontend (Node.js)](#frontend-nodejs)
  - [Backend (FastAPI)](#backend-fastapi)
- [Utilisation](#utilisation)
  - [Exécution du Frontend](#exécution-du-frontend)
  - [Exécution du Backend](#exécution-du-backend)
- [Endpoints de l'API](#endpoints-de-lapi)
- [Contribution](#contribution)
- [Licence](#licence)

## Installation

### Frontend (Node.js)

1. **Clonez le dépôt :**

   ```bash
   git clone https://github.com/AymeRx/InfraCloudAPI.git
   cd InfraCloudAPI/frontend
   ```

2. **Installez les dépendances :**

   ```bash
   npm install
   ```

3. **Démarrez le serveur de développement :**

   ```bash
   npm start
   ```

   Le frontend sera disponible à `http://localhost:3000`.

### Backend (FastAPI)

1. **Changer de dossier :**

   ```bash
   cd ../api
   ```

2. **Créez un environnement virtuel :**

   ```bash
   python -m venv venv
   ```

3. **Activez l'environnement virtuel :**

   Sur Windows :

   ```bash
   venv\Scripts\activate
   ```

   Sur macOS/Linux :

   ```bash
   source venv/bin/activate
   ```

4. **Installez les dépendances :**

   ```bash
   pip install -r requirements.txt
   ```

5. **Exécutez le serveur FastAPI :**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload   
   ```

   L'API sera disponible à `http://localhost:8000`.

## Utilisation

### Exécution du Frontend

Après avoir démarré le serveur de développement, ouvrez votre navigateur et naviguez vers `http://localhost:3000`. Vous verrez l'interface frontend où vous pourrez interagir avec l'api sur les pays.

### Exécution du Backend

Avec le serveur FastAPI en cours d'exécution, vous pouvez accéder à la documentation de l'API en naviguant vers `http://localhost:8000/docs` dans votre navigateur. Cela fournira une interface Swagger UI pour tester les endpoints de l'API.

## Endpoints de l'API

Voici les différents endpoints de l'API disponibles :

- `GET /countries` : Récupérer la liste de tous les pays.
- `GET /countries/{code}` : Récupérer des informations sur un pays spécifique par son code.
- `POST /countries` : Créer un nouveau pays.
- `PUT /countries/{code}` : Mettre à jour les informations sur un pays spécifique par son code.
- `DELETE /countries/{code}` : Supprimer un pays par son code.
- `GET /countries/search/by-name` : Rechercher des pays par nom.
- `GET /countries/search/by-continent-code` : Rechercher des pays par code de continent.
- `GET /continents/` : Récupérer la liste de tous les continents.
- `GET /continents/{code}` : Récupérer des informations sur un continent spécifique par son code.
- `POST /countries/{code}/pib/{data}` : Récupérer des informations sur un continent spécifique par son code.
- `GET /countries/{code}/pib` : Récupérer des informations sur un continent spécifique par son code.

## Schéma de du code :

![Schéma de l'Application](/SchemaAPI.drawio.png)
