# modules/data_loader.py

import pandas as pd
import numpy as np
import os

def load_data_aman(provinsi, tahun):
    """
    1. Membaca data utama dari data_ekonomi.csv untuk TAHUN terpilih (Seluruh Provinsi).
    """
    if os.path.exists("data/data_ekonomi.csv"):
        path_file = "data/data_ekonomi.csv"
    elif os.path.exists("data_ekonomi.csv"):
        path_file = "data_ekonomi.csv"
    else:
        return pd.DataFrame(columns=['provinsi', 'tahun', 'klasifikasi', 'lpe_tw1', 'lpe_tw2', 'lpe_tw3', 'lpe_tw4', 'lpe_ctc'])

    try:
        df_all = pd.read_csv(path_file, sep=";")
        
        # Penanganan jika baris header bergeser
        if 'provinsi' not in df_all.columns:
            if 'Unnamed: 0' in df_all.columns:
                df_all = df_all.rename(columns={'Unnamed: 0': 'provinsi'})
            else:
                df_all.rename(columns={df_all.columns[0]: 'provinsi'}, inplace=True)
        
        # Bersihkan spasi nama provinsi
        df_all['provinsi'] = df_all['provinsi'].astype(str).str.strip()
        
        # Pastikan kolom tahun menjadi integer bulat
        df_all['tahun'] = pd.to_numeric(df_all['tahun'], errors='coerce').fillna(0).astype(int)
        
        # Paksa kolom-kolom indikator menjadi Angka murni (Float)
        kolom_angka = [
            'lpe_tw1', 'lpe_tw2', 'lpe_tw3', 'lpe_tw4', 'lpe_ctc', 
            'kontribusi', 'pdrb_perkapita', 'inflasi', 'ipm', 'kemiskinan', 'tpt', 'gini'
        ]
        
        for kol in kolom_angka:
            if kol in df_all.columns:
                df_all[kol] = df_all[kol].astype(str).str.replace(',', '.', regex=False)
                df_all[kol] = pd.to_numeric(df_all[kol], errors='coerce')
        
        # Saring berdasarkan tahun terpilih
        df_filtered = df_all[df_all['tahun'] == int(tahun)]
        
        return df_filtered if not df_filtered.empty else pd.DataFrame(columns=df_all.columns)
            
    except Exception as e:
        print(f"❌ Error pada load_data_aman: {e}")
        return pd.DataFrame(columns=['provinsi', 'tahun', 'klasifikasi', 'lpe_tw1', 'lpe_tw2', 'lpe_tw3', 'lpe_tw4', 'lpe_ctc'])

def load_data_sektoral_aman(provinsi):
    """
    2. Membaca data cross-section 17 sektor untuk provinsi terpilih dari data_sektoral.csv.
    """
    if os.path.exists("data/data_sektoral.csv"):
        path_file = "data/data_sektoral.csv"
    elif os.path.exists("data_sektoral.csv"):
        path_file = "data_sektoral.csv"
    else:
        return pd.DataFrame()

    try:
        df_sektoral = pd.read_csv(path_file, sep=";")
        df_sektoral['provinsi'] = df_sektoral['provinsi'].astype(str).str.strip()
        df_filtered = df_sektoral[df_sektoral['provinsi'] == str(provinsi).strip()]
        return df_filtered if not df_filtered.empty else pd.DataFrame(columns=df_sektoral.columns)
    except Exception as e:
        print(f"❌ Error Sektoral: {e}")
        return pd.DataFrame()

def load_data_struktur_aman(provinsi):
    """
    3. Membaca tren historis kontribusi 17 sektor dari data_struktur.csv.
    """
    if os.path.exists("data/data_struktur.csv"):
        path_file = "data/data_struktur.csv"
    elif os.path.exists("data_struktur.csv"):
        path_file = "data_struktur.csv"
    else:
        return pd.DataFrame()

    try:
        df_all = pd.read_csv(path_file, sep=";")
        df_all['provinsi'] = df_all['provinsi'].astype(str).str.strip()
        df_filtered = df_all[df_all['provinsi'] == str(provinsi).strip()]
        return df_filtered if not df_filtered.empty else pd.DataFrame(columns=df_all.columns)
    except Exception as e:
        print(f"❌ Error Struktur: {e}")
        return pd.DataFrame()
