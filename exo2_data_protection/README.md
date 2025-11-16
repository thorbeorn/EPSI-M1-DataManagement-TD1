# Data Protection Pipeline (Masking, Anonymization, Encryption)

Ce projet implémente un pipeline complet de protection des données
clients en utilisant : - **Pandas** pour la manipulation des données -
**Faker** pour la génération de données fictives - **Cryptography
(Fernet)** pour chiffrer les emails - **Rôles utilisateurs** pour
contrôler l'accès à certaines colonnes

------------------------------------------------------------------------

## 📦 Fonctionnalités

### 1. **Masquage (Masking)**

-   Masque les numéros de téléphone (seuls les 2 premiers chiffres sont
    conservés)
-   Remplacement des noms et prénoms par des données factices

### 2. **Anonymisation**

-   Convertit les villes en **codes de département**
-   Gestion approximative avec `get_close_matches`

### 3. **Pseudonymisation**

-   Génération d'un nouvel identifiant client fictif (5 chiffres)

### 4. **Chiffrement & Déchiffrement (Email)**

-   Chiffrement Fernet avec clé stockée dans un fichier `.key`
-   Déchiffrement possible uniquement avec la bonne clé

### 5. **Gestion des accès par rôle**

-   **Analyste Marketing** : ID pseudonymisé, montant d'achat,
    département
-   **Support N1** : ID pseudonymisé, nom et prénom fictifs, téléphone
    masqué
-   **Admin Sécurité** : accès complet aux données brutes

------------------------------------------------------------------------

## 📁 Structure des fichiers

    main.py
    clients_data.parquet
    mail.key              # généré automatiquement si absent
    requirements.txt
    README.md

------------------------------------------------------------------------

## 🛠 Installation

### 1. Créer un environnement virtuel (recommandé)

``` bash
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate     # Windows
```

### 2. Installer les dépendances

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## ▶️ Exécution

Assurez-vous que le fichier **clients_data.parquet** est présent, puis
lancez :

``` bash
python main.py
```

------------------------------------------------------------------------

## 🔑 Gestion de la clé Fernet

-   Si `mail.key` n'existe pas → il est automatiquement créé.
-   Les emails sont chiffrés dans le DataFrame principal.
-   Le script affiche également un DataFrame avec les emails déchiffrés
    pour vérification.

------------------------------------------------------------------------

## 👥 Rôles disponibles

  -----------------------------------------------------------------------
  Rôle                    Colonnes visibles     Niveau de protection
  ----------------------- --------------------- -------------------------
  analyste_marketing      id (pseudonymisé),    Moyen
                          montant, département  

  support_client_n1       id (pseudo), nom +    Élevé
                          prénom fake,          
                          téléphone masqué      

  admin_sécurité          Tout                  Aucun (full access)
  -----------------------------------------------------------------------

Vous pouvez tester :

``` python
get_Dataframe_View_By_Role(df, "Analyste_Marketing")
get_Dataframe_View_By_Role(df, "Support_Client_N1")
get_Dataframe_View_By_Role(df, "Admin_Sécurité")
```

------------------------------------------------------------------------

## 📦 requirements.txt

    pandas
    cryptography
    faker

------------------------------------------------------------------------

## 📜 Licence

Ce projet est fourni à titre éducatif pour démontrer les méthodes de
protection des données (RGPD).
