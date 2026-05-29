# modules/simulasi.py

def hitung_target_triwulan(target_fy, q1_act):
    # Rumus Run-rate sisa pemenuhan target tahunan penuh (Full Year)
    # Target_FY = (Q1_Aktual + Q2 + Q3 + Q4) / 4
    total_bobot_sisa = (target_fy * 4) - q1_act
    sisa_per_q = round(total_bobot_sisa / 3, 2)
    
    # Menentukan status tingkat kerawanan deviasi pencapaian target target kerja pemerintah
    if sisa_per_q > (q1_act + 2.5):
        status = "AKSELERASI TINGGI / SANGAT BERAT"
        alert_type = "error"
    elif sisa_per_q > (q1_act + 0.5):
        status = "PERLU INTERVENSI / UPAYA EKSTRA"
        alert_type = "warning"
    else:
        status = "KONDISI NORMAL / REALISTIS"
        alert_type = "success"
        
    return sisa_per_q, status, alert_type