from data_distribusi_vaksin.data import *
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
# PILIH CELL TERBAIK
# =========================

def find_best_cell(row_penalties, col_penalties):

    max_row_penalty = max(row_penalties)
    max_col_penalty = max(col_penalties)

    # PILIH ROW
    if max_row_penalty >= max_col_penalty:

        row_index = row_penalties.index(max_row_penalty)

        min_cost = M
        col_index = -1

        for j in range(len(matrix[0])):

            if need[j] is not None and matrix[row_index][j] is not None:

                if matrix[row_index][j] < min_cost:
                    min_cost = matrix[row_index][j]
                    col_index = j

        return row_index, col_index

    # PILIH COLUMN
    else:

        col_index = col_penalties.index(max_col_penalty)

        min_cost = M
        row_index = -1

        for i in range(len(matrix)):

            if availability[i] is not None and matrix[i][col_index] is not None:

                if matrix[i][col_index] < min_cost:
                    min_cost = matrix[i][col_index]
                    row_index = i

        return row_index, col_index


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