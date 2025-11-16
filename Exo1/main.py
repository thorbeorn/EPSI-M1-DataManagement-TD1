import pandas as pd
import sys
import os
from time import perf_counter
import requests
from tqdm import tqdm
from zipfile import ZipFile

PATHS = {
    "zip": "flight_data_2024.zip",
    "data_folder": "data",
    "csv": "data/flight_data_2024.csv",
    "parquet_raw": "data/flight_data_2024.parquet",
    "parquet_compressed": "data/flight_data_2024_compressed.parquet"
}

DTYPE_colone = {
    24: str
}

Colone_Selected = ["op_carrier_fl_num", "origin_city_name"]
extra_Files = ["flight_data_2024_data_dictionary.csv", "flight_data_2024_sample.csv"]

def download(url, filename):
    with open(filename, 'wb') as f:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            tqdm_params = {
                'desc': url,
                'total': total,
                'miniters': 1,
                'unit': 'B',
                'unit_scale': True,
                'unit_divisor': 1024,
            }
            with tqdm(**tqdm_params) as pb:
                for chunk in r.iter_content(chunk_size=8192):
                    pb.update(len(chunk))
                    f.write(chunk)
def extract(path_ZIP, path_Folder):
    with ZipFile(path_ZIP) as zf:
        for member in tqdm(zf.infolist(), desc='Extracting '):
            try:
                zf.extract(member, path_Folder)
            except ZipFile.error as e:
                pass
def remove_Extra_Files(path_Folder, extra_Files):
    for file in extra_Files:
        os.remove(os.path.join(path_Folder, file))
def Get_Data_CSV_File():
    if os.path.exists(PATHS["csv"]):
        print("The CSV exist and don't need to be redownload")
    else:
        if not os.path.exists(PATHS["zip"]):
            download("https://www.kaggle.com/api/v1/datasets/download/hrishitpatil/flight-data-2024",PATHS["zip"])
        if not os.path.exists(PATHS["csv"]):
            extract(PATHS["zip"], PATHS["data_folder"])
            remove_Extra_Files(PATHS["data_folder"], extra_Files)
        
def read_CSV_to_Dataframe(path, colonetypes=DTYPE_colone):
    try:
        start_time = perf_counter()
        dataframe = pd.read_csv(path, dtype=colonetypes)
        end_time = perf_counter()
        duration = end_time - start_time
        print("CSV file read into DataFrame successfully.")
        return dataframe, duration
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None, None
def write_Dataframe_to_Parquet(dataframe, path, engine='pyarrow', compression='snappy', index=None, partition_cols=None):
    try:
        start_time = perf_counter()
        dataframe.to_parquet(path, engine=engine, compression=compression, index=index, partition_cols=partition_cols)
        end_time = perf_counter()
        print("DataFrame converted to Parquet successfully.")
        duration = end_time - start_time
        return duration
    except Exception as e:
        print(f"Error converting DataFrame to Parquet: {e}")
        return None
def read_Parquet_to_Dataframe(path):
    try:
        start_time = perf_counter()
        dataframe = pd.read_parquet(path, engine='pyarrow')
        end_time = perf_counter()
        duration = end_time - start_time
        print("Parquet file read into DataFrame successfully.")
        return dataframe, duration
    except Exception as e:
        print(f"Error converting DataFrame to Parquet: {e}")
        return None, None

def display_Comparison_Table(headers, rows):
    try:
        dataframe = pd.DataFrame(rows, columns=headers)
        print(dataframe.to_string(index=False))
        return True
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return False
def compare_File_sizes(path_CSV, path_parquet_Raw, path_parquet_Compressed):
    size_CSV = os.path.getsize(path_CSV) / 1_000_000
    size_Raw = os.path.getsize(path_parquet_Raw) / 1_000_000
    size_Comp = os.path.getsize(path_parquet_Compressed) / 1_000_000

    rows = [
        ["CSV", size_CSV, "-", "-"],
        [
            "Parquet (No Compression)",
            size_Raw,
            f"{(1 - size_Raw / size_CSV) * 100:.2f}%",
            "-"
        ],
        [
            "Parquet (Compressed)",
            size_Comp,
            f"{(1 - size_Comp / size_CSV) * 100:.2f}%",
            f"{(1 - size_Comp / size_CSV) * 100:.2f}%"
        ]
    ]

    headers = ["Format", "Size (MB)", "Gain vs CSV", "Gain vs Raw Parquet"]
    display_Comparison_Table(headers, rows)
def compare_Times(CSV_Time, raw_Time, compressed_Time):
    rows = [
        ["CSV", CSV_Time, "-", "-"],
        [
            "Parquet (No Compression)",
            raw_Time,
            CSV_Time - raw_Time,
            "-"
        ],
        [
            "Parquet (Compressed)",
            compressed_Time,
            CSV_Time - compressed_Time,
            raw_Time - compressed_Time
        ]
    ]

    headers = ["Format", "Load Time (s)", "Gain vs CSV", "Gain vs Raw Parquet"]
    display_Comparison_Table(headers, rows)

def read_Selected_Column_From_CSV(path, columns):
    try:
        start_time = perf_counter()
        dataframe = pd.read_csv(path, usecols=columns)
        end_time = perf_counter()
        duration = end_time - start_time
        print("CSV file read column into DataFrame successfully.")
        return dataframe, duration
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None, None
def read_Selected_Column_From_Parquet(path, columns, engine='auto'):
    try:
        start_time = perf_counter()
        dataframe = pd.read_parquet(path, engine=engine, columns=columns)
        end_time = perf_counter()
        duration = end_time - start_time
        print("Parquet file read column into DataFrame successfully.")
        return dataframe, duration
    except Exception as e:
        print(f"Error reading Parquet file: {e}")
        return None, None

def main():
    Get_Data_CSV_File()
    dataframe_CSV, duration_CSV_Read_To_Dataframe = read_CSV_to_Dataframe(PATHS["csv"], DTYPE_colone)
    if dataframe_CSV is not None:
        try:
            duration_Dataframe_To_Raw_Parquet_Write = write_Dataframe_to_Parquet(dataframe_CSV, PATHS["parquet_raw"], compression=None)
            duration_Dataframe_To_Compressed_Parquet_Write = write_Dataframe_to_Parquet(dataframe_CSV, PATHS["parquet_compressed"], compression='brotli')

            dataframe_Raw_Parquet, duration_Read_Raw_Parquet_To_Dataframe = read_Parquet_to_Dataframe(PATHS["parquet_raw"])
            dataframe_Raw_Parquet, duration_Read_Compressed_Parquet_To_Dataframe = read_Parquet_to_Dataframe(PATHS["parquet_compressed"])

            print("\n#########ALL File Comparison#########")
            print("\nCompare file size ->")
            compare_File_sizes(PATHS["csv"], PATHS["parquet_raw"], PATHS["parquet_compressed"])
            print("\nCompare write CSV to parquet time ->")
            compare_Times(duration_CSV_Read_To_Dataframe, duration_Dataframe_To_Raw_Parquet_Write, duration_Dataframe_To_Compressed_Parquet_Write)
            print("\nCompare Read parquet to dataframe time ->")
            compare_Times(duration_CSV_Read_To_Dataframe, duration_Read_Raw_Parquet_To_Dataframe, duration_Read_Compressed_Parquet_To_Dataframe)
        except Exception as e:
            sys.exit(f'Error Converting Dataframe to Parquet {e}. exiting program.')
    else:
        sys.exit('Error reading CSV file. exiting program.')

    try:
        dataframe_CSV_Column, duration_CSV_Column_Read_To_Dataframe = read_Selected_Column_From_CSV(PATHS["csv"], Colone_Selected)
        dataframe_Raw_Parquet_column, duration_Raw_Parquet_column_Read_To_Dataframe = read_Selected_Column_From_Parquet(PATHS["parquet_raw"], Colone_Selected)
        dataframe_Compressed_Parquet_column, duration_Compressed_Parquet_column_Read_To_Dataframe = read_Selected_Column_From_Parquet(PATHS["parquet_compressed"], Colone_Selected)
        if dataframe_CSV_Column is not None and dataframe_Raw_Parquet_column is not None and dataframe_Compressed_Parquet_column is not None:
            print("\n#########Load Column File Comparison#########")
            compare_Times(duration_CSV_Column_Read_To_Dataframe, duration_Raw_Parquet_column_Read_To_Dataframe, duration_Compressed_Parquet_column_Read_To_Dataframe)
        else:
            sys.exit('Error reading selected columns from file. exiting program.')
    except Exception as e:
        sys.exit(f'Error Converting Dataframe to Parquet {e}. exiting program.')
    
if __name__ == "__main__":
    main()