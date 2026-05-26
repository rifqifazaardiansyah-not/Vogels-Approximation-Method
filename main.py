from data.data2 import *
from copy import deepcopy

# =========================
# COPY DATA AGAR DATA ASLI
# TIDAK BERUBAH
# =========================

matrix = deepcopy(matrix)
need = deepcopy(need)
availability = deepcopy(availability)

# =========================
# RESULT MATRIX
# =========================

allocation_matrix = []
cost_matrix = []


def reset_result_matrix():
    for i in range(len(matrix)):
        allocation_matrix.append([0] * len(matrix[0]))
        cost_matrix.append([0] * len(matrix[0]))


# =========================
# VAM PENALTY
# =========================

def calculate_penalty(costs):
    valid_costs = [x for x in costs if x is not None]

    if len(valid_costs) == 0:
        return -1

    if len(valid_costs) == 1:
        return valid_costs[0]

    valid_costs.sort()

    return valid_costs[1] - valid_costs[0]


# =========================
# HITUNG PENALTY
# =========================

def calculate_penalties():

    row_penalties = []
    col_penalties = []

    # ROW PENALTY
    for i in range(len(matrix)):

        row = []

        for j in range(len(matrix[0])):

            if need[j] is not None and matrix[i][j] is not None:
                row.append(matrix[i][j])

        row_penalties.append(calculate_penalty(row))

    # COLUMN PENALTY
    for j in range(len(matrix[0])):

        column = []

        for i in range(len(matrix)):

            if availability[i] is not None and matrix[i][j] is not None:
                column.append(matrix[i][j])

        col_penalties.append(calculate_penalty(column))

    return row_penalties, col_penalties


# =========================
# HELPER: CARI SEL TERBAIK DALAM SATU BARIS
# =========================

def best_cell_in_row(row_index):
    """
    Kembalikan (min_cost, col_index) dari sel valid di baris row_index.
    """
    min_cost = float('inf')
    col_index = -1
    for j in range(len(matrix[0])):
        if need[j] is not None and matrix[row_index][j] is not None:
            if matrix[row_index][j] < min_cost:
                min_cost = matrix[row_index][j]
                col_index = j
    return min_cost, col_index


# =========================
# HELPER: CARI SEL TERBAIK DALAM SATU KOLOM
# =========================

def best_cell_in_col(col_index):
    """
    Kembalikan (min_cost, row_index) dari sel valid di kolom col_index.
    """
    min_cost = float('inf')
    row_index = -1
    for i in range(len(matrix)):
        if availability[i] is not None and matrix[i][col_index] is not None:
            if matrix[i][col_index] < min_cost:
                min_cost = matrix[i][col_index]
                row_index = i
    return min_cost, row_index


# =========================
# HELPER: HITUNG ALOKASI MAKSIMUM PADA SEL (i, j)
# =========================

def max_allocation(row_index, col_index):
    """
    Jumlah unit yang bisa dialokasikan pada sel (row_index, col_index),
    yaitu min(availability[row_index], need[col_index]).
    """
    return min(availability[row_index], need[col_index])


# =========================
# PILIH CELL TERBAIK (dengan tie-breaking 3 level)
# =========================

def find_best_cell(row_penalties, col_penalties):
    """
    Aturan tie-breaking (urutan prioritas):
      1. Penalti terbesar → kandidat baris/kolom yang penaltinya = max_penalty
      2. Di antara kandidat, pilih yang memiliki biaya sel terkecil
      3. Jika biaya juga sama, pilih yang memungkinkan alokasi terbesar
      4. Jika alokasi juga sama, pilih baris/kolom paling atas / paling kiri
    """
    max_penalty = max(max(row_penalties), max(col_penalties))

    # Kumpulkan semua kandidat: ('row', i) atau ('col', j)
    candidates = []

    for i, p in enumerate(row_penalties):
        if p == max_penalty and availability[i] is not None:
            min_cost, best_col = best_cell_in_row(i)
            if best_col != -1:
                alloc = max_allocation(i, best_col)
                # Kandidat baris: tipe, indeks baris, indeks kolom terbaik,
                #                 biaya terkecil, alokasi maks, indeks urut (i)
                candidates.append(('row', i, best_col, min_cost, alloc, i))

    for j, p in enumerate(col_penalties):
        if p == max_penalty and need[j] is not None:
            min_cost, best_row = best_cell_in_col(j)
            if best_row != -1:
                alloc = max_allocation(best_row, j)
                # Kandidat kolom: tipe, indeks kolom, indeks baris terbaik,
                #                 biaya terkecil, alokasi maks, indeks urut (j)
                candidates.append(('col', j, best_row, min_cost, alloc, j))

    # Tie-breaking:
    #   key[0] = min_cost      → lebih kecil lebih baik  (ascending)
    #   key[1] = -alloc        → lebih besar lebih baik  (descending → pakai negatif)
    #   key[2] = urut_index    → lebih kecil lebih baik  (baris atas / kolom kiri)
    candidates.sort(key=lambda c: (c[3], -c[4], c[5]))

    winner = candidates[0]

    if winner[0] == 'row':
        return winner[1], winner[2]   # (row_index, col_index)
    else:
        return winner[2], winner[1]   # (row_index, col_index)


# =========================
# TOTAL COST
# =========================

def calculate_total_cost():

    total = 0

    for i in range(len(cost_matrix)):
        for j in range(len(cost_matrix[0])):
            total += cost_matrix[i][j]

    return total


# =========================
# MAIN VAM
# =========================

def vam():

    reset_result_matrix()

    while True:

        # STOP JIKA SEMUA SUDAH SELESAI
        if all(x is None for x in need):
            break

        row_penalties, col_penalties = calculate_penalties()

        row, col = find_best_cell(row_penalties, col_penalties)

        qty = min(availability[row], need[col])

        # SIMPAN ALOKASI
        allocation_matrix[row][col] = qty

        # SIMPAN COST
        cost_matrix[row][col] = qty * matrix[row][col]

        # UPDATE SUPPLY & DEMAND
        availability[row] -= qty
        need[col] -= qty

        # JIKA SUPPLY HABIS
        if availability[row] == 0:

            availability[row] = None

            for j in range(len(matrix[0])):
                matrix[row][j] = None

        # JIKA DEMAND HABIS
        if need[col] == 0:

            need[col] = None

            for i in range(len(matrix)):
                matrix[i][col] = None


# =========================
# RUN
# =========================

vam()

print("=== ALOKASI ===")
for row in allocation_matrix:
    print(row)

print("\n=== COST MATRIX ===")
for row in cost_matrix:
    print(row)

print("\nTOTAL COST:")
print(calculate_total_cost())