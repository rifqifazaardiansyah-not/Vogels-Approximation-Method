"""
CONTOH PENGGUNAAN STEPPING STONE UNTUK BERBAGAI KASUS
======================================================

File ini menunjukkan bagaimana menggunakan fungsi stepping_stone() yang
sudah refactored untuk menangani berbagai kasus transportasi berbeda.

Setiap contoh dapat dijalankan secara independen.
"""

from steppingstone import stepping_stone
import time

# ==============================================================
# KASUS 1: KASUS ORIGINAL (SUDAH ADA)
# ==============================================================

def kasus_original():
    """Kasus original dengan 5 vendor dan 5 destinasi"""
    
    print("\n" + "="*70)
    print("  KASUS 1: ORIGINAL (5 Vendor × 5 Destinasi)")
    print("="*70)
    
    origin      = ['Vendor 1', 'Vendor 2', 'Vendor 3', 'Vendor 4', 'Vendor 5']
    destination = ['Pekanbaru', 'Jambi', 'Padang', 'Palembang', 'Dummy']
    
    cost_table = [
        [1000, 1600, 1200, 2200, 0],
        [800,  1300, 1000, 1800, 0],
        [700,  1200,  900, 2000, 0],
        [1200, 1500, 1300, 2100, 0],
        [1300, 1400, 1100, 1900, 0],
    ]
    
    need_orig         = [17000, 12000, 10000, 10000, 2000]
    availability_orig = [8000, 15000, 12000, 8000, 8000]
    
    alloc_vam = [
        [0,     0,     8000, 0,    0   ],
        [15000, 0,     0,    0,    0   ],
        [2000,  8000,  2000, 0,    0   ],
        [0,     4000,  0,    4000, 0   ],
        [0,     0,     0,    6000, 2000],
    ]
    
    start_time = time.time()
    alloc, cost, iterations = stepping_stone(
        origin, destination, cost_table, need_orig, availability_orig,
        alloc_vam, show_details=True
    )
    elapsed = time.time() - start_time
    
    print(f"\n✓ Waktu eksekusi: {elapsed:.4f} detik, Iterasi: {iterations}")
    return alloc, cost


# ==============================================================
# KASUS 2: KASUS SEDERHANA (3×3)
# ==============================================================

def kasus_sederhana():
    """Kasus transportasi sederhana dengan 3 pabrik dan 3 gudang"""
    
    print("\n" + "="*70)
    print("  KASUS 2: SEDERHANA (3 Pabrik × 3 Gudang)")
    print("="*70)
    
    origin      = ['Pabrik A', 'Pabrik B', 'Pabrik C']
    destination = ['Gudang X', 'Gudang Y', 'Gudang Z']
    
    cost_table = [
        [2, 3, 4],
        [1, 4, 2],
        [3, 1, 5],
    ]
    
    need_orig         = [100, 150, 100]
    availability_orig = [80, 120, 150]
    
    # Alokasi awal menggunakan VAM (contoh)
    alloc_vam = [
        [80, 0,  0],
        [0,  120, 0],
        [20, 30, 100],
    ]
    
    start_time = time.time()
    alloc, cost, iterations = stepping_stone(
        origin, destination, cost_table, need_orig, availability_orig,
        alloc_vam, show_details=True
    )
    elapsed = time.time() - start_time
    
    print(f"\n✓ Waktu eksekusi: {elapsed:.4f} detik, Iterasi: {iterations}")
    return alloc, cost


# ==============================================================
# KASUS 3: KASUS BESAR (4×5)
# ==============================================================

def kasus_besar():
    """Kasus transportasi dengan 4 sumber dan 5 tujuan"""
    
    print("\n" + "="*70)
    print("  KASUS 3: BESAR (4 Sumber × 5 Tujuan)")
    print("="*70)
    
    origin      = ['Depot 1', 'Depot 2', 'Depot 3', 'Depot 4']
    destination = ['Kota A', 'Kota B', 'Kota C', 'Kota D', 'Kota E']
    
    cost_table = [
        [10, 15, 20, 12, 18],
        [12, 18, 14, 16, 20],
        [15, 12, 16, 18, 14],
        [18, 16, 15, 14, 12],
    ]
    
    need_orig         = [50, 60, 40, 70, 50]
    availability_orig = [60, 80, 70, 60]
    
    # Alokasi awal VAM
    alloc_vam = [
        [0,  0,  0,  0,  60],
        [0,  0,  0,  80, 0],
        [0,  60, 10, 0,  0],
        [50, 0,  30, 0,  0],
    ]
    
    start_time = time.time()
    alloc, cost, iterations = stepping_stone(
        origin, destination, cost_table, need_orig, availability_orig,
        alloc_vam, show_details=True
    )
    elapsed = time.time() - start_time
    
    print(f"\n✓ Waktu eksekusi: {elapsed:.4f} detik, Iterasi: {iterations}")
    return alloc, cost


# ==============================================================
# KASUS 4: VERSI RINGKAS (Tanpa Detail Iterasi)
# ==============================================================

def kasus_ringkas():
    """Menjalankan kasus tanpa menampilkan detail iterasi"""
    
    print("\n" + "="*70)
    print("  KASUS 4: RINGKAS (Output Minimal)")
    print("="*70)
    
    origin      = ['A', 'B', 'C']
    destination = ['X', 'Y', 'Z', 'W']
    
    cost_table = [
        [5, 6, 7, 8],
        [4, 5, 6, 7],
        [6, 7, 8, 9],
    ]
    
    need_orig         = [30, 40, 25, 35]
    availability_orig = [50, 50, 30]
    
    alloc_vam = [
        [0,  40, 10, 0],
        [0,  0,  15, 35],
        [30, 0,  0,  0],
    ]
    
    start_time = time.time()
    alloc, cost, iterations = stepping_stone(
        origin, destination, cost_table, need_orig, availability_orig,
        alloc_vam, show_details=False  # <-- Tidak menampilkan detail
    )
    elapsed = time.time() - start_time
    
    print(f"\n  Hasil Optimal:")
    print(f"  - Total Cost    : {cost:,}")
    print(f"  - Jumlah Iterasi: {iterations}")
    print(f"  - Waktu         : {elapsed:.4f} detik")
    
    return alloc, cost


# ==============================================================
# MAIN - JALANKAN SEMUA KASUS
# ==============================================================

if __name__ == "__main__":
    print("\n\n")
    print("="*70)
    print("DEMONSTRASI STEPPING STONE METHOD - BERBAGAI KASUS")
    print("="*70)
    
    # Jalankan semua kasus
    results = {}
    
    try:
        print("\n[1/4] Menjalankan kasus original...")
        results['Original'] = kasus_original()
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # try:
    #     print("\n[2/4] Menjalankan kasus sederhana...")
    #     results['Sederhana'] = kasus_sederhana()
    # except Exception as e:
    #     print(f"✗ Error: {e}")
    
    # try:
    #     print("\n[3/4] Menjalankan kasus besar...")
    #     results['Besar'] = kasus_besar()
    # except Exception as e:
    #     print(f"✗ Error: {e}")
    
    # try:
    #     print("\n[4/4] Menjalankan kasus ringkas...")
    #     results['Ringkas'] = kasus_ringkas()
    # except Exception as e:
    #     print(f"✗ Error: {e}")
    
    # Ringkasan hasil
    print("\n\n" + "="*70)
    print("RINGKASAN HASIL SEMUA KASUS")
    print("="*70)
    print(f"\n{'Kasus':<15} {'Total Cost':>15}")
    print("─"*32)
    for kasus_name, (alloc, cost) in results.items():
        print(f"{kasus_name:<15} Rp {cost:>13,}")
    print("="*70)
