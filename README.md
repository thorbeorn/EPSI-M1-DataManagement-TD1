# EPSI-M1-DataManagement-TD1

## TD 1 : Performance et Sécurité

Ce TD regroupe deux projets complémentaires :

-   **Analyse de performance : CSV vs Parquet**
-   **Protection de données : masquage, anonymisation, chiffrement et
    gestion des accès**

L'objectif est d'explorer à la fois :

-   les formats de stockage performants pour les pipelines de données,
-   les bonnes pratiques de sécurité et de protection des données.

------------------------------------------------------------------------

## 🚀 Objectifs pédagogiques

✔ Comprendre les différences entre CSV et Parquet\
✔ Manipuler et convertir des données avec Pandas\
✔ Mesurer la performance de lecture/écriture\
✔ Mettre en place un pipeline de protection des données personnelles\
✔ Effectuer du masking, anonymisation, pseudonymisation\
✔ Chiffrer/déchiffrer les emails avec Fernet (cryptography)\
✔ Gérer des rôles utilisateurs avec accès restreints\
✔ Manipuler des fichiers Parquet bruts et compressés

------------------------------------------------------------------------

## 📂 Structure générale du TD

    EPSI-M1-DataManagement-TD1/
    │── LICENSE.txt
    │── .gitignore
    │── exo1_data_performance/
    │   ├── main.py
    │   ├── README.md
    │   ├── requirements.txt
    │   └── data/
    │       ├── flight_data_2024.csv
    │       ├── flight_data_2024.parquet
    │       └── flight_data_2024_compressed.parquet
    │
    │── exo2_data_protection/
    │   ├── main.py
    │   ├── clients_data.parquet
    │   ├── mail.key
    │   ├── requirements.txt
    │   └── README.md
    │
    └── README.md   ← ce fichier général

------------------------------------------------------------------------

# 🧪 Exercice 1 --- Performance : CSV vs Parquet

## 🔍 Description

Ce script :

-   Télécharge automatiquement le dataset Flight Data 2024 depuis
    Kaggle\
-   Extrait le CSV\
-   Produit deux fichiers Parquet :
    -   non compressé\
    -   compressé (brotli)\
-   Mesure et compare :
    -   ⏱ Temps d'écriture\
    -   ⏱ Temps de lecture\
    -   📏 Taille des fichiers\
    -   ⏱ Lecture de colonnes spécifiques (CSV vs Parquet)

🎯 **Objectif : démontrer pourquoi Parquet est plus performant dans les
architectures data modernes.**

------------------------------------------------------------------------

## 📦 Technologies utilisées

-   pandas\
-   pyarrow / fastparquet\
-   tqdm\
-   requests

------------------------------------------------------------------------

# 🔐 Exercice 2 --- Sécurité : Masquage, Anonymisation, Chiffrement

## 🔍 Description

Ce projet applique un pipeline complet de protection des données clients
:

### 1. **Masking**

-   téléphone → seuls les deux premiers digits conservés\
-   noms/prénoms → remplacés via Faker

### 2. **Anonymisation**

-   villes transformées en codes département\
-   gestion approximative via `get_close_matches`

### 3. **Pseudonymisation**

-   génération d'un identifiant client fictif (5 chiffres)

### 4. **Chiffrement (Fernet)**

-   génération automatique de `mail.key`\
-   chiffrement / déchiffrement des emails

### 5. **Rôles utilisateurs**

  Rôle                 Colonnes visibles                        Niveau
  -------------------- ---------------------------------------- --------
  Analyste Marketing   ID pseudo, montant, département          Moyen
  Support Client N1    ID pseudo, nom/prénom fake, tel masqué   Élevé
  Admin Sécurité       Accès complet                            Aucun

------------------------------------------------------------------------

# 🛠 Installation générale

### 1. Créer un environnement virtuel

    python -m venv venv

### 2. Activer l'environnement

**Windows**

    venv\Scripts\activate

**macOS / Linux**

    source venv/bin/activate

### 3. Installer les dépendances

    pip install -r exo1_data_performance/requirements.txt
    pip install -r exo2_data_protection/requirements.txt

------------------------------------------------------------------------

# ▶️ Exécution

### Exercice 1 : performance

    python exo1_data_performance/main.py

### Exercice 2 : sécurité

    python exo2_data_protection/main.py

------------------------------------------------------------------------

# 🎯 Compétences acquises

-   Choisir un format de stockage optimal pour un pipeline data\
-   Mesurer et optimiser les performances I/O\
-   Construire un pipeline complet de protection des données\
-   Appliquer masking, anonymisation, pseudonymisation\
-   Implémenter un chiffrement robuste (Fernet)\
-   Gérer des permissions basées sur les rôles

------------------------------------------------------------------------

# 📄 Licence

Projet libre d'utilisation et de modification --- usage pédagogique
EPSI.
