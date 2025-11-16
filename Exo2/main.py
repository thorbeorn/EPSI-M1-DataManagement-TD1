import pandas as pd
from difflib import get_close_matches
from faker import Faker
from cryptography.fernet import Fernet
import os

fake = Faker(locale="fr_FR")
parquetpath = "clients_data.parquet"
keypath = "secret.key"
ville_to_dept = {
    "Paris": "75",
    "Marseille": "13",
    "Lyon": "69",
    "Toulouse": "31",
    "Nice": "06",
    "Nantes": "44",
    "Strasbourg": "67",
    "Montpellier": "34",
    "Bordeaux": "33",
    "Lille": "59",
}

def readParquetFile(path, engine='auto', columns=None):
    try:
        dataframe = pd.read_parquet(path, engine=engine, columns=columns)
        print("parquet file read into DataFrame successfully.")
        return dataframe
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def generate_key(path: str = "secret.key") -> bytes:
    """Génère une clé Fernet et l'écrit dans le fichier `path`. Retourne la clé."""
    key = Fernet.generate_key()
    with open(path, "wb") as f:
        f.write(key)
    return key
def load_key(path: str = "secret.key") -> bytes:
    """Charge la clé depuis `path`. Lève FileNotFoundError si absent."""
    with open(path, "rb") as f:
        return f.read()
def encryptEmailColumn(dataframe: pd.DataFrame, column: str = "email", key: bytes | None = None) -> pd.DataFrame:
    """Chiffre chaque valeur de la colonne `column` en place en utilisant la clé Fernet fournie.

    - Les valeurs NaN sont laissées inchangées.
    - La fonction retourne le DataFrame modifié (même objet).
    """
    if dataframe is None or column not in dataframe.columns:
        raise ValueError(f"Invalid DataFrame or column '{column}' not found.")

    if key is None:
        raise ValueError("A cryptographic key must be provided.")

    f = Fernet(key)

    def _encrypt(val):
        if pd.isna(val):
            return val
        return f.encrypt(str(val).encode()).decode()

    dataframe[column] = dataframe[column].apply(_encrypt)
    return dataframe
def decryptEmailColumn(dataframe: pd.DataFrame, column: str = "email", key: bytes | None = None) -> pd.DataFrame:
    """Déchiffre chaque valeur de la colonne `column` en place en utilisant la clé Fernet fournie.
    Si une valeur ne peut pas être déchiffrée, elle est laissée telle quelle.
    """
    if dataframe is None or column not in dataframe.columns:
        raise ValueError(f"Invalid DataFrame or column '{column}' not found.")

    if key is None:
        raise ValueError("A cryptographic key must be provided.")

    f = Fernet(key)

    def _decrypt(val):
        if pd.isna(val):
            return val
        try:
            return f.decrypt(val.encode()).decode()
        except Exception:
            # si la valeur n'est pas un token Fernet valide, la laisser
            return val

    dataframe[column] = dataframe[column].apply(_decrypt)
    return dataframe
def maskParquetData(dataframe, information, column):
    if dataframe is None or column not in dataframe.columns:
        print(f"Invalid DataFrame or column '{column}' not found.")
        return dataframe

    match information.lower():
        case "prenom":
            dataframe[column] = [fake.first_name() for _ in range(len(dataframe))]
        case "nom":
            dataframe[column] = [fake.last_name() for _ in range(len(dataframe))]
        case "telephone":
            def mask_phone(num):
                if isinstance(num, str) and len(num) >= 4:
                    return num[:4] + "X" * (len(num) - 4)
                else:
                    return num
            dataframe[column] = dataframe[column].apply(mask_phone)
        case _:
            print(f"Information type '{information}' not recognized.")
    
    return dataframe
def anonymizeParquetData(dataframe, information, column):
    if dataframe is None or column not in dataframe.columns:
        print(f"Invalid DataFrame or column '{column}' not found.")
        return dataframe

    match information.lower():
        case "ville":
            def map_to_dept(ville):
                if not isinstance(ville, str):
                    return None
                if ville in ville_to_dept:
                    return ville_to_dept[ville]
                return ville_to_dept[get_close_matches(ville, ville_to_dept.keys(), n=1, cutoff=0.6)[0] if get_close_matches(ville, ville_to_dept.keys(), n=1, cutoff=0.6) else None]
            dataframe[column] = dataframe[column].apply(map_to_dept)
        case _:
            print(f"Information type '{information}' not recognized.")
    
    return dataframe
def pseudomizeParquetData(dataframe, information, column):
    if dataframe is None or column not in dataframe.columns:
        print(f"Invalid DataFrame or column '{column}' not found.")
        return dataframe

    match information.lower():
        case "id":
            def pseudomize_id_client(id_client):
                if isinstance(id_client, int):
                    return fake.random_number(digits=5)
                else:
                    return fake.random_number(digits=5)
            dataframe[column] = dataframe[column].apply(pseudomize_id_client)
        case _:
            print(f"Information type '{information}' not recognized.")
    
    return dataframe

def getDataByRole(dataframe, role):
    match role.lower():
        case "analyste_marketing" :
            dftemp = dataframe[['id_client', 'montant_achat', 'ville_résidence']]
            dftemp = pseudomizeParquetData(dftemp.copy(), "id", "id_client")
            dftemp =  anonymizeParquetData(dftemp.copy(), "Ville", "ville_résidence")
            return dftemp
        case "support_client_n1" :
            dftemp = dataframe[['id_client', 'nom', 'prénom', 'téléphone', 'montant_achat']] 
            dftemp = pseudomizeParquetData(dftemp.copy(), "id", "id_client")
            dftemp = maskParquetData(dftemp.copy(), "Prenom", "prénom")
            dftemp = maskParquetData(dftemp.copy(), "Nom", "nom")
            dftemp = maskParquetData(dftemp.copy(), "Telephone", "téléphone")
            return dftemp
        case "admin_sécurité" :
            return dataframe

def partie1Et2():
    generate_key("p12_" + keypath)

    df = readParquetFile(parquetpath)
    print(df)

    df = maskParquetData(df, "Prenom", "prénom")
    df = maskParquetData(df, "Nom", "nom")
    df = maskParquetData(df, "Telephone", "téléphone")
    print(df)

    df = anonymizeParquetData(df, "Ville", "ville_résidence")
    print(df)

    key = load_key("p12_" + keypath)
    df = encryptEmailColumn(df, "email", key)
    print(df)
    df = decryptEmailColumn(df, "email", key)
    print(df)

    df = pseudomizeParquetData(df, "id", "id_client")
    print(df)
    return df
def partie3():
    df = readParquetFile(parquetpath)

    print("#####Analyste_Marketing#####")
    print(getDataByRole(df, "Analyste_Marketing"))
    print("#####Support_Client_N1#####")
    print(getDataByRole(df, "Support_Client_N1"))
    print("#####Admin_Sécurité#####")
    print(getDataByRole(df, "Admin_Sécurité"))

partie1Et2()
partie3()