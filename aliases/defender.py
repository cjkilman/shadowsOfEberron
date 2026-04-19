<drac2>
ch = character()
c = combat()
p = argparse(&ARGS&)
input_mode = &ARGS&[0].lower() if &ARGS& else "bite"

# 1. FIND THE ATTACK OBJECT
# Avrae maps the GSheet "Attack Name" to a list of attack objects.
atk = ([a for a in ch.attacks if input_mode in a.name.lower() and "[def]" in a.name.lower()] + [None])[0]

if not atk:
    return f'echo "No module \'{input_mode} [Def]\' found on sheet."'

# 2. THE VERIFIED DATA EXTRACTION
# Avrae dumps GSheet "Notes" into atk.description
import re
raw_notes = atk.description.lower() if atk.description else ""

# Search for "hp: ##" and "ac: ##" within that text block
hp_search = re.search(r'hp:\s*(\d+)', raw_notes)
ac_search = re.search(r'ac:\s*(\d+)', raw_notes)

# Assign variables: Use the found number, or fall back to defaults
def_hp = int(hp_search.group(1)) if hp_search else 24
def_ac = int(ac_search.group(1)) if ac_search else 17

# 3. INITIATIVE SYNC & INJECTION
pet_name = p.get("name")[0] if p.get("name") else f"{ch.name}'s Defender"
pet = c.get_combatant(pet_name) if c else None

if c and not pet:
    # Use the character's current initiative to place the pet
    my_init = c.me.init if c.me else 0
    pet = c.add_combatant(pet_name, init=my_init, hp=def_hp, ac=def_ac)
    status = f'-f "System|{pet_name} deployed (HP: {def_hp}, AC: {def_ac}) at Init {my_init}."'
else:
    status = ""

# 4. EXECUTE THE ATTACK
res = atk.roll()
# ... (standard targeting logic) ...
return f'embed -title "{pet_name}: {atk.name.replace("[Def]","")}" -f "Result|{res.attack.full}" -f "Damage|{res.damage.full}" {status} -color 00ff00'
</drac2>