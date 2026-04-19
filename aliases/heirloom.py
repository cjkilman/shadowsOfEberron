<drac2>
ch = character()
args = "&*&".split()
mode = args[0].lower() if args else "attack"
target_type = args[1].lower() if len(args) > 1 else ""

# 1. FIND THE HEIRLOOM
atk = next((a for a in ch.attacks if "(Heirloom)" in a.name), None)
if not atk: 
    return 'echo "Add \'(Heirloom)\' to your weapon name in the character sheet."'

base_name = atk.name.split('(')[0].strip()
props = atk.raw['props'].lower()

# --- KEYWORD PARSING & COMBAT ENGINE ---
crit_num = 19 if "crit19" in props else (18 if "crit18" in props else 20)
res = atk.roll(crit=crit_num)

extra_text = ""
cc_text = ""

# 2. CHARGES & COUNTERS LOGIC
import re
charge_match = re.search(r'charges\((\d+)\)', props)
if charge_match:
    max_charges = int(charge_match.group(1))
    cc_name = f"{base_name} Charges"
    reset_type = "long" if "reset(long)" in props else ("short" if "reset(short)" in props else "none")

    # Auto-create the counter if it does not exist
    if not ch.cc_exists(cc_name):
        ch.create_cc_nx(cc_name, 0, max_charges, reset_type, "bubble")
        ch.set_cc(cc_name, max_charges)
        cc_text = f'\n-f "System|Created Counter: {cc_name} ({max_charges}/{max_charges})"'

    # Decrement charge if using a special mode
    if mode in ["repair", "pulse", "smite"] and ch.cc_exists(cc_name):
        if ch.get_cc(cc_name) > 0:
            ch.mod_cc(cc_name, -1)
            cc_text += f'\n-f "Charges|{cc_name}: {ch.get_cc(cc_name)}/{max_charges} (-1)"'
        else:
            return f'echo "You are out of charges for {base_name}!"'

# 3. ACTION-TRIGGER MODES
if "repair" in props and mode == "repair":
    extra_text += f'\n-f "Repair|{vroll("2d8+INT").full} [HP] restored to the target."'
elif "pulse" in props and mode == "pulse":
    extra_text += f'\n-f "Pulse|{vroll("2d10+INT").full} [Force] damage to the area."'
elif "smite" in props and mode == "smite":
    extra_text += f'\n-f "Smite|{vroll("2d8").full} [Radiant] damage added to the strike!"'

# 4. PASSIVE & ELEMENTAL TAGS (Triggers on standard attacks)
if mode not in ["repair", "pulse", "smite"]:
    if "fire" in props:
        extra_text += '\n-f "Elemental|The target is ignited by searing flames!"'
    elif "lightning" in props:
        extra_text += '\n-f "Elemental|Crackling energy arcs across the target!"'
    elif "force" in props:
        extra_text += '\n-f "Elemental|A concussive blast of raw magic strikes the target!"'
    elif "cold" in props:
        extra_text += '\n-f "Elemental|Frost creeps across the target, chilling them to the bone!"'

    # Bane Logic: bane(creature)
    bane_match = re.search(r'bane\(([a-z]+)\)', props)
    if bane_match:
        bane_type = bane_match.group(1)
        # Check if the player typed the creature type in their command
        if target_type == bane_type or mode == bane_type:
            bane_dmg = vroll("2d6")
            extra_text += f'\n-f "Bane ({bane_type.title()})|{bane_dmg.full} extra damage!"'
        else:
            extra_text += f'\n-f "Bane|Weapon glows, seeking {bane_type.title()}..."'

    # Bypass Resistance tags
    bypass = []
    if "magical" in props: bypass.append("Magical")
    if "silvered" in props: bypass.append("Silvered")
    if "adamantine" in props: bypass.append("Adamantine")
    if bypass:
        extra_text += f'\n-f "Properties|{", ".join(bypass)} (Bypasses standard resistances)"'

# 5. OUTPUT
return f'embed -title "{ch.name} uses {base_name}" -f "Attack|{res.attack.full}" -f "Damage|{res.damage.full}" {extra_text} {cc_text}'
</drac2>