# modules/ai_engine.py

def generate_executive_narrative(macro_row, df_sektoral):
    # Ambil daftar nama sektor unggulan dari data terfilter
    sektor_unggulan = df_sektoral[df_sektoral['Kuadran'] == "Kuadran I"]['Lapangan_Usaha'].tolist()
    sektor_tertekan = df_sektoral[df_sektoral['Kuadran'] == "Kuadran IV"]['Lapangan_Usaha'].tolist()
    
    top_3_unggulan = [s.split(". ")[1] for s in sektor_unggulan[:3]] if sektor_unggulan else ["Industri Pengolahan"]
    top_3_tertekan = [s.split(". ")[1] for s in sektor_tertekan[:3]] if sektor_tertekan else ["Jasa Lainnya"]

    narasi = f"""
    ### 🏛️ LAPORAN NOTA DINAS ANALISIS MAKRO SEKTORAL WILAYAH
    **Dokumen Telaah Perencanaan Pembangunan Makro Regional**
    
    **1. Evaluasi Capaian Indikator Makroekonomi**
    Pada periode analisis Tahun {macro_row['Tahun']}, perekonomian Provinsi {macro_row['Provinsi']} mencatatkan laju pertumbuhan sebesar **{macro_row['Pertumbuhan_Ekonomi']}%**. Kapasitas output riil masyarakat yang direpresentasikan melalui nilai PDRB Per Kapita menyentuh angka **Rp {macro_row['PDRB_Per_Kapita']} Juta/Tahun**. Kinerja makro ini bergerak di tengah volatilitas tingkat inflasi daerah yang terkendali pada level **{macro_row['Inflasi']}%**, didukung realisasi investasi (PMA/PMDN) sebesar **Rp {macro_row['Investasi']} Triliun**.
    
    **2. Telaah Kondisi Kesejahteraan Sosial dan Inklusivitas**
    Pencapaian Indeks Pembangunan Manusia (IPM) tercatat pada skor **{macro_row['IPM']}**, yang mengindikasikan kualitas modal manusia berada pada koridor memadai. Kendati demikian, tantangan struktural daerah masih tertuju pada penyelesaian tingkat kemiskinan yang berada di angka **{macro_row['Kemiskinan']}%**, beriringan dengan Tingkat Pengangguran Terbuka (TPT) sebesar **{macro_row['TPT']}%**. Kesenjangan distribusi pendapatan atau Gini Ratio berada pada koefisien **{macro_row['Gini_Ratio']}**, membutuhkan pendekatan pembangunan yang mengedepankan aspek keadilan spasial.
    
    **3. Konfigurasi Sektor Penggerak Ekonomi Daerah (Klassen Typology)**
    Berdasarkan integrasi matriks nilai Location Quotient (LQ) dan analisis komponen deviasi Shift-Share, klusterisasi sektor di Provinsi {macro_row['Provinsi']} menghasilkan rumusan berikut:
    * **Sektor Unggulan Utama (Maju & Tumbuh Cepat):** Sektor {', '.join(top_3_unggulan)}. Sektor-sektor ini bertindak sebagai lokomotif utama pertumbuhan.
    * **Sektor Tertekan (Relatif Tertinggal):** Sektor {', '.join(top_3_tertekan)}. Sektor ini membutuhkan perhatian khusus berupa restrukturisasi atau insentif fiskal daerah guna mencegah pemburukan kontribusi PDRB.
    """
    return narasi

def generate_ai_policy_matrix(macro_row):
    matrix = {}
    
    # Rumusan Rekomendasi Fiskal
    if macro_row['Pertumbuhan_Ekonomi'] < 5.0:
        matrix['fiskal'] = "Menginisiasi skema relaksasi pajak daerah (*tax holiday* lokal) untuk kluster UMKM sektor hilir, serta mendorong percepatan penyerapan anggaran belanja modal APBD untuk stimulus daya beli."
    else:
        matrix['fiskal'] = "Meningkatkan alokasi Belanja Tidak Terduga (BTT) untuk ketahanan pangan, serta mengoptimalkan ruang fiskal daerah melalui penguatan Dana Alokasi Khusus (DAK) fisik infrastruktur."
        
    # Rumusan Sektoral & Investasi
    matrix['sektoral'] = "Mendorong hilirisasi komoditas basis lokal guna meningkatkan nilai tambah (*value added*) domestik, sekaligus melakukan deregulasi perizinan usaha di kawasan industri prioritas daerah melalui integrasi KEK."
    
    # Rumusan Kebijakan Sosial & Kemiskinan
    if macro_row['Kemiskinan'] > 9.5:
        matrix['sosial'] = "Melakukan integrasi program bansos daerah berbasis intervensi Satu Data Regsosek, serta memperbanyak alokasi program Padat Karya Tunai Daerah (PKTD) pada infrastruktur tersier pedesaan."
    else:
        matrix['sosial'] = "Mengembangkan program sertifikasi keahlian khusus melalui Balai Latihan Kerja (BLK) untuk menjembatani suplai tenaga kerja lokal dengan permintaan sektor industri pengolahan."
        
    # Rumusan Pengendalian Inflasi
    if macro_row['Inflasi'] > 3.2:
        matrix['inflasi'] = "Mengintensifkan operasi pasar murah melalui BUMD pangan, memperluas cakupan Kerjasama Antar Daerah (KAD) pasokan logistik, serta memberikan subsidi ongkos angkut komoditas bahan pokok penting."
    else:
        matrix['inflasi'] = "Melakukan pemantauan berkala pada rantai distribusi energi dan pangan pokok di tingkat distributor utama guna memitigasi spekulasi harga menjelang HBKN."
        
    return matrix