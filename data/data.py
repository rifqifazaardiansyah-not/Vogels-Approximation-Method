# ==========================================
# 1. DEFINISI DATA SESUAI STUDI KASUS JURNAL
# ==========================================
origin = ['CGK', 'UPG']
destination = ['BPN', 'SUB', 'KNO', 'UPG', 'DJJ']

M = 999999999

# Matriks Biaya Pengiriman (Rp/kg)
matrix = [
    [24000, 22500, 30000, 28000, 45000],  # CGK
    [M, M, M, M, 18000]                   # UPG
]

# Kebutuhan Vaksin (Demand) tiap kota tujuan
need = [2000, 3000, 2000, 2500, 2500]      # Total = 12,000 kg

# Kapasitas Gudang (Supply) real berdasarkan alokasi imbang jurnal
availability = [11000, 1000]               # Total = 12,000 kg