from steppingstone import stepping_stone

origin      = ['Depot 1', 'Depot 2', 'Depot 3', 'Depot 4']
destination = ['Kota A', 'Kota B', 'Kota C', 'Kota D', 'Kota E']
cost_table  = [[10,15,20,12,18], [12,18,14,16,20], [15,12,16,18,14], [18,16,15,14,12]]
need_orig   = [50, 60, 40, 70, 50]
avail_orig  = [60, 80, 70, 60]
alloc_vam   = [[0,0,0,0,60], [0,0,0,80,0], [0,60,10,0,0], [50,0,30,0,0]]

alloc, cost, iters = stepping_stone(origin, destination, cost_table, need_orig, avail_orig, alloc_vam, show_details=True)
print(f"\nJumlah iterasi: {iters}, Total cost: {cost}")
