import json
import os
from collections import defaultdict

def main():
    lvl_data_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(lvl_data_path)
    print(f"Scanning {lvl_data_path}")
    
    if not os.path.exists(lvl_data_path):
        print(f"Invalid Path! Could not find: {lvl_data_path}\n")
        input()
        return

    max_id = 0
    ids = dict()
    total_files = 0

    for root, dirs, files in os.walk(lvl_data_path):
        dirs[:] = [d for d in dirs if not d.startswith('_')]

        for file in files:
            if file.startswith('_'):
                continue

            if file.endswith(".json"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, lvl_data_path)
                
                try:
                    with open(full_path, "r", encoding='utf-8') as f:
                        data = json.load(f)
                        current_id = data.get("levelNumber", 0)
                        
                        ids[rel_path] = current_id
                        total_files += 1
                        
                        if current_id > max_id:
                            max_id = current_id
                except (json.JSONDecodeError, KeyError, PermissionError):
                    continue
            
    grouped_ids = defaultdict(list)
    for rel_path, lvl_id in ids.items():
        grouped_ids[lvl_id].append(rel_path)

    conflicts = {lvl_id: files for lvl_id, files in grouped_ids.items() if len(files) > 1}

    print("-" * 30)
    if not conflicts:
        print(f"Success! Checked {total_files} files.")
        print(f"No ID conflicts found. Max ID currently in use: {max_id}")
    else:
        print(f"CRITICAL: Found {len(conflicts)} ID conflicts!")
        for lvl_id, files in conflicts.items():
            print(f"[ID {lvl_id}] is shared by:")
            for f in files:
                print(f"  -> {f}")
            print()
            
    print("-" * 30)
    print("Press Enter to close.")
    input()

if __name__ == '__main__':
    main()
