import json
for nb_name in ['02_clean_data', '03_charts']:
    nb = json.load(open(f'notebooks/{nb_name}.ipynb', encoding='utf-8'))
    print(f"########## {nb_name} — {len(nb['cells'])} cells ##########\n")
    for i, c in enumerate(nb['cells']):
        print(f"=== CELL {i} [{c['cell_type']}] ===")
        print(''.join(c.get('source', [])))
        print()