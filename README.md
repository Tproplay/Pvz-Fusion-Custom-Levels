
---

# **How to install**


1. Download and extract the latest release.
2. Put the `CustomLevelsLoader.dll` into your mods folder.
3. Put the levels folder in your game folder
   
   `C:\Users\(User)\AppData\LocalLow\LanPiaoPiao\PlantsVsZombiesRH\Saves\(Save file)\LevelData\Levels`
   
    or
   
   `C:\Users\(User)\AppData\LocalLow\LanPiaoPiao\PlantsVsZombiesRH\LevelData\Levels`
4. (Optional) Put the `ID checker.py` file into the same folder and run it to insure there is no conflicting Level ids.
   If there is conflicting ids, edit your json file and change the "levelNumber" to something else.
5. Run the game.

---

## 📂 File Overview

### 1. `CustomLevelsLoader.dll`
The game normally only reads level files if they are sitting directly in the root `Levels` folder. This mod allows you to organize your levels into subfolders (e.g., by world, difficulty, or author).

*   **How it works:** When you start the game, the mod "flattens" your folder structure by moving all `.json` files from subfolders into the main folder so the game can see them.
*   **Automatic Cleanup:** When you close the game normally, it remembers where every file came from and moves them back into their original folders.
*   **Safety Features:** If two folders have a file with the same name, the mod renames them during the game session (e.g., `World1_level1.json`) to prevent them from overwriting each other.

### 2. `ID checker.py`
The game identifies levels using an internal `levelNumber` inside the JSON code, not by the filename. If two different files use the same ID, the game will crash or glitch.

*   **How it works:** This script scans your entire level collection and checks the internal data of every file.
*   **Conflict Detection:** It will warn you if two files share the same ID.
*   **Development Aid:** It tells you the highest ID currently in use, making it easy to know what number to give your next custom level.

---

## ⚠️ Important Rules
*   **Don't Force Close:** Always exit the game through the menu. If you use Task Manager or the game crashes, the mod won't have time to move your files back to their subfolders.
*   **Ignore Folders:** If you want to hide a folder from the game (for backups or unfinished work), start the folder name with an underscore (e.g., `_Backup`). Both the mod and the script will skip these folders.

