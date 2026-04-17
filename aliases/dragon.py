<drac2>
ch = character()
args = "&*&".split()
pb = int(character().stats.prof_bonus)
ember_cc = "Emberbrand"

# 1. Input & Status Check
is_out = "-fail" in args or "-auto" in args
active_module = "bite" 
if args:
    input_mode = args[0].lower()
    valid_modes = ["bite", "railgun", "flame", "wings", "sync", "cocoon", "aegis"]
    if input_mode in valid_modes:
        active_module = input_mode

# 2. THE OVERCLOCK & PROPHECY LOGIC
overclock_active = False
pwr_msg = ""
if "-power" in args:
    if ch.cc_exists(ember_cc) and ch.get_cc(ember_cc) > 0:
        ch.mod_cc(ember_cc, -1)
        overclock_active = True
        pwr_msg = f'\n\n**[FERNIAN OVERCLOCK]** {ember_cc} consumed! +{pb} DMG.'
        if vroll("1d100").total > 75:
            frags = ["The Crescent shall rise when the Flame meets the Metal.", "Memory is the only geography that cannot be burned.", "The Threefold Source flows through the one who Mends the Soul."]
            pwr_msg += f'\n**[PROPHECY FRAGMENT]** Vyrakath\'s voice clears: *"{frags[vroll(f"1d{len(frags)}-1").total]}"*'

# 3. EMERGENCY PROTOCOL (Priority #1)
if is_out:
    title = "EMERGENCY PROTOCOL: Vyrakath Takeover"
    stability = vroll("1d6").total
    if stability <= 2:
        desc = "Engineer vital signs critical. Deploying Mag-Lock Saddle and extracting."
        fields = '-f "Protocol|Defensive Extraction (Gero moved 15ft)"'
    elif stability <= 4:
        dmg = vroll(f"1d8+2+{pb if overclock_active else 0}")
        desc = "KATH-Protocol active. Protecting the Creator."
        fields = f'-f "Action: Bite|Dmg: {dmg.full} [force]"'
    else:
        desc = "VYRA-Overclock: Planar Surge! STAND CLEAR."
        fields = f'-f "Action: Planar Surge|Dmg: {vroll("3d6").full} [fire]"'
    return f'embed -title "{title}" -desc "*{desc}*{pwr_msg}" {fields} -color 00ff00'

# 4. WEAPON & UTILITY MODULES
if active_module == "bite":
    title, desc = "Vyrakath: Ironfang Bite", "The steel jaw snaps shut with hydraulic force."
    fields = f'-f "Attack|{vroll(f"1d20+{pb+3}").full}" -f "Damage|{vroll(f"1d8+2+{pb if overclock_active else 0}").full} [force]"'

elif active_module in ["cocoon", "aegis"]:
    title, desc = "Vyrakath: Armored Cocoon", "Plating shifts and overlaps, forming a protective cradle for the rider."
    fields = '-f "Defense|Gero has Three-Quarters Cover (+5 AC/DEX Saves)" -f "Status|Mag-Lock Saddle Engaged (Gero cannot fall off)"'

# ... (Insert your existing Railgun/Flame/Wings modules here)

return f'embed -title "{title}" -desc "{desc}{pwr_msg}" {fields}'
</drac2>