# ==========================================
# 1. DEFINISI DATA SESUAI STUDI KASUS
# ==========================================

origin = [
    'Vendor 1',
    'Vendor 2',
    'Vendor 3',
    'Vendor 4',
    'Vendor 5'
]

destination = [
    'Pekanbaru',
    'Jambi',
    'Padang',
    'Palembang'
]

M = 999999999

# Matriks Biaya Pengiriman
matrix = [
    [1000, 1600, 1200, 2200],  # Vendor 1
    [800, 1300, 1000, 1800],   # Vendor 2
    [700, 1200, 900, 2000],    # Vendor 3
    [1200, 1500, 1300, 2100],  # Vendor 4
    [1300, 1400, 1100, 1900]   # Vendor 5
]

# Permintaan tiap kota tujuan
need = [17000, 12000, 10000, 10000]  # Total = 49,000

# Kapasitas tiap vendor
availability = [8000, 15000, 12000, 8000, 8000]  # Total = 51,000