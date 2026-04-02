#  PvZ Fusion Custom Levels

#### Two files are recommended too use with this Level pack for easier load
---

## 📥 Subfolder Loader
This is a **MelonLoader** mod that allows the game to level JSON files nested within subfolders—a feature natively unsupported by the game engine.

### **How it Works**
*   **Dynamic Flattening:** Upon game startup, the mod scans all subfolders and moves `.json` files to the root `Levels` directory so the game can detect them.
*   **Collision Prevention:** If two different folders contain a file with the same name (e.g., `World1/level1.json` and `World2/level1.json`), the mod renames them to `World1_level1.json` during the session to prevent overwriting.
*   **Automatic Restoration:** When the game is closed normally, the mod moves every file back to its original subfolder, keeping your directory structure clean.
*   **Ignore System:** Any folder or file starting with an underscore (e.g., `_Drafts/` or `_Obsolete/`) is ignored by the loader.

### **Installation**
1.  Ensure [MelonLoader](https://github.com/lavagang/melonloader) is installed.
2.  Place the compiled `SubfolderLoader.dll` into your game's `Mods` folder.
3.  Organize your `.json` files into subfolders within:
    `%USERPROFILE%\AppData\LocalLow\LanPiaoPiao\PlantsVsZombiesRH\LevelData\Levels\`

---

## 🐍 Helper Tool: ID Conflict Checker
Because the game identifies levels by an internal `levelNumber` key inside the JSON (not by the filename), it is easy to accidentally assign the same ID to two different levels. This script validates your library before you play.

### **Usage**
1.  Place the `id_check.py` script inside your `Levels` folder.
2.  Run the script using Python.
3.  **The script will:**
    *   Deep-scan all subfolders (respecting the `_ignore` rule).
    *   Flag **CRITICAL** errors if two different files share the same `levelNumber`.
    *   Display the **Max ID** currently in use to help you assign the next available ID.

---

## 📂 Example Directory Structure
The mod and helper script are designed to work together seamlessly:

```text
Levels/
├── id_check.py           <-- Run this to check for ID errors
├── Adventure_Mode/
│   ├── level1.json       (Internal ID: 1)
│   └── level2.json       (Internal ID: 2)
├── Hard_Mode/
│   └── level1.json       (Internal ID: 101)
└── _Testing/             <-- This folder is IGNORED by the mod
    └── buggy_level.json
```
### ⚠️ Important Notes
* **Graceful Exit**: You must close the game normally for the mod to restore files to their subfolders. If the game crashes or is killed via Task Manager, the files will remain in the root Levels folder.
* **Manual Recovery**: If a crash occurs, simply move the files back to their original folders manually, or run the game again and close it properly to trigger the restoration.
* **Data Integrity**: Always run the ID Conflict Checker after adding new levels to prevent loading glitches or crashes.
