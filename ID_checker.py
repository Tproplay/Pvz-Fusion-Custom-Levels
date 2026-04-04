import json
import os
from collections import defaultdict
import datetime
import shutil

def ID_Checker(lvl_data_path):
    """
    Scans JSON files for 'levelNumber' and identifies duplicate IDs.
    Returns a dictionary of conflicts found.
    """
    max_id = 0
    ids = dict()
    total_files = 0

    for root, dirs, files in os.walk(lvl_data_path):
        # Modify dirs in-place to skip any folder starting with '_'
        # This prevents the script from scanning the _Backups folder
        # or the folders that needs to be ignored.
        dirs[:] = [d for d in dirs if not d.startswith('_')]

        for file in files:
            # Only process JSON files that aren't marked as hidden/temp (_)
            if file.startswith('_') or not file.endswith(".json"):
                continue

            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, lvl_data_path)
            
            try:
                with open(full_path, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    # Use .get() to avoid KeyError if 'levelNumber' is missing
                    current_id = data.get("levelNumber", 0)
                    ids[rel_path] = current_id
                    total_files += 1
                    
                    if current_id > max_id:
                        max_id = current_id
            except (json.JSONDecodeError, KeyError, PermissionError) as e:
                print(f"Skipping {file}: {e}")
                continue
            
    # Group file paths by their ID to find duplicates
    grouped_ids = defaultdict(list)
    for rel_path, lvl_id in ids.items():
        grouped_ids[lvl_id].append(rel_path)

    # Filter for IDs that appear in more than one file
    conflicts = {lvl_id: files for lvl_id, files in grouped_ids.items() if len(files) > 1}
    
    if not conflicts:
        print(f"Success! Checked {total_files} files.")
        print(f"No ID conflicts found. Max ID currently in use: {max_id}")
    else:
        print(f"CRITICAL: Found {len(conflicts)} ID conflicts!")
        for lvl_id, files in conflicts.items():
            print(f"[ID {lvl_id}] is shared by: {', '.join(files)}")
            
    print("-" * 30)
    return conflicts

def Backup(lvl_data_path):
    """
    Copies all project folders/files (excluding scripts and hidden folders) 
    into a timestamped backup directory.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    backup_dir = os.path.join(lvl_data_path, "_Backups")
    target_path = os.path.join(backup_dir, f"_backup {timestamp}")
    
    this_script = os.path.basename(__file__)
    copied = 0

    try:
        # exist_ok=True prevents errors if the folder already exists
        os.makedirs(target_path, exist_ok=True)
        
        for item in os.listdir(lvl_data_path):
            # Do not backup the script itself or existing backup/temp folders
            if item.startswith("_") or item == this_script:
                continue
            
            src = os.path.join(lvl_data_path, item)
            dst = os.path.join(target_path, item)
            
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                # copy2 preserves file metadata like 'Date Modified'
                shutil.copy2(src, dst)
            copied += 1
            
        print(f"Successfully backed up {copied} items to: {target_path}")
    except Exception as e:
        print(f"Backup failed: {e}")
    print("-" * 30)

def main():
    # Get the directory where this script is located
    lvl_data_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(lvl_data_path)
    
    print(f"Scanning: {lvl_data_path}\n" + "-" * 30)
    
    if not os.path.exists(lvl_data_path):
        print(f"Invalid Path!")
        return
    
    # Check for ID duplicates before allowing a backup
    conflicts = ID_Checker(lvl_data_path)
    
    if not conflicts:
        user_choice = input("Type 'y' to create a backup: ").lower()
        if 'y' in user_choice:
            Backup(lvl_data_path)
            
    input("Press Enter to close.")

if __name__ == '__main__':
    main()
