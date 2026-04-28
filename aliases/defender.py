<drac2>
# 1. CONTEXT & STATS
ch, c, args = character(), combat(), &ARGS&
p, m = argparse(args), args[0].lower() if args else "bite"

# THE FIX: Properly calling stats from the character sheet
int_mod = ch.stats.get_mod("int")
prof = ch.stats.prof_bonus
level = ch.levels.total_level

pet_hp = 2 + int_mod + (5 * level)
pet_ac = 15 + prof

# 2. DATA SYNC (Ammo Check)
atk = ([a for a in ch.attacks if m in a.name.lower()] + [None])[0]
ammo_name = atk.raw.get('ammo') if atk else None
has_ammo = ch.get_cc(ammo_name) > 0 if ammo_name else True

# 3. ROLLS (Only if has_ammo)
if not has_ammo:
    return f'echo You are out of {ammo_name}!'

h_bonus = atk.bonus if atk else f"{int_mod} + {prof}"
d_expr = atk.damage if atk else f"1d8 + {prof}"

# THE FIX: Secure Critical Hit handling
d20 = vroll("1d20")
is_crit = d20.total == 20
h_roll = vroll(f"{d20.total} + {h_bonus}")

if is_crit:
    d_roll = vroll(f"{d_expr} + {d_expr}")
else:
    d_roll = vroll(d_expr)

# 4. AMMO DEDUCTION
if ammo_name:
    ch.mod_cc(ammo_name, -1)

# 5. MECHANICAL TARGETING
targets, fields, damage_cmds = p.get("t"), "", []
if c and targets:
    for t_name in targets:
        t = c.get_combatant(t_name)
        if t and (h_roll.total >= t.ac or is_crit):
            damage_cmds.append(f'!i hp "{t.name}" -{d_roll.total}')
            fields += f' -f "{t.name} (Hit)|HP -{d_roll.total} (AC {t.ac})"'
        elif t:
            fields += f' -f "{t.name} (Miss)|AC {t.ac}"'

# 6. ASSEMBLY
out, pet_name = ["multiline"], f"{ch.name}'s Defender"
if c and not c.get_combatant(pet_name):
    out.append(f'!i add {c.me.init if c.me else 0} "{pet_name}" -hp {pet_hp} -ac {pet_ac} -note "Fly 30ft (Hover)"')

ammo_str = f" | {ammo_name}: {ch.get_cc(ammo_name)}" if ammo_name else ""
out.append(f'!embed -title "{pet_name}: {m.title()}" -f "Stats|HP: {pet_hp} | AC: {pet_ac}{ammo_str}" -f "Result|{h_roll.full}" -f "Damage|{d_roll.full}" {fields} -color 00ff00')
if damage_cmds: out.extend(damage_cmds)
return "\n".join(out)
</drac2>