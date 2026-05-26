from copy import deepcopy

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

ROWS = 5
COLS = 5

# ============================================================
# Alokasi VAM manual yang sudah dikoreksi:
# V1 → Padang: 8000
# V2 → Pekanbaru: 15000
# V3 → Pekanbaru: 2000, Jambi: 8000, Padang: 2000 (total=12000 ✓)
# V4 → Jambi: 4000, Palembang: 4000               (total=8000  ✓)
# V5 → Palembang: 6000, Dummy: 2000               (total=8000  ✓)
# ============================================================
alloc_vam = [
    [0,     0,     8000, 0,    0   ],  # Vendor 1
    [15000, 0,     0,    0,    0   ],  # Vendor 2
    [2000,  8000,  2000, 0,    0   ],  # Vendor 3
    [0,     4000,  0,    4000, 0   ],  # Vendor 4
    [0,     0,     0,    6000, 2000],  # Vendor 5
]

# ── helpers ─────────────────────────────────────────────────

def _total_cost(alloc):
    return sum(alloc[i][j]*cost_table[i][j]
               for i in range(ROWS) for j in range(COLS))

def _basic_cells(alloc):
    return [(i,j) for i in range(ROWS) for j in range(COLS) if alloc[i][j]>0]

def _non_basic_cells(alloc):
    return [(i,j) for i in range(ROWS) for j in range(COLS) if alloc[i][j]==0]

def _print_table(alloc, eps=None, label="ALOKASI"):
    es  = set(eps) if eps else set()
    cw  = 11
    print(f"\n{'─'*70}")
    print(f"  {label}")
    print(f"{'─'*70}")
    print(f"  {'':14}" + "".join(f"{d:>{cw}}" for d in destination)
          + f"  {'Supply':>8}")
    print(f"  {'':14}" + "─"*(cw*COLS) + "  " + "─"*8)
    for i in range(ROWS):
        cells = []
        for j in range(COLS):
            if (i,j) in es and alloc[i][j]==0:
                cells.append(f"{'ε':>{cw}}")
            elif alloc[i][j]>0:
                cells.append(f"[{alloc[i][j]:,}]".rjust(cw))
            else:
                cells.append(f"{'─':>{cw}}")
        print(f"  {origin[i]:<14}" + "".join(cells)
              + f"  {availability_orig[i]:>8,}")
    print(f"  {'Demand':<14}"
          + "".join(f"{d:>{cw},}" for d in need_orig))
    print(f"\n  Total Cost : Rp {_total_cost(alloc):>15,.0f}")

# ── verifikasi ───────────────────────────────────────────────

def _verify(alloc):
    print("  Cek supply :")
    ok_all = True
    for i in range(ROWS):
        tot = sum(alloc[i])
        ok  = tot == availability_orig[i]
        ok_all = ok_all and ok
        print(f"    {origin[i]:<12}: {tot:>6,}  {'✓' if ok else f'✗ harusnya {availability_orig[i]:,}'}")
    print("  Cek demand :")
    for j in range(COLS):
        tot = sum(alloc[i][j] for i in range(ROWS))
        ok  = tot == need_orig[j]
        ok_all = ok_all and ok
        print(f"    {destination[j]:<12}: {tot:>6,}  {'✓' if ok else f'✗ harusnya {need_orig[j]:,}'}")
    return ok_all

# ── loop finder ──────────────────────────────────────────────

def _find_loop(start, basic_set):
    def dfs(path, direction):
        ci, cj = path[-1]
        if len(path) >= 4:
            si, sj = start
            if direction=='H' and ci==si: return path
            if direction=='V' and cj==sj: return path
        if len(path) > (ROWS+COLS)*2: return None
        nd    = 'V' if direction=='H' else 'H'
        moves = ([(ci,j) for j in range(COLS) if j!=cj]
                 if direction=='H'
                 else [(i,cj) for i in range(ROWS) if i!=ci])
        for nxt in moves:
            if nxt==start and len(path)>=3:
                r = dfs(path+[nxt], nd)
                if r: return r
            elif nxt in basic_set and nxt not in path:
                r = dfs(path+[nxt], nd)
                if r: return r
        return None
    return dfs([start], 'H')

def _improvement_index(loop):
    nodes = loop if loop[-1]!=loop[0] else loop[:-1]
    signed, idx = [], 0
    for k, cell in enumerate(nodes):
        s = '+' if k%2==0 else '-'
        signed.append((cell, s))
        idx += cost_table[cell[0]][cell[1]] * (1 if s=='+' else -1)
    return idx, signed

def _reallocate(alloc, signed_loop):
    theta = min(alloc[i][j] for (i,j),s in signed_loop if s=='-')
    na    = deepcopy(alloc)
    for (i,j),s in signed_loop:
        if s=='+': na[i][j] += theta
        else:      na[i][j] -= theta
    return na, theta

def _fix_degeneracy(alloc, eps):
    req = ROWS+COLS-1
    eps[:] = [c for c in eps if alloc[c[0]][c[1]]==0]
    tot = len(_basic_cells(alloc))+len(eps)
    if tot < req:
        d = req-tot
        print(f"\n  [DEGENERASI] basic={tot}, butuh={req}. Tambah {d} sel epsilon.")
        for i in range(ROWS):
            for j in range(COLS):
                c=(i,j)
                if alloc[i][j]==0 and c not in eps:
                    eps.append(c)
                    print(f"  → Epsilon: {origin[i]} → {destination[j]}")
                    d-=1
                    if d==0: break
            if d==0: break
    return alloc

# ── Stepping Stone utama ─────────────────────────────────────

def stepping_stone(alloc_init):
    alloc = deepcopy(alloc_init)
    eps   = []
    itr   = 0

    print("\n" + "="*70)
    print("         S T E P P I N G   S T O N E   M E T H O D")
    print("="*70)
    _print_table(alloc, label="SOLUSI AWAL (VAM MANUAL TERKOREKSI)")

    while True:
        itr += 1
        print(f"\n{'═'*70}")
        print(f"  ITERASI {itr}")
        print(f"{'═'*70}")

        alloc     = _fix_degeneracy(alloc, eps)
        basic     = _basic_cells(alloc)
        non_basic = _non_basic_cells(alloc)
        bset      = set(basic)|set(eps)

        print(f"\n  Jumlah sel basic    : {len(bset)}  "
              f"(syarat m+n-1 = {ROWS}+{COLS}-1 = {ROWS+COLS-1})")
        print(f"  Sel Basic    : " +
              ", ".join(f"{origin[i]}→{destination[j]}" for i,j in sorted(bset)))
        print(f"\n  Evaluasi improvement index tiap sel non-basic:")
        print(f"\n  {'Sel (dari→ke)':<32} {'Index':>9}   Loop")
        print(f"  {'─'*32} {'─'*9}   {'─'*50}")

        evals = []
        for cell in non_basic:
            if cell in eps: continue
            i, j  = cell
            label = f"{origin[i]}→{destination[j]}"
            loop  = _find_loop(cell, bset)
            if not loop:
                print(f"  {label:<32} {'N/A':>9}   Loop tidak ditemukan")
                continue
            idx, signed = _improvement_index(loop)
            lstr = " → ".join(
                f"[{'+'if s=='+' else '−'}]{origin[r]}→{destination[c]}"
                for (r,c),s in signed)
            flag = "  ◄ NEGATIF" if idx<0 else ""
            print(f"  {label:<32} {idx:>9,.0f}   {lstr}{flag}")
            evals.append((idx, loop, signed, cell))

        neg = [x for x in evals if x[0]<0]

        if not neg:
            print(f"\n  {'─'*68}")
            print(f"  ✓ Semua improvement index ≥ 0")
            print(f"  ✓ SOLUSI SUDAH OPTIMAL! Tidak perlu iterasi lagi.")
            break

        neg.sort(key=lambda x: x[0])
        bi, bl, bs, bc = neg[0]
        ri, rj = bc
        print(f"\n  {'─'*68}")
        print(f"  ► Sel masuk  : {origin[ri]} → {destination[rj]}")
        print(f"    Index      : {bi:,.0f}  (paling negatif → diprioritaskan)")
        print(f"    Loop       : " + " → ".join(
            f"[{'+'if s=='+' else '−'}]{origin[r]}→{destination[c]}"
            for (r,c),s in bs))

        minus_info = [(alloc[r][c], origin[r], destination[c])
                      for (r,c),s in bs if s=='-']
        print(f"    Nilai sel (−): " +
              ", ".join(f"{origin}→{dest}={qty:,}"
                        for qty,origin,dest in minus_info))
        theta = min(q for q,_,_ in minus_info)
        print(f"    θ = min({', '.join(str(q) for q,_,_ in minus_info)}) = {theta:,}")

        if bc in eps: eps.remove(bc)
        alloc, _ = _reallocate(alloc, bs)
        _print_table(alloc, eps, label=f"ALOKASI SETELAH ITERASI {itr}")

    # Hasil akhir
    print("\n" + "="*70)
    print("  HASIL AKHIR — SOLUSI OPTIMAL")
    print("="*70)
    _print_table(alloc, label="TABEL ALOKASI OPTIMAL")

    print(f"\n  Rincian rute aktif:")
    print(f"  {'Rute':<32} {'Qty':>8}  {'Tarif/kg':>9}  {'Subtotal':>14}")
    print(f"  {'─'*32} {'─'*8}  {'─'*9}  {'─'*14}")
    grand = 0
    for i in range(ROWS):
        for j in range(COLS):
            if alloc[i][j]>0:
                sub   = alloc[i][j]*cost_table[i][j]
                grand += sub
                rute  = f"{origin[i]} → {destination[j]}"
                print(f"  {rute:<32} {alloc[i][j]:>8,}  "
                      f"{cost_table[i][j]:>9,}  {sub:>14,}")
    print(f"  {'─'*32} {'─'*8}  {'─'*9}  {'─'*14}")
    print(f"  {'TOTAL COST':<32} {'':>8}  {'':>9}  {grand:>14,}")
    print(f"\n  Total Cost VAM awal  : Rp {_total_cost(alloc_init):>13,.0f}")
    print(f"  Total Cost Optimal   : Rp {grand:>13,.0f}")
    diff = _total_cost(alloc_init) - grand
    if diff > 0:
        print(f"  Penghematan          : Rp {diff:>13,.0f}")
    else:
        print(f"  (Tidak ada penghematan — VAM sudah optimal)")
    print("="*70)
    return alloc, grand

# ============================================================
# RUN
# ============================================================

print("="*70)
print("  VERIFIKASI ALOKASI VAM MANUAL")
print("="*70)
_print_table(alloc_vam, label="INPUT ALOKASI VAM MANUAL")
print()
valid = _verify(alloc_vam)
print(f"\n  Status : {'✓ Alokasi valid dan seimbang' if valid else '✗ Ada ketidakseimbangan'}")

stepping_stone(alloc_vam)