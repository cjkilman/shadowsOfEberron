<drac2>
# 1. CONTEXT
ch = character()
c = combat()
args = &ARGS&
p = argparse(args)
m = args[0].lower() if args else "bite"

# 2. DATA SYNC (TRUST THE SHEET)
# This finds the attack object created by your GSheet formulas
atk = ([a for a in ch.attacks if m in a.name.lower()] + [None])[0]

# 3. HIT & DAMAGE STRINGS
# If sheet is found, use its values. Otherwise, use 12 Int (+1) + 5th Level (+3)
h_bonus = atk.bonus if atk else (intelligenceMod + proficiencyBonus)
d_expr = atk.damage if atk else (f"2d10 + {intelligenceMod}" if "rail" in m else f"1d8 + {proficiencyBonus}")

# 4. ROLLS (With Crit Handling)
h_roll = vroll(f"1d20 + {h_bonus}")
# Automatically doubles dice if the d20 is a 20
d_roll = vroll(d_expr, crit=(h_roll.result.crit == 1))

# 5. MECHANICAL TARGETING (-t)
targets = p.get("t")
fields, damage_cmds = "", []

if c and targets:
    for t_name in targets:
        t = c.get_combatant(t_name)
        if t:
            # Check against target AC
            if h_roll.total >= t.ac or h_roll.result.crit == 1:
                # Generates the actual command to reduce HP
                damage_cmds.append(f'!i hp "{t.name}" -{d_roll.total}')
                fields += f' -f "{t.name} (Hit)|HP -{d_roll.total} (AC {t.ac})"'
            else:
                fields += f' -f "{t.name} (Miss)|AC {t.ac}"'

# 6. ASSEMBLY
out = ["multiline"]
pet_name = f"{ch.name}'s Defender"

# Auto-deploy pet to initiative if missing
if c and not c.get_combatant(pet_name):
    out.append(f'!i add {c.me.init if c.me else 0} "{pet_name}" -hp 24 -ac 17')

# Result Embed
out.append(f'!embed -title "{pet_name}: {m.title()}" -f "Result|{h_roll}" -f "Damage|{d_roll}" {fields} -color 00ff00')

# Execute HP reduction commands
if damage_cmds:
    out.extend(damage_cmds)

return "\n".join(out)
</drac2>