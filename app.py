# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Menggunakan data loader aman dari modules
from modules.data_loader import load_data_aman, load_data_sektoral_aman, load_data_struktur_aman

# Impor fungsi visualisasi dari modules/analisis_sektoral.py
from modules.analisis_sektoral import (
    buat_bar_chart_makro, buat_peta_klasifikasi, 
    buat_line_growth, buat_area_struktur, buat_scatter_sektoral
)

# Pengaturan Dasar Halaman Eksekutif
st.set_page_config(page_title="Ekonomi Makro Daerah", layout="wide")

# Title Dashboard Utama
st.title("🏛️ Dashboard Ekonomi Makro Daerah")
st.markdown("---")

# Pilihan Filter Diletakkan di Atas (Bukan di Sidebar)
st.markdown("#### Pilihan Filter Analisis")
col_provinsi, col_tahun = st.columns(2)

with col_provinsi:
    # Daftar Nama 38 Provinsi Asli Indonesia Secara Urut dan Presisi
    list_provinsi = [
        "Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Jambi", 
        "Sumatera Selatan", "Bengkulu", "Lampung", "Kepulauan Bangka Belitung", 
        "Kepulauan Riau", "DKI Jakarta", "Jawa Barat", "Jawa Tengah", 
        "DI Yogyakarta", "Jawa Timur", "Banten", "Bali", "Nusa Tenggara Barat", 
        "Nusa Tenggara Timur", "Kalimantan Barat", "Kalimantan Tengah", 
        "Kalimantan Selatan", "Kalimantan Timur", "Kalimantan Utara", 
        "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan", 
        "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat", "Maluku", 
        "Maluku Utara", "Papua Barat", "Papua Barat Daya", "Papua", 
        "Papua Selatan", "Papua Tengah", "Papua Pegunungan"
    ]
    provinsi_terpilih = st.selectbox("Pilih Wilayah Analisis:", list_provinsi)

with col_tahun:
    tahun_terpilih = st.selectbox("Tahun Analisis:", list(range(2011, 2026)), index=14) # Default ke 2025 sesuai data sektoral

st.markdown("---")

# Perhatian: load_data_aman harus mengembalikan seluruh DataFrame tahun terkait 
# agar bisa dipakai visualisasi bar chart makro 38 provinsi.
df_all_prov = load_data_aman(provinsi_terpilih, tahun_terpilih) 
df_sektoral_aktif = load_data_sektoral_aman(provinsi_terpilih)
df_struktur_aktif = load_data_struktur_aman(provinsi_terpilih)

# if not df_all_prov.empty:
#    df_all_prov['tahun'] = df_all_prov['tahun'].astype(int)

# Ambil baris spesifik untuk Provinsi & Tahun terpilih demi keperluan pengisian Metric Box
df_row = df_all_prov[(df_all_prov['provinsi'] == provinsi_terpilih) & (df_all_prov['tahun'] == int(tahun_terpilih))]

# Jika data baris ditemukan, ubah menjadi tipe Series/Dictionary
if not df_row.empty:
    df_active_dict = df_row.iloc[0].to_dict()
else:
    df_active_dict = {}

# ==========================================
# URUTAN 1: KONDISI EKONOMI MAKRO DAERAH 38 PROVINSI
# ==========================================
st.header("KONDISI EKONOMI MAKRO DAERAH 38 PROVINSI")

# 1. Baris Pertama: Dibagi menjadi 2 Kolom untuk Grafik Batang 38 Provinsi
col_Grafik1, col_Grafik2 = st.columns(2)

with col_Grafik1:
    st.subheader(f"Laju Pertumbuhan Ekonomi ({tahun_terpilih})")
    # Mengirimkan seluruh dataframe agar barchart memuat 38 provinsi
    buat_bar_chart_makro(df_all_prov, "Pertumbuhan Ekonomi")

with col_Grafik2:
    st.subheader(f"Kontribusi PDRB terhadap Nasional ({tahun_terpilih})")
    buat_bar_chart_makro(df_all_prov, "Kontribusi PDRB")

# 2. Baris Kedua: Peta Sebaran Wilayah dibuat Melebar Penuh (Wide)
st.subheader(f"🗺️ Sebaran Klasifikasi Wilayah")
buat_peta_klasifikasi(df_all_prov)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# URUTAN 2: KINERJA INDIKATOR EKONOMI DAN SOSIAL
# ==========================================
st.header(f"KINERJA INDIKATOR EKONOMI DAN SOSIAL {provinsi_terpilih.upper()}")

# 1. Pertumbuhan Ekonomi YoY
st.markdown("#### Pertumbuhan Ekonomi (YoY)")
buat_line_growth(df_all_prov, provinsi_terpilih)

# 5 Kotak capaian kuartal (Kuartal terakhir c-to-c warna gelap)
st.write(f"**Capaian Laju Pertumbuhan Ekonomi Makro Daerah**")
q1, q2, q3, q4, q5 = st.columns(5)
q1.metric("TW I YoY", df_active_dict.get("lpe_tw1", "-"))
q2.metric("TW II YoY", df_active_dict.get("lpe_tw2", "-"))
q3.metric("TW III YoY", df_active_dict.get("lpe_tw3", "-"))
q4.metric("TW IV YoY", df_active_dict.get("lpe_tw4", "-"))

capaian_ctc = df_active_dict.get("lpe_ctc", "-")

# Kotak c-to-c dibuat kontras dengan wadah khusus
with q5:
    st.markdown(
        f'<div style="background-color:#0A192F; color:white; padding:10px; border-radius:5px; text-align:center;">'
        f'<p style="margin:0; font-size:12px;">Capaian c-to-c</p>'
        f'<h3 style="margin:0; color:#00CC96;">{capaian_ctc}%</h3>'
        f'</div>', 
        unsafe_allow_html=True
    )

# Box Simulasi Target Pertumbuhan (Warna latar belakang khusus)
st.markdown("<br>", unsafe_allow_html=True)
with st.container():
    st.markdown(
        '<div style="background-color:#1E293B; padding:5px; border-radius:10px;">'
        '<h4 style="color:#F8FAFC; margin-top:0; padding-left:10px;">Simulasi Pencapaian Target Pertumbuhan Ekonomi Tahun 2026</h4>'
        '</div>', 
        unsafe_allow_html=True
    )
    
    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        target_2026 = st.number_input("**Target Pertumbuhan Ekonomi (Persen):**", value=5.0, step=0.1)
        
        try:
            capaian_realitas = float(capaian_ctc) if capaian_ctc != "-" else 0.0
        except ValueError:
            capaian_realitas = 0.0
            
        # Logika bar status capaian ke kanan
        status_track = "On Track / Realistis untuk Dicapai" if capaian_realitas >= target_2026 else "Memerlukan Dukungan Percepatan / Upaya Ekstra"
        st.write(f"**Status Capaian:** {status_track}")
        
        # Hindari pembagian dengan nol
        pembagi = max(target_2026, 0.1)
        st.progress(min(max(float(capaian_realitas / pembagi), 0.0), 1.0))
        
    with col_sim2:
        # Interpretasi rumus dinamis kuartal selanjutnya
        sisa_target = max((target_2026 * 4 - capaian_realitas) / 3, 0.0)
        st.write(f"**Interpretasi Singkat:** Untuk mencapai target pertumbuhan sebesar {target_2026}%, laju pertumbuhan rata-rata pada Triwulan selanjutnya minimal harus didorong sebesar {sisa_target:.2f}%.")

# 2. Struktur Ekonomi Daerah (Area Chart)
st.markdown("#### Struktur Ekonomi Daerah")
buat_area_struktur(df_struktur_aktif)

# 3. Indikator Ekonomi dan Sosial Lainnya
st.markdown("#### Indikator Ekonomi dan Sosial Lainnya")

col_ek1, col_ek2, col_ek3, col_ek4, col_ek5 = st.columns(5)
with col_ek1:
    st.metric(label="PDRB Perkapita (Juta Rp)", value=df_active_dict.get('pdrb_perkapita', '-'))
with col_ek2:
    st.metric(label="Tingkat Inflasi Tahunan (Persen)", value=df_active_dict.get('inflasi', '-'))
with col_ek3:
    with st.container():
        st.markdown("**Nilai Investasi:**")
        st.write(f"• PMA (Juta USD): {df_active_dict.get('pma', '-')}")
        st.write(f"• PMDN (Miliar Rp): {df_active_dict.get('pmdn', '-')}")
with col_ek4:
    st.metric(label="Komoditas Ekspor Terbesar", value=df_active_dict.get('ekspor_top3', '-'))
with col_ek5:
    st.metric(label="Tenaga Kerja Terbesar", value=df_active_dict.get('naker_top', '-'))

# 4 Kotak indikator sosial
col_sos1, col_sos2, col_sos3, col_sos4 = st.columns(4)
with col_sos1:
    st.metric(label="Indeks Pembangunan Manusia - IPM", value=df_active_dict.get('ipm', '-'))
with col_sos2:
    st.metric(label="Tingkat Kemiskinan (%)", value=df_active_dict.get('kemiskinan', '-'))
with col_sos3:
    st.metric(label="Tingkat Pengangguran Terbuka (TPT) (%)", value=df_active_dict.get('tpt', '-'))
with col_sos4:
    st.metric(label="Rasio Gini", value=df_active_dict.get('gini', '-'))

st.markdown("---")

# ==========================================
# URUTAN 3: ANALISIS SEKTOR UNGGULAN DAERAH
# ==========================================
st.header(f"ANALISIS SEKTOR UNGGULAN DAERAH {provinsi_terpilih.upper()}")
buat_scatter_sektoral(df_sektoral_aktif, "Overlay")
buat_scatter_sektoral(df_sektoral_aktif, "Shift Share")
buat_scatter_sektoral(df_sektoral_aktif, "Tipologi Klassen")

st.markdown("---")

# ==========================================
# URUTAN 4: INTERPRETASI DAN REKOMENDASI
# ==========================================
st.header("INTERPRETASI DAN REKOMENDASI")

st.markdown("### Interpretasi Sisi Ekonomi")
st.info(df_active_dict.get("interpretasi_ekonomi_riil", "-"))

st.markdown("### Rekomendasi Sisi Ekonomi")
st.success(df_active_dict.get("rekomendasi_ekonomi_riil", "-"))
