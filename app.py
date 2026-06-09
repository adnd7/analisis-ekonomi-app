# app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

st.set_page_config(page_title="Ekonomi Makro Daerah", layout="wide", page_icon="📍")

# ==============================================================================
# Bagian 1: SMART DATA LOADER (Auto-Detect CSV / Excel)
# ==============================================================================
@st.cache_data
def smart_load(filename_base):
    """Mencari file baik dalam format .xlsx maupun .csv di folder root maupun folder 'data'"""
    formats = ['.xlsx', '.csv'] 
    folders = ['', 'data/']
    
    for fldr in folders:
        for fmt in formats:
            path = f"{fldr}{filename_base}{fmt}"
            if os.path.exists(path):
                try:
                    if fmt == '.xlsx':
                        df = pd.read_excel(path, engine='openpyxl')
                    else:
                        try:
                            df = pd.read_csv(path, sep=";", encoding='cp1252', engine='python')
                            if len(df.columns) < 2:
                                df = pd.read_csv(path, sep=",", encoding='cp1252', engine='python')
                        except:
                            df = pd.read_csv(path, sep=",", encoding='cp1252', engine='python')
                    
                    df.columns = df.columns.astype(str).str.strip().str.lower()
                    return df
                except Exception as e:
                    continue
                    
    return pd.DataFrame()

def load_data_aman(provinsi, tahun):
    df_all = smart_load("data_ekonomi")
    if df_all is None or df_all.empty:
        return pd.DataFrame(columns=['provinsi', 'tahun', 'klasifikasi', 'lpe_tw1', 'lpe_tw2', 'lpe_tw3', 'lpe_tw4', 'lpe_ctc'])

    try:
        df_all['provinsi'] = df_all['provinsi'].astype(str).str.strip()
        df_all['tahun'] = pd.to_numeric(df_all['tahun'], errors='coerce').fillna(0).astype(int)
        
        kolom_angka = [
            'lpe_tw1', 'lpe_tw2', 'lpe_tw3', 'lpe_tw4', 'lpe_ctc', 
            'kontribusi', 'pdrb_perkapita', 'inflasi', 'pma', 'pmdn', 
            'ipm', 'kemiskinan', 'tpt', 'gini'
        ]
        
        for kol in kolom_angka:
            if kol in df_all.columns:
                df_all[kol] = df_all[kol].astype(str).str.strip().replace(['-', '', 'nan', 'none', 'None'], np.nan)
                df_all[kol] = df_all[kol].str.replace(',', '.', regex=False)
                df_all[kol] = pd.to_numeric(df_all[kol], errors='coerce')
        
        df_filtered = df_all[df_all['tahun'] == int(tahun)]
        return df_filtered.reset_index(drop=True) if not df_filtered.empty else pd.DataFrame(columns=df_all.columns)
            
    except Exception as e:
        return pd.DataFrame(columns=['provinsi', 'tahun', 'klasifikasi', 'lpe_tw1', 'lpe_tw2', 'lpe_tw3', 'lpe_tw4', 'lpe_ctc'])

def load_data_sektoral_aman(provinsi):
    df_sektoral = smart_load("data_sektoral")
    if df_sektoral is None or df_sektoral.empty: return pd.DataFrame()
    try:
        df_sektoral['provinsi'] = df_sektoral['provinsi'].astype(str).str.strip()
        df_filtered = df_sektoral[df_sektoral['provinsi'].str.lower().str.strip() == str(provinsi).lower().strip()]
        return df_filtered.reset_index(drop=True) if not df_filtered.empty else pd.DataFrame(columns=df_sektoral.columns)
    except:
        return pd.DataFrame()

def load_data_struktur_aman(provinsi):
    df_all = smart_load("data_struktur")
    if df_all is None or df_all.empty: return pd.DataFrame()
    try:
        df_all['provinsi'] = df_all['provinsi'].astype(str).str.strip()
        df_filtered = df_all[df_all['provinsi'].str.lower().str.strip() == str(provinsi).lower().strip()]
        return df_filtered.reset_index(drop=True) if not df_filtered.empty else pd.DataFrame(columns=df_all.columns)
    except:
        return pd.DataFrame()

# ==============================================================================
# Bagian 2: VISUALISASI CHART & PETA
#
