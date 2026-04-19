<drac2>
ch = character()
args = "&*&".split()
pb = int(ch.stats.prof_bonus)
ember_cc = "Emberbrand"
cc_ammo = "Dragon Ammo"

# 1. Input & Overclock Check
mode = args[0].lower() if args else "mace"
overclock_active = False
pwr_msg = ""
dmg_bonus = ""

if "-power" in args:
    if ch.cc_exists(ember_cc) and ch.get_cc(ember_cc) > 0:
        ch.mod_cc(ember_cc, -1)
        overclock_active = True
        # Pulling bonus from PB as requested in original logic
        dmg_bonus = f"+{pb}"
        pwr_msg = f'\n\n**[FERNIAN OVERCLOCK]** {ember_cc} channeled! +{pb} DMG.'
        
        if vroll("1d100").total > 75:
            frags = [
                "The Crescent shall rise when the Flame meets the Metal.",
                "The Scavenger's Will is the Key to the Shattered Gates.",
                "The Threefold Source flows through the one who Mends the Soul."
            ]
            pwr_msg += f'\n**[PROPHECY FRAGMENT]** The handle vibrates: *"{frags[vroll(f"1d{len(frags)}-1").total]}"*'
    else:
        pwr_msg = f'\n\n**[OVERCLOCK FAILED]** No {ember_cc} charges available!'

# 2. Mode Logic
# This helper finds the attack on your sheet so the math stays in the CSV
def get_atk(name):
    return next((a for a in ch.attacks if name.lower() in a.name.lower()), None)

if mode in ["mace", "smash"]:
    atk = get_atk("Tinkering Wrench") or get_atk("Mace")
    if not atk: return 'echo "Error: Could not find Mace/Wrench attack on sheet."'
    
    title = "Tinkering Wrench: Kinetic Mace"
    desc = "Ger locks the gears into a rigid clubbing form."
    # Use the attack object's roll method to include sheet bonuses
    res = atk.roll(d_bonus=dmg_bonus)
    fields = f'-f "Attack|{res.attack.full}" -f "Damage|{res.damage.full}"'

elif mode in ["rail", "gun"]:
    atk = get_atk("Railgun") or get_atk("Rail-Wrench")
    if not atk: return 'echo "Error: Could not find Railgun attack on sheet."'
    
    if not ch.cc_exists(cc_ammo):
        ch.create_cc(cc_ammo, 0, 10, "long", "bubble")
    
    if ch.get_cc(cc_ammo) > 0:
        ch.mod_cc(cc_ammo, -1)
        title = "Tinkering Wrench: Rail Driver"
        desc = "Miniature magnetic coils accelerate a jagged scrap slug."
        res = atk.roll(d_bonus=dmg_bonus)
        fields = f'-f "Attack|{res.attack.full}" -f "Damage|{res.damage.full}" -f "Slugs|{ch.get_cc(cc_ammo)}/10"'
    else:
        return 'echo "CLICK. Out of scrap slugs!"'

elif mode in ["mend", "wrench", "fix"]:
    title = "Tinkering Wrench: Maintenance Mode"
    desc = "Ger realigns Vyrakath’s internal servos."
    # Mending is often a static value or level-based, but could be pulled from an 'Attack' entry if desired
    fields = f'-f "Mending|{vroll("2d6").full} HP restored to Vyrakath."'

else:
    return f'echo Unknown mode: {mode}. Use mace, rail, or mend.'

return f'embed -title "{title}" -desc "{desc}{pwr_msg}" {fields}'
</drac2>