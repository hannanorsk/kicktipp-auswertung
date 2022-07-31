import pandas as pd


def excel_to_dataframe(xlsx_path, sheet_name):
    '''
    Dieser Funktion kann eine Excel übergeben werden und sie gibt ein Dataframe zurück. Den konkreten Dateipfad der Funktion mitgeben. Z.B. excel_to_dataframe('test/Kürzel_Mannschaft.xlsx')
    '''
    
    df = pd.read_excel(xlsx_path, sheet_name)
    return df

def csv_to_dataframe(csv_path):
    '''
    Dieser Funktion kann eine CSV übergeben werden und sie gibt ein Dataframe zurück. Den konkreten Dateipfad der Funktion mitgeben. Z.B. csv_to_dataframe('test/Kürzel_Mannschaft.csv')
    '''

    df = pd.read_csv(csv_path)
    return df

