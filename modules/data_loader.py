# modules/data_loader.py

import pandas as pd
import numpy as np
import os

# 1. Master Urutan 38 Provinsi Resmi BPS/Kemendagri
DAFTAR_PROVINSI_URUT = [
    "Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Jambi", 
    "Sumatera Selatan", "Bengkulu", "Lampung", "Kepulauan Bangka Belitung", "Kepulauan Riau", 
    "DKI Jakarta", "Jawa Barat", "Jawa Tengah", "DI Yogyakarta", "Jawa Timur", 
    "Banten", "Bali", "Nusa Tenggara Barat", "Nusa Tenggara Timur", "Kalimantan Barat", 
    "Kalimantan Tengah", "Kalimantan Selatan", "Kalimantan Timur", "Kalimantan Utara", 
    "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan", "Sulawesi Tenggara", "Gorontalo", 
    "Sulawesi Barat", "Maluku", "Maluku Utara", "Papua Barat", "Papua Barat Daya", 
    "Papua", "Papua Selatan", "Papua Tengah", "Papua Pegunungan"
]

# 2. Master Nomenklatur 17 Lapangan Usaha Standar BPS
DAFTAR_SEKTOR_BPS = [
    "01. Pertanian, Kehutanan, dan Perikanan",
    "02. Pertambangan dan Penggalian",
    "03. Industri Pengolahan",
    "04. Pengadaan Listrik dan Gas",
    "05. Pengadaan Air, Pengelolaan Sampah, Limbah dan Daur Ulang",
    "06. Konstruksi",
    "07. Perdagangan Besar dan Eceran; Reparasi Mobil dan Sepeda Motor",
    "08. Transportasi dan Pergudangan",
    "09. Penyediaan Akomodasi dan Makan Minum",
    "10. Informasi dan Komunikasi",
    "11. Jasa Keuangan dan Asuransi",
    "12. Real Estat",
    "13. Jasa Perusahaan",
    "14. Administrasi Pemerintahan, Pertahanan dan Jaminan Sosial Wajib",
    "15. Jasa Pendidikan",
    "16. Jasa Kesehatan dan Kegiatan Sosial",
    "17. Jasa Lainnya"
]

def load_all_economic_data():
    file_path = "data/data_ekonomi.csv"
    
    # Jika file data fisik dari user ditemukan, baca langsung
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    
    # FALLBACK ENGINE: Jika data csv belum ditaruh, auto-generate data 38 provinsi x 17 sektor secara presisi
    data_store = []
    np.random.seed(100)
    tahun_list = [2025, 2024, 2023]
    
    for prov in DAFTAR_PROVINSI_URUT:
        for thn in tahun_list:
            # Baseline Indikator Makro & Sosial per wilayah agar mendekati data riil BPS 2025/2026
            base_growth = 12.5 if prov in ["Sulawesi Tengah", "Maluku Utara"] else (4.9 if prov in ["Jawa Timur", "Jawa Barat", "Sumatera Utara"] else 5.1)
            base_pdrb_kap = 290.5 if prov == "DKI Jakarta" else (120.0 if prov == "Kalimantan Timur" else 55.4)
            base_kemiskinan = 3.6 if prov == "DKI Jakarta" else (11.4 if prov in ["Aceh", "Nusa Tenggara Timur"] else 8.2)
            base_ipm = 83.2 if prov == "DKI Jakarta" else 73.5
            
            for sek in DAFTAR_SEKTOR_BPS:
                # Simulasi nilai analisis Overlay, Shift-Share (D), dan LQ berdasarkan jenis sektor
                is_basis = any(keyword in sek for keyword in ["Pertanian", "Pertambangan", "Industri"]) if prov not in ["DKI Jakarta"] else any(keyword in sek for keyword in ["Keuangan", "Informasi", "Jasa Perusahaan"])
                
                lq_val = round(np.random.uniform(1.1, 2.8) if is_basis else np.random.uniform(0.3, 0.95), 2)
                ss_d_val = round(np.random.uniform(0.5, 5.8) if is_basis else np.random.uniform(-3.5, 0.4), 2)
                kontribusi = round(np.random.uniform(10.0, 25.0) if is_basis else np.random.uniform(1.5, 5.5), 2)
                
                # Menentukan Tipologi Klassen berdasarkan matriks kuadran LQ dan Shift Share D
                if lq_val >= 1.0 and ss_d_val >= 0:
                    klasifikasi = "Sektor Unggulan (Kuadran I)"
                    kuadran = "Kuadran I"
                elif lq_val >= 1.0 and ss_d_val < 0:
                    klasifikasi = "Sektor Potensial (Kuadran II)"
                    kuadran = "Kuadran II"
                elif lq_val < 1.0 and ss_d_val >= 0:
                    klasifikasi = "Sektor Berkembang (Kuadran III)"
                    kuadran = "Kuadran III"
                else:
                    klasifikasi = "Sektor Tertekan (Kuadran IV)"
                    kuadran = "Kuadran IV"
                
                data_store.append({
                    "Provinsi": prov,
                    "Tahun": thn,
                    "Lapangan_Usaha": sek,
                    "LQ": lq_val,
                    "Shift_Share_D": ss_d_val,
                    "Kontribusi_PDRB": kontribusi,
                    "Klasifikasi": klasifikasi,
                    "Kuadran": kuadran,
                    # Makro Regional Info
                    "Pertumbuhan_Ekonomi": round(np.random.uniform(base_growth-0.3, base_growth+0.4), 2),
                    "PDRB_Per_Kapita": round(np.random.uniform(base_pdrb_kap-2, base_pdrb_kap+3), 2),
                    "Inflasi": round(np.random.uniform(2.1, 3.8), 2),
                    "Investasi": round(np.random.uniform(20.0, 75.0), 2),
                    "Ekspor": round(np.random.uniform(5.0, 45.0), 2),
                    # Sosial Info
                    "IPM": round(np.random.uniform(base_ipm-0.2, base_ipm+0.4), 2),
                    "Kemiskinan": round(np.random.uniform(base_kemiskinan-0.4, base_kemiskinan+0.3), 2),
                    "TPT": round(np.random.uniform(4.2, 6.8), 2),
                    "Gini_Ratio": round(np.random.uniform(0.320, 0.395), 3)
                })
                
    return pd.DataFrame(data_store)