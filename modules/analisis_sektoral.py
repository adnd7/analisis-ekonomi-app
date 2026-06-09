# modules/analisis_sektoral.py

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

# Palet warna institusional institusional seragam untuk 17 Lapangan Usaha (Case-Insensitive)
WARNA_SEKTOR_GLOBAL = {
    "pertanian": "#22C55E", "pertambangan": "#D97706", "industri": "#6B21A8",
    "pengadaan listrik": "#EA580C", "pengadaan air": "#1E3A1E", "konstruksi": "#8B5CF6",
    "perdagangan": "#1D4ED8", "transportasi": "#FBBF24", "akmamin": "#F472B6",
    "informasi dan komunikasi": "#3B82F6", "jasa keuangan": "#EC4899", "real estat": "#6B7280",
    "jasa perusahaan": "#9CA3AF", "adm. pemerintahan": "#DC2626", "jasa pendidikan": "#0D9488",
    "jasa kesehatan": "#78350F", "jasa lainnya": "#D97706"
}

def get_warna_sektor_map(df_column):
    """Fungsi helper untuk mencocokkan kolom sektor dengan palet warna tanpa sensitif huruf kapital"""
    return {sektor: WARNA_SEKTOR_GLOBAL.get(sektor.lower(), "#6B7280") for sektor in df_column.unique()}

def buat_bar_chart_makro(df_aktif, tipe_chart):
    """
    URUTAN 1: Visualisasi Bar Chart Horizontal Kondisi Makro 38 Provinsi.
    """
    if df_aktif.empty:
        st.warning("Data makro untuk grafik batang kosong.")
        return

    if tipe_chart == "Pertumbuhan Ekonomi":
        df_sorted = df_aktif.sort_values(by="lpe_ctc", ascending=True)
        fig = px.bar(df_sorted, x="lpe_ctc", y="provinsi", orientation='h',
                     labels={"lpe_ctc": "LPE c-to-c (%)", "provinsi": "Provinsi"},
                     color="lpe_ctc", color_continuous_scale="Viridis")
    else:
        df_sorted = df_aktif.sort_values(by="kontribusi", ascending=True)
        fig = px.bar(df_sorted, x="kontribusi", y="provinsi", orientation='h',
                     labels={"kontribusi": "Kontribusi PDRB (%)", "provinsi": "Provinsi"},
                     color="kontribusi", color_continuous_scale="Cividis")
        
    fig.update_layout(height=600, margin={"r":10,"t":10,"l":10,"b":10})
    st.plotly_chart(fig, use_container_width=True)

def buat_peta_klasifikasi(df_aktif):
    """
    URUTAN 1: Visualisasi Peta Choropleth 38 Provinsi dengan Skema Warna KEMD resmi.
    """
    if df_aktif.empty:
        st.warning("Data kosong, peta tidak dapat dimuat.")
        return
        
    try:
        with open("data/indonesia_provinces.geojson", "r") as f:
            geojson_indonesia = json.load(f)
            
        fig = px.choropleth_mapbox(
            df_aktif,
            geojson=geojson_indonesia,
            locations="provinsi",               
            featureidkey="properties.PROVINSI",  
            color="klasifikasi",                 
            color_discrete_map={                
                "Daerah Maju dan Cepat Tumbuh": "#0D415C",  
                "Daerah Berkembang Cepat": "#13BA8E",      
                "Daerah Maju tapi Tertekan": "#A7E048",    
                "Daerah Relatif Tertinggal": "#D9DADB"     
            },
            mapbox_style="carto-positron",
            center={"lat": -2.5, "lon": 118.0}, 
            zoom=3.5,
            opacity=0.8,
            labels={"klasifikasi": "Status Klasifikasi"}
        )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.info(f"🗺️ *[Gagal memuat batas spasial GeoJSON. Pastikan file data/indonesia_provinces.geojson tersedia. Error: {e}]*")

def buat_line_growth(df_aktif, provinsi):
    """
    URUTAN 2: Grafik Tren Pertumbuhan Ekonomi Wilayah Tren Tahunan.
    """
    # Membaca file mentah untuk mengambil tren historis tahun-tahun sebelumnya
    try:
        df_raw = pd.read_csv("data/data_ekonomi.csv")
        df_prov = df_raw[df_raw['provinsi'].str.strip() == provinsi].sort_values(by="tahun")
        
        if df_prov.empty:
            st.warning(f"Data tren historis untuk {provinsi} tidak ditemukan.")
            return
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_prov['tahun'], y=df_prov['lpe_ctc'], name=f"{provinsi} (c-to-c)", mode='lines+markers', line=dict(width=3, color='#1D4ED8')))
        fig.add_trace(go.Scatter(x=df_prov['tahun'], y=df_prov['inflasi'], name='Inflasi Wilayah', mode='lines+markers', line=dict(dash='dash', color='#DC2626')))
        
        fig.update_layout(xaxis=dict(dtick=1, type='category'), xaxis_title="Tahun", yaxis_title="Persentase (%)",
                          margin={"r":10,"t":30,"l":10,"b":10}, legend_orientation="h")
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.error("Gagal memuat tren pertumbuhan makro historis.")

def buat_area_struktur(df_aktif):
    """
    URUTAN 2: Grafik Struktur Ekonomi 17 Lapangan Usaha (Kunci Perbaikan: Huruf Kecil Kolom).
    """
    if not df_aktif.empty:
        # KUNCI PERBAIKAN: Gunakan kolom 'tahun', 'kontribusi_sektor', 'sektor' sesuai CSV asli Anda
        df_display = df_aktif.sort_values(by="tahun")
        warna_map = get_warna_sektor_map(df_display['sektor'])
        
        fig = px.area(
            df_display,
            x="tahun",
            y="kontribusi_sektor",
            color="sektor",
            line_group="sektor",
            color_discrete_map=warna_map,
            labels={"tahun": "Tahun Analisis", "kontribusi_sektor": "Kontribusi Sektor PDRB (%)"}
        )
        fig.update_layout(
            showlegend=True,    
            xaxis=dict(dtick=1, type='category'), 
            margin={"r": 10, "t": 10, "l": 10, "b": 10}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 *[Grafik Tren Area Struktur Ekonomi belum dapat dimuat karena data kosong]*")

def buat_scatter_sektoral(df_aktif, jenis_analisis):
    """
    URUTAN 3: Scatter Plot Sektoral RIIL menggunakan Input Data dari CSV Aktif.
    """
    if df_aktif.empty:
        st.info(f"🎯 *[Grafik Scatter Plot {jenis_analisis} akan muncul otomatis setelah data sektoral provinsi termuat]*")
        return

    # 1. Penentuan Sumbu & Threshold Dinamis Berdasarkan Spesifikasi CSV Anda
    if jenis_analisis == "Overlay":
        judul_full = 'Scatter Plot "Overlay (MRP - LQ) 2025"'
        help_teks = "Metode Overlay merupakan teknik yang menggabungkan hasil analisis Location Quotient (LQ) dan Model Rasio Pertumbuhan (MRP) untuk mengidentifikasi sektor yang memiliki keunggulan sekaligus pertumbuhan yang kuat. Dengan mengombinasikan kedua pendekatan tersebut, metode ini menghasilkan penentuan sektor prioritas yang lebih robust dibandingkan penggunaan satu metode secara terpisah."
        kriteria_teks = (
            "- **Kriteria I (Rasio Pertumbuhan > 1 dan LQ > 1):** Sektor Unggulan dan Dominan $\\rightarrow$ sektor dengan pertumbuhan tinggi dan kontribusi besar yang menjadi motor utama perekonomian daerah.\n"
            "- **Kriteria II (Rasio Pertumbuhan > 1 dan LQ < 1):** Sektor Berkembang $\\rightarrow$ sektor dengan pertumbuhan tinggi namun kontribusinya masih kecil, sehingga berpotensi menjadi sumber pertumbuhan baru.\n"
            "- **Kriteria III (Rasio Pertumbuhan < 1 dan LQ > 1):** Sektor Potensial $\\rightarrow$ sektor dengan kontribusi besar tetapi pertumbuhannya mulai melambat, sehingga perlu dijaga keberlanjutannya.\n"
            "- **Kriteria IV (Rasio Pertumbuhan < 1 dan LQ < 1):** Sektor Tertinggal $\\rightarrow$ sektor dengan pertumbuhan dan kontribusi yang rendah, sehingga belum memiliki peran signifikan dalam perekonomian."
        )
        col_x, col_y = "lq_2025", "rps_2025"
        garis_x, garis_y = 1.0, 1.0  # Threshold LQ=1, RPs=1
        labels_x, labels_y = "Komponen Kontribusi (Location Quotient)", "Komponen Pertumbuhan (Rasio Pertumbuhan)"

    elif jenis_analisis == "Shift Share":
        judul_full = 'Scatter Plot "Shift Share 2015/2025"'
        help_teks = "Metode Shift Share digunakan untuk menguraikan pertumbuhan suatu sektor ke dalam komponen pengaruh pertumbuhan nasional, struktur ekonomi, dan daya saing daerah. Melalui metode ini, dapat diketahui apakah kinerja suatu sektor didorong oleh dinamika nasional atau oleh keunggulan kompetitif yang dimiliki daerah."
        kriteria_teks = (
            "- **Kriteria I (RS + IM +):** Sektor Tumbuh Pesat $\\rightarrow$ sektor yang memiliki daya saing tinggi di tingkat lokal dan didukung oleh tren pertumbuhan nasional.\n"
            "- **Kriteria II (RS + IM -):** Sektor Berpotensi $\\rightarrow$ sektor yang kuat secara lokal meskipun secara nasional cenderung melambat, sehingga berpotensi menjadi keunggulan spesifik daerah.\n"
            "- **Kriteria III (RS - IM +):** Sektor Berkembang $\\rightarrow$ sektor yang tumbuh secara nasional namun belum diikuti oleh daya saing daerah, sehingga memerlukan penguatan kapasitas lokal.\n"
            "- **Kriteria IV (RS - IM -):** Sektor Tertinggal $\\rightarrow$ sektor dengan daya saing dan pertumbuhan yang rendah baik di tingkat lokal maupun nasional."
        )
        col_x, col_y = "im_2025", "rs_2025"
        garis_x, garis_y = 0.0, 0.0  # Threshold Net Gain Shift Share
        labels_x, labels_y = "Komponen Daya Saing (Regional Share)", "Komponen Struktur Nasional (Industrial Mix)"

    else:  # Tipologi Klassen
        judul_full = 'Scatter Plot "Tipologi Klassen Rata-Rata 2022-2025"'
        help_teks = "Tipologi Klassen merupakan metode klasifikasi sektor berdasarkan tingkat pertumbuhan dan kontribusinya terhadap perekonomian daerah. Hasil analisisnya memberikan gambaran yang jelas mengenai posisi relatif setiap sektor, mulai dari sektor unggulan hingga sektor yang masih tertinggal, sehingga mendukung perumusan arah pembangunan ekonomi daerah."
        kriteria_teks = (
            "- **Kriteria I (Pertumbuhan > Nasional dan Kontribusi > Nasional):** Sektor Andalan $\\rightarrow$ sektor dengan pertumbuhan dan kontribusi tinggi yang menjadi prioritas utama pembangunan ekonomi.\n"
            "- **Kriteria II (Pertumbuhan > Nasional dan Kontribusi < Nasional):** Sektor Berkembang $\\rightarrow$ sektor dengan pertumbuhan tinggi namun kontribusi masih kecil, sehingga berpotensi menjadi andalan baru.\n"
            "- **Kriteria III (Pertumbuhan < Nasional dan Kontribusi > Nasional):** Sektor Potensial $\\rightarrow$ sektor dengan kontribusi besar tetapi pertumbuhan melambat, sehingga perlu dijaga agar tidak menurun.\n"
            "- **Kriteria IV (Pertumbuhan < Nasional dan Kontribusi < Nasional):** Sektor Tertinggal $\\rightarrow$ sektor dengan pertumbuhan dan kontribusi rendah yang memerlukan perhatian dan intervensi khusus."
        )
        col_x, col_y = "kontribusi_2025", "pertumbuhan_2025"
        # Threshold rata-rata makro nasional sebagai acuan kebijakan
        garis_x, garis_y = 5.6, 5.1  
        labels_x, labels_y = "Rata-Rata Kontribusi Sektor terhadap PDRB (%)", "Rata-Rata Pertumbuhan Sektor (%)"

    # 2. Layout Render Tiga Dimensi Sektoral
    st.markdown(f"##### {judul_full}", help=help_teks)
    col_grafik, col_narasi = st.columns([2, 1])
    
    with col_grafik:
        warna_map = get_warna_sektor_map(df_aktif['sektor'])
        
        # Gambar grafik scatter plot interaktif berbasis data riil CSV Anda
        fig = px.scatter(
            df_aktif, 
            x=col_x, 
            y=col_y, 
            text="sektor",        
            color="sektor",       
            labels={col_x: labels_x, col_y: labels_y},
            color_discrete_map=warna_map  
        )
        
        # Pasang Garis Threshold Kuadran Analisis
        fig.add_hline(y=garis_y, line_dash="dash", line_color="#475569", line_width=1.5)
        fig.add_vline(x=garis_x, line_dash="dash", line_color="#475569", line_width=1.5)
        
        fig.update_traces(textposition='top center', marker=dict(size=14))
        fig.update_layout(
            showlegend=False,          
            margin={"r": 20, "t": 30, "l": 20, "b": 20}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with col_narasi:
        st.markdown("**Deskripsi Pembagian Kuadran Sektor:**")
        st.markdown(kriteria_teks)
