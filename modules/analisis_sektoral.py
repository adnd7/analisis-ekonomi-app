# modules/analisis_sektoral.py

import plotly.express as px

def generate_klassen_chart(df_sektoral, nama_provinsi):
    fig = px.scatter(
        df_sektoral, 
        x="Shift_Share_D", 
        y="LQ",
        text="Lapangan_Usaha",
        size="Kontribusi_PDRB",
        color="Klasifikasi",
        color_discrete_map={
            "Sektor Unggulan (Kuadran I)": "#0F5132",    # Hijau Eksekutif
            "Sektor Potensial (Kuadran II)": "#FFC107",   # Amber / Kuning Emas
            "Sektor Berkembang (Kuadran III)": "#0D6EFD", # Biru Muda Pro
            "Sektor Tertekan (Kuadran IV)": "#DC3545"      # Merah Peringatan
        },
        hover_name="Lapangan_Usaha",
        hover_data={"LQ": True, "Shift_Share_D": True, "Kontribusi_PDRB": ":.2f%"},
        labels={"Shift_Share_D": "Dampak Net Shift (Komponen Keunggulan Kompetitif)", "LQ": "Nilai Indeks Location Quotient (LQ)"},
        title=f"Matriks Tipologi Klassen Lapangan Usaha BPS Provinsi {nama_provinsi}"
    )
    
    # Membuat garis potong kuadran nasional standar (LQ = 1.0 dan Net Shift = 0.0)
    fig.add_hline(y=1.0, line_dash="dash", line_color="#6C757D", annotation_text="Batas Basis (LQ=1)")
    fig.add_vline(x=0.0, line_dash="dash", line_color="#6C757D", annotation_text="Batas Tren Nasional")
    
    fig.update_traces(textposition='top center', marker=dict(opacity=0.85, line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(
        plot_bgcolor="#FFFFFF",
        hovermode="closest",
        legend_orientation="h",
        legend_y=-0.25,
        margin=dict(l=30, r=30, t=50, b=30)
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E2E8F0")
    fig.update_yaxes(showgrid=True, gridcolor="#E2E8F0")
    
    return fig