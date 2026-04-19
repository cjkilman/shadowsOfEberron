<drac2>
ch = character()
c = combat()
p = argparse(&ARGS&)
targets = p.get("t")
raw_args = "&*&".lower()

# 1. FIND THE HEIRLOOM
heirlooms = [a for a in ch.attacks if "(Heirloom)" in a.name]
if not heirlooms: 
    return 'echo "Add \'(Heirloom)\' to your weapon name in the character sheet."'

atk = heirlooms[0]
base_name = atk.name.split('(')[0].strip()
props = atk.raw.get('details', '').lower()

extra_text = ""
cc_text = ""
total_damage = 0

# 2. CHARGES & COUNTERS LOGIC
charge_match = False
max_charges = 0
if "charges(" in props:
    start = props.find("charges(") + 8
    end = props.find(")", start)
    if end != -1 and props[start:end].isdigit():
        max_charges = int(props[start:end])
        charge_match = True

if charge_match:
    cc_name = f"{base_name} Charges"
    reset_type = "long" if "reset(long)" in props else ("short" if "reset(short)" in props else "none")

    if not ch.cc_exists(cc_name):
        ch.create_cc_nx(cc_name, 0, max_charges, reset_type, "bubble")
        ch.set_cc(cc_name, max_charges)
        cc_text = f'\n-f "System|Created Counter: {cc_name} ({max_charges}/{max_charges})"'

    if ("repair" in raw_args or "pulse" in raw_args or "smite" in raw_args) and ch.cc_exists(cc_name):
        if ch.get_cc(cc_name) > 0:
            ch.mod_cc(cc_name, -1)
            cc_text += f'\n-f "Charges|{cc_name}: {ch.get_cc(cc_name)}/{max_charges} (-1)"'
        else:
            return f'echo "You are out of charges for {base_name}!"'

# 3. ACTION-TRIGGER MODES (Bypasses normal attack)
if "repair" in props and "repair" in raw_args:
    roll = vroll("2d8+"+str(ch.stats.get_mod("int")))
    target_results = ""
    if c and targets:
        for t_name in targets:
            t = c.get_combatant(t_name)
            if t:
                t.modify_hp(roll.total)
                target_results += f'\n-f "⚕️ {t.name} (Healed)|{t.hp}/{t.max_hp} HP (+{roll.total})"'
    return f'embed -title "{ch.name} uses {base_name} (Repair Mode)" -f "Repair|{roll.full} [HP] restored." {cc_text} {target_results}'

elif "pulse" in props and "pulse" in raw_args:
    roll = vroll("2d10+"+str(ch.stats.get_mod("int")))
    target_results = ""
    if c and targets:
        for t_name in targets:
            t = c.get_combatant(t_name)
            if t:
                t.modify_hp(-roll.total)
                target_results += f'\n-f "💥 {t.name} (Hit)|{t.hp}/{t.max_hp} HP (-{roll.total})"'
    return f'embed -title "{ch.name} uses {base_name} (Pulse Mode)" -f "Pulse|{roll.full} [Force] damage." {cc_text} {target_results}'

elif "smite" in props and "smite" in raw_args:
    smite_roll = vroll("2d8")
    total_damage += smite_roll.total
    extra_text += f'\n-f "Smite|{smite_roll.full} [Radiant] damage added!"'

# --- THE FIX: BULLETPROOF AUTOMATION PARSER ---
stats = {
    "strengthMod": ch.stats.get_mod("str"),
    "dexterityMod": ch.stats.get_mod("dex"),
    "constitutionMod": ch.stats.get_mod("con"),
    "intelligenceMod": ch.stats.get_mod("int"),
    "wisdomMod": ch.stats.get_mod("wis"),
    "charismaMod": ch.stats.get_mod("cha"),
    "proficiencyBonus": ch.stats.prof_bonus,
    "characterLevel": ch.levels.total_level
}

atk_bonus_str = "0"
dmg_parts = []

auto = atk.raw.get("automation", [])
if typeof(auto) in ["list", "SafeList"]:
    for step in auto:
        effects = []
        if typeof(step) in ["dict", "SafeDict"]:
            if step.get("type") == "target":
                effects = step.get("effects", [])
            elif step.get("type") == "attack":
                effects = [step]
        
        if typeof(effects) in ["list", "SafeList"]:
            for eff in effects:
                if typeof(eff) in ["dict", "SafeDict"] and eff.get("type") == "attack":
                    atk_bonus_str = str(eff.get("attackBonus", "0"))
                    hits = eff.get("hit", [])
                    if typeof(hits) in ["list", "SafeList"]:
                        for hit in hits:
                            if typeof(hit) in ["dict", "SafeDict"] and hit.get("type") == "damage":
                                dmg_parts.append(str(hit.get("damage", "0")))

for stat, val in stats.items():
    atk_bonus_str = atk_bonus_str.replace(stat, str(val))
    for i in range(len(dmg_parts)):
        dmg_parts[i] = dmg_parts[i].replace(stat, str(val))

base_dmg = "+".join(dmg_parts) if dmg_parts else "1d4"
# ----------------------------------

# 4. STANDARD COMBAT ENGINE
crit_num = 19 if "crit19" in props else (18 if "crit18" in props else 20)

d20 = vroll("1d20")
is_crit = d20.total >= crit_num
hit_roll = vroll(f"{d20.total}+{atk_bonus_str}")
hit_text = f"{hit_roll.full}" + (" **(CRIT!)**" if is_crit else "")

if is_crit:
    dmg_roll = vroll(f"{base_dmg}+{base_dmg}") 
else:
    dmg_roll = vroll(base_dmg)

total_damage += dmg_roll.total

# 5. PASSIVE & ELEMENTAL TAGS
if "fire" in props: extra_text += '\n-f "Elemental|The target is ignited by searing flames!"'
elif "lightning" in props: extra_text += '\n-f "Elemental|Crackling energy arcs across the target!"'
elif "force" in props: extra_text += '\n-f "Elemental|A concussive blast of raw magic strikes the target!"'
elif "cold" in props: extra_text += '\n-f "Elemental|Frost creeps across the target, chilling them to the bone!"'

if "bane(" in props:
    start = props.find("bane(") + 5
    end = props.find(")", start)
    if end != -1:
        bane_type = props[start:end].strip()
        if bane_type in raw_args:
            bane_dmg = vroll("2d6")
            total_damage += bane_dmg.total
            extra_text += f'\n-f "Bane ({bane_type.title()})|{bane_dmg.full} extra damage!"'
        else:
            extra_text += f'\n-f "Bane|Weapon glows, seeking {bane_type.title()}..."'

# 6. TARGETING & AUTO-DAMAGE APPLICATION
target_results = ""
if c and targets:
    for t_name in targets:
        t = c.get_combatant(t_name)
        if t:
            if is_crit or hit_roll.total >= t.ac:
                t.modify_hp(-total_damage)
                target_results += f'\n-f "💥 {t.name} (Hit)|{t.hp}/{t.max_hp} HP (-{total_damage})"'
            else:
                target_results += f'\n-f "🛡️ {t.name} (Miss)|AC is {t.ac}"'
        else:
            target_results += f'\n-f "Targeting|Could not find \'{t_name}\' in combat."'

# 7. OUTPUT
return f'embed -title "{ch.name} attacks with {base_name}" -f "Attack|{hit_text}" -f "Damage|{dmg_roll.full}" {extra_text} {cc_text} {target_results}'
</drac2>