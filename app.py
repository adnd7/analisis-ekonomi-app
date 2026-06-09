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
                df_all[kol] = df_all[kol].astype(str).str.strip().replace(['-', '', 'nan', 'None'], np.nan)
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
# ==============================================================================
WARNA_SEKTOR_GLOBAL = {
    "pertanian": "#22C55E", "pertambangan": "#D97706", "industri": "#6B21A8",
    "pengadaan listrik": "#EA580C", "pengadaan air": "#1E3A1E", "konstruksi": "#8B5CF6",
    "perdagangan": "#1D4ED8", "transportasi": "#FBBF24", "akmamin": "#F472B6",
    "informasi dan komunikasi": "#3B82F6", "jasa keuangan": "#EC4899", "real estat": "#6B7280",
    "jasa perusahaan": "#9CA3AF", "adm. pemerintahan": "#DC2626", "jasa pendidikan": "#0D9488",
    "jasa kesehatan": "#78350F", "jasa lainnya": "#D97706"
}

def get_warna_sektor_map(df_column):
    return {sektor: WARNA_SEKTOR_GLOBAL.get(str(sektor).lower(), "#6B7280") for sektor in df_column.unique()}

def buat_bar_chart_makro(df_aktif, tipe_chart):
    if df_aktif is None or df_aktif.empty:
        st.warning("Data makro untuk grafik batang kosong.")
        return

    if tipe_chart == "Pertumbuhan Ekonomi":
        if "lpe_ctc" not in df_aktif.columns: return st.warning("Kolom lpe_ctc tidak ditemukan.")
        df_sorted = df_aktif.dropna(subset=["lpe_ctc"]).sort_values(by="lpe_ctc", ascending=True)
        fig = px.bar(df_sorted, x="lpe_ctc", y="provinsi", orientation='h', labels={"lpe_ctc": "LPE c-to-c (%)", "provinsi": "Provinsi"}, color="lpe_ctc", color_continuous_scale="Viridis")
    else:
        if "kontribusi" not in df_aktif.columns: return st.warning("Kolom kontribusi tidak ditemukan.")
        df_sorted = df_aktif.dropna(subset=["kontribusi"]).sort_values(by="kontribusi", ascending=True)
        fig = px.bar(df_sorted, x="kontribusi", y="provinsi", orientation='h', labels={"kontribusi": "Kontribusi PDRB (%)", "provinsi": "Provinsi"}, color="kontribusi", color_continuous_scale="Cividis")
        
    fig.update_layout(height=600, margin={"r":10,"t":10,"l":10,"b":10})
    st.plotly_chart(fig, use_container_width=True)

def buat_peta_klasifikasi(df_aktif):
    if df_aktif is None or df_aktif.empty or "klasifikasi" not in df_aktif.columns:
        st.warning("Data kosong atau kolom klasifikasi tidak ditemukan, peta tidak dapat dimuat.")
        return
        
    try:
        geojson_path = "data/indonesia_provinces.geojson" if os.path.exists("data/indonesia_provinces.geojson") else "indonesia_provinces.geojson"
        if not os.path.exists(geojson_path):
            st.info("🗺️ *[File GeoJSON batas wilayah tidak ditemukan]*")
            return
        with open(geojson_path, "r") as f:
            geojson_indonesia = json.load(f)
            
        df_peta = df_aktif.copy()
        df_peta['provinsi'] = df_peta['provinsi'].replace({
            "DI Yogyakarta": "Daerah Istimewa Yogyakarta",
            "D.I. Yogyakarta": "Daerah Istimewa Yogyakarta"
        })
            
        fig = px.choropleth_mapbox(
            df_peta, geojson=geojson_indonesia, locations="provinsi", featureidkey="properties.PROVINSI", color="klasifikasi",                  
            color_discrete_map={                
                "Daerah Maju dan Cepat Tumbuh": "#3797A4",  
                "Daerah Berkembang Cepat": "#8BCDCD",       
                "Daerah Maju tapi Tertekan": "#CEE397",    
                "Daerah Relatif Tertinggal": "#FCF876"      
            },
            mapbox_style="carto-positron", center={"lat": -2.5, "lon": 118.0}, zoom=3.5, opacity=0.8, labels={"klasifikasi": "Status Klasifikasi"}
        )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.info(f"🗺️ *[Gagal memuat peta GeoJSON. Error: {e}]*")

def buat_line_growth(provinsi):
    df_raw = smart_load("data_ekonomi")
    if df_raw is None or df_raw.empty: return
    try:
        df_raw['provinsi'] = df_raw['provinsi'].astype(str).str.strip()
        df_prov = df_raw[df_raw['provinsi'].str.lower().str.strip() == provinsi.lower().strip()].sort_values(by="tahun")
        
        if df_prov.empty:
            st.warning(f"Data tren historis untuk {provinsi} tidak ditemukan.")
            return
            
        df_prov['lpe_ctc'] = pd.to_numeric(df_prov['lpe_ctc'].astype(str).str.replace(',', '.', regex=False).str.strip().replace('-', np.nan), errors='coerce')
        df_prov['inflasi'] = pd.to_numeric(df_prov['inflasi'].astype(str).str.replace(',', '.', regex=False).str.strip().replace('-', np.nan), errors='coerce')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_prov['tahun'], y=df_prov['lpe_ctc'], name=f"{provinsi} (c-to-c)", mode='lines+markers', line=dict(width=3, color='#1D4ED8')))
        fig.add_trace(go.Scatter(x=df_prov['tahun'], y=df_prov['inflasi'], name='Inflasi Wilayah', mode='lines+markers', line=dict(dash='dash', color='#DC2626')))
        
        fig.update_layout(xaxis=dict(dtick=1, type='category'), xaxis_title="Tahun", yaxis_title="Persentase (%)", margin={"r":10,"t":30,"l":10,"b":10}, legend_orientation="h")
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.error("Gagal memuat tren pertumbuhan makro historis.")

def buat_area_struktur(df_aktif):
    if df_aktif is not None and not df_aktif.empty and 'sektor' in df_aktif.columns and 'kontribusi_sektor' in df_aktif.columns:
        df_display = df_aktif.sort_values(by="tahun")
        warna_map = get_warna_sektor_map(df_display['sektor'])
        
        fig = px.area(
            df_display, x="tahun", y="kontribusi_sektor", color="sektor", line_group="sektor", color_discrete_map=warna_map,
            labels={"tahun": "Tahun Analisis", "kontribusi_sektor": "Kontribusi Sektor PDRB (%)"}
        )
        fig.update_layout(showlegend=True, xaxis=dict(dtick=1, type='category'), margin={"r": 10, "t": 10, "l": 10, "b": 10})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 *[Grafik Tren Area Struktur Ekonomi belum dapat dimuat karena data kosong]*")

def buat_scatter_sektoral(df_aktif, jenis_analisis):
    if df_aktif is None or df_aktif.empty:
        st.info(f"🎯 *[Grafik Scatter Plot {jenis_analisis} akan muncul otomatis setelah data sektoral provinsi termuat]*")
        return

    if jenis_analisis == "Overlay":
        judul_full = 'Scatter Plot "Overlay (MRP - LQ) 2025"'
        help_teks = "Metode Overlay..."
        kriteria_teks = "- Kriteria I (Rasio Pertumbuhan > 1 dan LQ > 1): Sektor Unggulan...\n"
        col_x, col_y = "lq_2025", "rps_2025"
        garis_x, garis_y = 1.0, 1.0  
        labels_x, labels_y = "Location Quotient (LQ)", "Rasio Pertumbuhan Sektoral (RPS)"

    elif jenis_analisis == "Shift Share":
        judul_full = 'Scatter Plot "Shift Share 2015/2025"'
        help_teks = "Metode Shift Share..."
        kriteria_teks = "- Kriteria I (RS + IM +): Sektor Tumbuh Pesat...\n"
        col_x, col_y = "im_2025", "rs_2025"
        garis_x, garis_y = 0.0, 0.0  
        labels_x, labels_y = "Regional Share (RS)", "Industrial Mix (IM)"

    else:  
        judul_full = 'Scatter Plot "Tipologi Klassen Rata-Rata 2022-2025"'
        help_teks = "Tipologi Klassen..."
        kriteria_teks = "- Kriteria I (Pertumbuhan > Nas & Kontribusi > Nas): Sektor Andalan...\n"
        col_x, col_y = "kontribusi_2025", "pertumbuhan_2025"
        garis_x, garis_y = 5.6, 5.1  
        labels_x, labels_y = "Rata-Rata Kontribusi (%)", "Rata-Rata Pertumbuhan (%)"

    if col_x not in df_aktif.columns or col_y not in df_aktif.columns:
        return st.warning(f"Kolom {col_x} atau {col_y} tidak ditemukan pada data sektoral.")

    st.markdown(f"##### {judul_full}", help=help_teks)
    col_grafik, col_narasi = st.columns([2, 1])
    
    with col_grafik:
