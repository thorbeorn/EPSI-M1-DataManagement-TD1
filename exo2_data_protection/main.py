import pandas as pd
from difflib import get_close_matches
from faker import Faker
from cryptography.fernet import Fernet
import os

fake = Faker(locale="fr_FR")

PATHS = {
    "key": "mail.key",
    "parquet": "clients_data.parquet"
}

city_Department_Code = {
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

def read_Parquet_File(path, engine='auto', columns=None):
    try:
        dataframe = pd.read_parquet(path, engine=engine, columns=columns)
        print("parquet file read into DataFrame successfully.")
        return dataframe
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

def generate_key(path):
    try:
        key = Fernet.generate_key()
        with open(path, "wb") as f:
            f.write(key)
        return key
    except Exception:
        raise ValueError(f"Unable to generate key at {path}")
def load_key(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception:
        raise ValueError(f"Unable to load key from {path}")

def encrypt_Column(dataframe, column, key: bytes | None = None):
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
def decrypt_Column(dataframe, column, key: bytes | None = None):
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
            return val
    dataframe[column] = dataframe[column].apply(_decrypt)
    return dataframe

def faking_Column(dataframe, column, fake_Command):
    if dataframe is None or column not in dataframe.columns:
        raise ValueError(f"Invalid DataFrame or column '{column}' not found.")
    if not callable(fake_Command):
        raise TypeError("fake_Command must be a callable function.")
    dataframe[column] = [fake_Command() for _ in range(len(dataframe))]
    return dataframe
def masking_Phone_Column(dataframe, column):
    if dataframe is None or column not in dataframe.columns:
        raise ValueError(f"Invalid DataFrame or column '{column}' not found.")
    def mask_phone(num):
        if isinstance(num, str) and len(num) >= 2:
            return num[:2] + "X" * (len(num) - 2)
        else:
            return num
    dataframe[column] = dataframe[column].apply(mask_phone)   
    return dataframe
def anonymize_City_Column(dataframe, column):
    if dataframe is None or column not in dataframe.columns:
        raise ValueError(f"Invalid DataFrame or column '{column}' not found.")
    def city_To_Department_Code(city): 
        if not isinstance(city, str):
            return None
        if city in city_Department_Code:
            return city_Department_Code[city]
        return city_Department_Code[get_close_matches(city, city_Department_Code.keys(), n=1, cutoff=0.6)[0] if get_close_matches(city, city_Department_Code.keys(), n=1, cutoff=0.6) else None]
    dataframe[column] = dataframe[column].apply(city_To_Department_Code)
    return dataframe

def get_Dataframe_View_By_Role(dataframe, role):
    match role.lower():
        case "analyste_marketing" :
            dataframe_Temp = dataframe[['id_client', 'montant_achat', 'ville_résidence']]
            dataframe_Temp = faking_Column(dataframe_Temp, "id_client", lambda: fake.random_number(digits=5))
            dataframe_Temp = anonymize_City_Column(dataframe_Temp, "ville_résidence")
            return dataframe_Temp
        case "support_client_n1" :
            dataframe_Temp = dataframe[['id_client', 'nom', 'prénom', 'téléphone', 'montant_achat']] 
            dataframe_Temp = faking_Column(dataframe_Temp, "id_client", lambda: fake.random_number(digits=5))
            dataframe_Temp = faking_Column(dataframe_Temp, "prénom", lambda: fake.first_name())
            dataframe_Temp = faking_Column(dataframe_Temp, "nom", lambda: fake.last_name())
            dataframe_Temp = masking_Phone_Column(dataframe_Temp, "téléphone")
            return dataframe_Temp
        case "admin_sécurité" :
            return dataframe
def process_All_Column_To_Dataframe(dataframe):
    if not os.path.exists(PATHS["key"]):
        generate_key(PATHS["key"])
    key = load_key(PATHS["key"])
    dataframe = faking_Column(dataframe, "prénom", lambda: fake.first_name())
    dataframe = faking_Column(dataframe, "nom", lambda: fake.last_name())
    dataframe = masking_Phone_Column(dataframe, "téléphone")
    dataframe = anonymize_City_Column(dataframe, "ville_résidence")
    dataframe = encrypt_Column(dataframe, "email", key)
    dataframe = faking_Column(dataframe, "id_client", lambda: fake.random_number(digits=5))
    return dataframe

if __name__ == "__main__":
    dataframe = read_Parquet_File(PATHS["parquet"])
    dataframep1et2 = process_All_Column_To_Dataframe(dataframe)
    key = load_key(PATHS["key"])
    print("Dataframe with all column processed")
    print(dataframep1et2)
    print("Dataframe with email decrypted for check key encryption method")
    print(decrypt_Column(dataframep1et2, "email", key))
    print("#####Analyste_Marketing#####")
    print(get_Dataframe_View_By_Role(dataframe, "Analyste_Marketing"))
    print("#####Support_Client_N1#####")
    print(get_Dataframe_View_By_Role(dataframe, "Support_Client_N1"))
    print("#####Admin_Sécurité#####")
    print(get_Dataframe_View_By_Role(dataframe, "Admin_Sécurité"))