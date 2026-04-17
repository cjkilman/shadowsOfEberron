---

## 🛠️ SHADOWS OF EBERRON - AVRAE WORKSPACE
**Project:** Crescent Kingdom Character Marks & Automation  
**Dev:** CJ Kilman (Gerolkae)  
**Environment:** Linux Mint / VS Code / Avrae Draconic (Python 3.x)

---

### 📂 FILE STRUCTURE
```text
/shadows-of-eberron
│
├── /aliases/      (Standalone Commands)
│   └── tinker.py   - Logic for Artificer Magical Tinkering
│
├── /snippets/     (Attack/Check Modifiers)
│   ├── emberbrand.py - Fire dmg + charge tracking
│   └── silverveil.py - Illusion/Stealth mechanics
│
├── /counters/     (Data Schema - Text files for !cc strings)
│   ├── emberbrand.txt  - 4 charges, Long Rest reset
│   ├── tinkering.txt   - INT-based bubble count
│   └── rail-hound.txt  - Steel Defender HP tracking
│
└── README.md      (This file)
```

---

### 🚀 DEPLOYMENT PROTOCOL
1. **LOCAL DEV:** Edit `.py` files in VS Code for syntax highlighting.
2. **COUNTER SYNC:** If counters are missing, copy/paste string from `/counters/*.txt` to Discord.
3. **LOGIC SYNC:** - **Discord Test:** Use `!servsnippet [name] <drac2>[paste code]</drac2>`
   - **Workbench:** Paste pure code (NO TAGS) into [avrae.io](https://avrae.io).
4. **REFRESH:** Run `!update` in Discord to pull new GSheet stats and Workshop changes.

---

### 📉 ACTIVE COUNTER REGISTRY
| Counter Name | Max | Reset | Purpose |
| :--- | :--- | :--- | :--- |
| **Emberbrand** | 4 | Long | Elemental Fire Flare (1d6) |
| **Magical Tinkering** | INT | Long | Utility item slots |
| **Infusion: Railgun** | 1 | Long | Repeating Shot / Lightning logic |

---

### 📝 DEV NOTES
* **Case Sensitivity:** Avrae is strict. `Emberbrand` != `emberbrand`.
* **Indentation:** Use 4 spaces only. No tabs (Python nuanced).
* **Local-First:** Always keep the master logic in this directory. Discord/Avrae is the "production" server; this folder is "Source Control."

---

## 💻 ENVIRONMENT
**OS:** Windows 10/11
**Root:** C:\Users\gerol\Documents\DnD\Server Aliases\
**Line Endings:** LF (Crucial for Avrae/Discord compatibility)

---

### 🔧 NEXT TASK: "SILVER VEIL"
* **Status:** Pending.
* **Goal:** Create logic to buff Stealth or Deception checks using a dedicated charge pool.

---

