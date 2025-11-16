# 📘 README --- Flight Data 2024 · CSV vs Parquet Benchmark

## 🚀 Objectif du projet

Ce projet permet de :

-   Télécharger automatiquement le dataset **Flight Data 2024** depuis
    Kaggle\
-   Extraire le fichier CSV et supprimer les fichiers superflus\
-   Convertir le CSV en deux formats Parquet :
    -   **Parquet non compressé**
    -   **Parquet compressé (brotli)**
-   Comparer :
    -   ⏱ Temps de lecture\
    -   ⏱ Temps d'écriture\
    -   💾 Tailles des fichiers\
    -   ⏱ Lecture de colonnes sélectionnées (CSV vs Parquet)

Le script fournit un tableau comparatif propre pour toutes les étapes.

------------------------------------------------------------------------

## 📂 Structure du projet

    project/
    │── main.py
    │── requirements.txt
    │── README.md
    │── flight_data_2024.zip (auto-téléchargé si absent)
    └── data/
        │── flight_data_2024.csv
        │── flight_data_2024.parquet
        └── flight_data_2024_compressed.parquet

------------------------------------------------------------------------

## 🔧 Installation

### 1. Cloner le dépôt

``` bash
git clone <url_du_repo>
cd <repo>
```

### 2. Créer un environnement virtuel

``` bash
python -m venv venv
```

### 3. Activer l'environnement

**Windows**

``` bash
venv\Scripts\activate
```

**Linux/MacOS**

``` bash
source venv/bin/activate
```

### 4. Installer les dépendances

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 📦 Requirements (requirements.txt)

    pandas
    pyarrow
    fastparquet
    requests
    zipfile
    tqdm

------------------------------------------------------------------------

## 🛠 Exécution du script

``` bash
python main.py
```

------------------------------------------------------------------------

## 📊 Fonctionnalités détaillées

### ✔ Téléchargement automatique depuis Kaggle

### ✔ Extraction + nettoyage

### ✔ Benchmarks CSV vs Parquet

------------------------------------------------------------------------

## 🧪 Colonnes analysées

    op_carrier_fl_num
    origin_city_name

------------------------------------------------------------------------

## 📘 Variables importantes

``` python
PATHS = {
    "zip": "flight_data_2024.zip",
    "data_folder": "data",
    "csv": "data/flight_data_2024.csv",
    "parquet_raw": "data/flight_data_2024.parquet",
    "parquet_compressed": "data/flight_data_2024_compressed.parquet"
}
```

------------------------------------------------------------------------

## 🔍 Pourquoi ce projet est utile ?

Parce que Parquet :

-   compresse mieux\
-   se lit beaucoup plus vite\
-   est optimisé pour les colonnes\
-   est standard dans les pipelines modernes (Spark, Dask, Snowflake,
    BigQuery)

------------------------------------------------------------------------

## 📄 Licence

Libre de réutilisation et de modification.
