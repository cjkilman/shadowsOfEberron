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
    valid_modes = ["bite", "railgun", "flamethrower", "flame", "rail", "soarsled", "wings", "recharge", "sync", "sentry", "aegis", "camp"]
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
            frags = [
                "The Crescent shall rise when the Flame meets the Metal.",
                "The Scavenger's Will is the Key to the Shattered Gates.",
                "Memory is the only geography that cannot be burned.",
                "The Threefold Source flows through the one who Mends the Soul."
            ]
            pwr_msg += f'\n**[PROPHECY FRAGMENT]** The voice clears: *"{frags[vroll(f"1d{len(frags)}-1").total]}"*'
    else:
        pwr_msg = f'\n\n**[OVERCLOCK FAILED]** No {ember_cc} charges available!'

# 3. EMERGENCY PROTOCOL
if is_out:
    title = "EMERGENCY PROTOCOL: Docent Takeover"
    stability = vroll("1d6").total
    if stability <= 2:
        desc = "Engineer vital signs critical. Redirecting planar flow."
        fields = '-f "Protocol|Defensive Extraction (Gero moved 15ft)"'
    elif stability <= 4:
        dmg = vroll(f"1d8+2+{pb if overclock_active else 0}")
        desc = "Kinetic cover established. Calculating optimal force."
        fields = f'-f "Action: Bite|Dmg: {dmg.full} [force]"'
    else:
        desc = "Overclocking Planar Battery. STAND CLEAR."
        fields = f'-f "Action: Planar Surge|Dmg: {vroll("3d6").full} [fire]"'
    return f'embed -title "{title}" -desc "*{desc}*{pwr_msg}" {fields} -color 00ff00'

# 4. WEAPON & UTILITY MODULES
if active_module == "bite":
    title = "Mechanical Dragon: Force-Bite"
    desc = "The construct's jaws hum with kinetic energy."
    fields = f'-f "Attack|{vroll(f"1d20+{pb+3}").full}" -f "Damage|{vroll(f"1d8+2+{pb if overclock_active else 0}").full} [force]"'

elif active_module in ["railgun", "rail"]:
    cc = "Dragon Ammo"
    if not ch.cc_exists(cc): ch.create_cc(cc, 0, 10, "long", "bubble", None, None, 10)
    if ch.get_cc(cc) < 1: return 'echo "OUT OF AMMO!"'
    ch.mod_cc(cc, -1)
    title, desc = "Mechanical Dragon: Railgun Mode", "Magnetic rails accelerate a scrap-metal slug."
    fields = f'-f "Attack|{vroll(f"1d20+{pb+4}").full}" -f "Damage|{vroll(f"2d10+2+{pb if overclock_active else 0}").full} [piercing]" -f "Ammo|{ch.get_cc(cc)}/10"'

elif active_module in ["flamethrower", "flame"]:
    cc = "Fuel Tank"
    if not ch.cc_exists(cc): ch.create_cc(cc, 0, 3, "long", "bubble", None, None, 3)
    if ch.get_cc(cc) < 1: return 'echo "FUEL DEPLETED!"'
    ch.mod_cc(cc, -1)
    title, desc = "Mechanical Dragon: Flamethrower", "Igniting pressurized Fernian essence."
    fields = f'-f "Save|DC {8+pb+3} DEX" -f "Damage|{vroll(f"3d6+{pb if overclock_active else 0}").full} [fire]" -f "Fuel|{ch.get_cc(cc)}/3"'

elif active_module in ["soarsled", "wings"]:
    cc = "Planar Battery"
    if not ch.cc_exists(cc): ch.create_cc(cc, 0, 5, "long", "bubble", None, None, 5)
    if ch.get_cc(cc) < 1: return 'echo "PLANAR SYNC FAILED!"'
    ch.mod_cc(cc, -1)
    title, desc = "Mechanical Dragon: Soarsled Wings", "Retractable soarwood panels deploy."
    fields = f'-f "Movement|Flight: 40ft (Hover)" -f "Evasion|+{pb} to AC/DEX Saves" -f "Battery|{ch.get_cc(cc)}/5"'

elif active_module in ["recharge", "sync"]:
    cc = "Planar Battery"
    if not ch.cc_exists(cc): ch.create_cc(cc, 0, 5, "long", "bubble", None, None, 5)
    if len(args) > 1 and args[1].isdigit():
        lvl = int(args[1])
        if ch.spellbook.get_slots(lvl) > 0:
            ch.spellbook.use_slot(lvl); ch.mod_cc(cc, lvl * 2)
            title, desc = "Arcane Siphon", f"Gero funnels a Level {lvl} slot."
        else: return f'echo "No slots!"'
    else:
        ch.mod_cc(cc, 1); title, desc = "Atmospheric Osmosis", "Catching planar currents."
    fields = f'-f "Battery|{ch.get_cc(cc)}/5"'

elif active_module in ["sentry", "aegis", "camp"]:
    cc = "Planar Battery"
    if ch.get_cc(cc) >= 2:
        ch.mod_cc(cc, -2)
        title, desc = "Mechanical Dragon: Aegis Perimeter", "The wings unfold into a wide, shimmering canopy filtering the Mournland mists."
        fields = f'-f "Perimeter|30ft Safe Zone" -f "Security|Advantage on Perception" -f "Battery|{ch.get_cc(cc)}/5"'
    else:
        return 'echo "PLANAR SYNC FAILURE: Insufficient battery!"'

return f'embed -title "{title}" -desc "{desc}{pwr_msg}" {fields}'
</drac2>