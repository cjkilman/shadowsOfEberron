--------------------------------------------------
SHADOWS OF EBERRON - AVRAE WORKSPACE
Project: Crescent Kingdom Character Marks & Automation
Dev: CJ Kilman (Gerolkae)
--------------------------------------------------

[FILE STRUCTURE]
/shadows-of-eberron
|-- collection.yaml
|-- readme.md
|-- /aliases/
|   |-- powermark.py
|-- /snippets/
|   |-- emberbrand.py
|   |-- silverveil.py
|   |-- dragon.py
|-- /counters/
|   |-- powermarks.txt

[DEPLOYMENT PROTOCOL]
1. LOCAL DEV: Edit .py files in VS Code.
2. COUNTER SYNC: Copy/paste string from /counters/*.txt to Discord.
3. LOGIC SYNC: Paste .py contents into Discord (Ctrl+Shift+V).
4. REFRESH: Run !update in Discord.

[ACTIVE COUNTER REGISTRY]
Name           | Max | Reset | Purpose
--------------------------------------------------
Emberbrand     | 4   | Long  | Elemental Fire Flare (1d6)
Silver Veil    | 4   | Long  | Illusion/Stealth mechanics (1d4)
Dragon Ammo    | 10  | Long  | Scrap-metal slugs for the Railgun module.
Fuel Tank      | 3   | Long  | Pressurized Fernian essence for the Flamethrower.
Planar Battery | 5   | Long  | Power for Soarsled wings and high-mobility flight.

[ENVIRONMENT]
Line Endings: LF (Crucial for Avrae/Discord compatibility)
--------------------------------------------------