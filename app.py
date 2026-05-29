# app.py

import streamlit as st
import pandas as pd
from modules.data_loader import load_all_economic_data, DAFTAR_PROVINSI_URUT, DAFTAR_SEKTOR_BPS
from modules.analisis_sektoral import generate_klassen_chart
from modules.simulasi import hitung_target_triwulan
from modules.ai_engine import generate_executive_narrative, generate_ai_policy_matrix

# 1. INITIALIZE SETTINGS & EXECUTIVE NAVY THEME
st.set_page_config(
    page_title="Dashboard Analisis Ekonomi Daerah - Perencanaan Bappenas",
    page_icon="🏛️",
    layout="wide"
)

# Custom Styling CSS untuk Tampilan Clean, Rounded Cards, dan Font Profesional Komparabel Dashboard Menteri
st.markdown("""
    <style>
    .main { background-color: #F4F6F9; }
    div[data-testid="stMetricValue"] { font-size: 30px; font-weight: 700; color: #0A192F; }
    div[data-testid="stMetricDelta"] { font-size: 13px; font-weight: 500; }
    h1, h2, h3, h4 { color: #0A192F; font-family: 'Segoe UI', Arial, sans-serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #E2E8F0;
        border-radius: 6px 6px 0px 0px;
        padding: 12px 24px;
        color: #4A5568;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #0A192F !important; 
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_html=True)

# LOAD COMPREHENSIVE DATA ENGINE
df_master = load_all_economic_data()

# ==========================================
# HEADER UTAMA DASHBOARD
# ==========================================
st.markdown("""
<div style="background-color:#0A192F; padding:20px; border-radius:10px; margin-bottom:25px; display:flex; align-items:center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <div style="margin-right:25px;"><span style="font-size:45px;">🏛️</span></div>
    <div>
        <h1 style="color:#FFFFFF; margin:0; font-size:26px; font-weight:700; letter-spacing:0.5px;">DASHBOARD ANALISIS EKONOMI DAN SEKTOR UNGGULAN DAERAH BERBASIS AI</h1>
        <p style="color:#CBD5E1; margin:6px 0 0 0; font-size:14px; font-weight:400;">Kementerian Perencanaan Pembangunan Nasional / Bappenas — Alat Bantu Pengambilan Kebijakan Strategis Makro Sektoral</p>
    </div>
</div>
""", unsafe_html=True)

# ==========================================
# SIDEBAR FILTER INTERAKTIF
# ==========================================
st.sidebar.markdown("### 🔍 Parameter Perencanaan")
provinsi_pilihan = st.sidebar.selectbox("Pilih Wilayah / Provinsi:", options=DAFTAR_PROVINSI_URUT)
tahun_pilihan = st.sidebar.selectbox("Pilih Tahun Dokumen:", options=[2025, 2024, 2023])
sektor_pilihan = st.sidebar.selectbox("Fokus Analisis Komoditas:", options=DAFTAR_SEKTOR_BPS)

st.sidebar.divider()
st.sidebar.markdown("### 📈 target Laju Pertumbuhan (Full-Year)")
target_slider = st.sidebar.slider("Target Pertumbuhan RKP/RPJMD (%):", 3.5, 15.0, 5.2, step=0.1)
q1_aktual_input = st.sidebar.number_input("Realisasi Triwulan I (Q1) Eksisting (%):", min_value=0.5, max_value=15.0, value=4.5, step=0.1)

# FILTERING DATA PROSES
df_filtered_makro = df_master[(df_master['Provinsi'] == provinsi_pilihan) & (df_master['Tahun'] == tahun_pilihan)]
row_makro = df_filtered_makro.iloc[0] # Ambil baris pertama sebagai representasi indikator makro wilayah

# ==========================================
# LAYOUT KONTEN UTAMA VIA TABS INTERAKTIF
# ==========================================
tab_makro, tab_sektoral, tab_simulasi, tab_ai = st.tabs([
    "📊 PANEL INDIKATOR MAKRO & SOSIAL", 
    "🎯 PANEL ANALISIS SEKTORAL KLASSEN", 
    "🔄 PANEL SIMULASI RUN-RATE", 
    "🤖 INTERPRETASI & REKOMENDASI AI"
])

# ------------------------------------------
# TAB 1: INDIKATOR MAKRO & SOSIAL
# ------------------------------------------
with tab_makro:
    st.markdown(f"### Kinerja Indikator Makro & Sosial Provinsi {provinsi_pilihan} (Tahun {tahun_pilihan})")
    
    # PANEL MAKRO EKONOMI
    st.markdown("#### A. Koridor Indikator Makroekonomi")
    c_m1, c_m2, c_m3, c_m4, c_m5 = st.columns(5)
    c_m1.metric("Pertumbuhan Ekonomi", f"{row_makro['Pertumbuhan_Ekonomi']}%", delta="+0.21% YoY", delta_color="normal")
    c_m2.metric("PDRB Per Kapita", f"Rp {row_makro['PDRB_Per_Kapita']} Jt", delta="+Rp 1.8 Jt")
    c_m3.metric("Tingkat Inflasi", f"{row_makro['Inflasi']}%", delta="-0.3% MoM", delta_color="inverse")
    c_m4.metric("Investasi Daerah", f"Rp {row_makro['Investasi']} T", delta="+8.4% yoy")
    c_m5.metric("Ekspor Daerah", f"US$ {row_makro['Ekspor']} M", delta="+2.5% yoy")
    
    st.write("")
    
    # PANEL SOSIAL & KESEJAHTERAAN
    st.markdown("#### B. Koridor Indikator Kesejahteraan Sosial")
    c_s1, c_s2, c_s3, c_s4 = st.columns(4)
    c_s1.metric("Indeks Pembangunan Manusia", f"{row_makro['IPM']}", delta="Kategori Tinggi")
    c_s2.metric("Tingkat Kemiskinan", f"{row_makro['Kemiskinan']}%", delta="-0.42% Membaik", delta_color="inverse")
    c_s3.metric("Pengangguran Terbuka (TPT)", f"{row_makro['TPT']}%", delta="+0.11% Memburuk", delta_color="normal")
    c_s4.metric("Gini Ratio Daerah", f"{row_makro['Gini_Ratio']}", delta="-0.002 Kontraksi", delta_color="inverse")

# ------------------------------------------
# TAB 2: ANALISIS SEKTORAL
# ------------------------------------------
with tab_sektoral:
    st.markdown(f"### Pemetaan Struktur 17 Lapangan Usaha BPS di {provinsi_pilihan}")
    
    col_chart_box, col_table_box = st.columns([3, 2])
    
    with col_chart_box:
        # Panggil fungsi grafik eksekutif dari modul sektoral
        chart_fig = generate_klassen_chart(df_filtered_makro, provinsi_pilihan)
        st.plotly_chart(chart_fig, use_container_width=True)
        
    with col_table_box:
        st.markdown("##### 🏆 Sektor Komoditas Unggulan Utama (Kuadran I)")
        df_q1 = df_filtered_makro[df_filtered_makro['Kuadran'] == "Kuadran I"].sort_values(by="LQ", ascending=False)
        st.dataframe(
            df_q1[['Lapangan_Usaha', 'LQ', 'Shift_Share_D', 'Kontribusi_PDRB']], 
            hide_index=True, 
            use_container_width=True
        )
        
        with st.expander("🔍 Lihat Detail Ringkasan Sektor Tertekan / Tertinggal (Kuadran IV)"):
            df_q4 = df_filtered_makro[df_filtered_makro['Kuadran'] == "Kuadran IV"].sort_values(by="LQ")
            st.table(df_q4[['Lapangan_Usaha', 'LQ', 'Kontribusi_PDRB']])

# ------------------------------------------
# TAB 3: SIMULASI TARGET PERTUMBUHAN
# ------------------------------------------
with tab_simulasi:
    st.markdown("### 🔄 Analisis Run-Rate dan Simulasi Pencapaian Target Pertumbuhan Ekonomi")
    st.write("Simulasi otomatis untuk menentukan target spasial pendorong sisa triwulan (Q2, Q3, Q4) agar deviasi rencana tahunan tidak meleset.")
    
    target_q_sisa, status_teks, alert_tipe = hitung_target_triwulan(target_slider, q1_aktual_input)
    
    if alert_tipe == "error":
        st.error(f"🚨 Konsekuensi Perencanaan: **{status_teks}**")
    elif alert_tipe == "warning":
        st.warning(f"⚠️ Konsekuensi Perencanaan: **{status_teks}**")
    else:
        st.success(f"✅ Konsekuensi Perencanaan: **{status_teks}**")
        
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        st.markdown("##### ⚙️ Kebutuhan Laju Kuartalan:")
        st.write(f"* Target Pertumbuhan *Full Year* Akhir: **{target_slider}%**")
        st.write(f"* Realisasi Capaian Kuartal I (Q1): **{q1_aktual_input}%**")
        st.markdown(f"Untuk mengamankan target tahunan **{target_slider}%**, sisa laju pertumbuhan rata-rata pada **Triwulan II, III, dan IV** tidak boleh kurang dari **{target_q_sisa}%**.")
        
    with col_sim2:
        st.markdown("##### 📊 Progres Capaian Terhadap Target Tahunan:")
        persen_progres = min(max(float(q1_aktual_input / target_slider), 0.0), 1.0)
        st.progress(persen_progres)
        st.caption(f"Tingkat Pemenuhan Target Rencana Tahunan: {round(persen_progres * 100, 2)}%")

# ------------------------------------------
# TAB 4: INTERPRETASI & REKOMENDASI AI
# ------------------------------------------
with tab_ai:
    st.markdown("### 🤖 Analisis Kebijakan Cerdas Berbasis Sistem Pakar Perencanaan")
    
    # 1. Jalankan narasi otomatis eksekutif
    laporan_teks = generate_executive_narrative(row_makro, df_filtered_makro)
    st.markdown(laporan_teks)
    
    st.divider()
    
    # 2. Tombol Aksi Generator Rekomendasi Kebijakan
    st.markdown("#### 💡 Formulasi Matriks Rekomendasi Kebijakan AI")
    st.write("Tekan tombol di bawah ini untuk menurunkan keputusan taktis lintas sektoral berdasarkan data di atas:")
    
    if st.button("🚀 Rumuskan Rekomendasi Kebijakan"):
        with st.spinner("Sistem sedang mengalkulasi data makro-sosial ke dalam matriks perencanaan strategis..."):
            matriks_opsi = generate_ai_policy_matrix(row_makro)
            
            st.success("Matriks Kebijakan Strategis Berhasil Disusun!")
            
            col_rec1, col_rec2 = st.columns(2)
            with col_rec1:
                st.markdown("##### 🏛️ Sektor Fiskal & Penganggaran APBD")
                st.info(matriks_opsi['fiskal'])
                
                st.markdown("##### 💼 Hilirisasi Sektoral & Stimulus Investasi")
                st.info(matriks_opsi['sektoral'])
                
            with rec_col2 if 'rec_col2' in locals() else col_rec2:
                st.markdown("##### 👥 Program Penanggulangan Kemiskinan & Sosial")
                st.warning(matriks_opsi['sosial'])
                
                st.markdown("##### 🛒 Pengendalian Inflasi Sektor Pangan (TPID)")
                st.success(matriks_opsi['inflasi'])