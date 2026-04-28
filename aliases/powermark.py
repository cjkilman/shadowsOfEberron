<drac2>
ch = character()
args = "&*&".split()
char_name = ch.name

# 1. Basic Usage Check
if not args:
    return f'echo Usage: !powermark <ember/silver/iron/star/earth> [dice]'

mark_type = args[0].lower()
switch_requested = "-switch" in [a.lower() for a in args]

# 2. Define the Marks in a cleaner Dictionary
marks = {
    "ember": {"cc": "Emberbrand", "dice": "1d6", "dmg": "[fire]", "flare": "Elemental fire surges through the strike."},
    "silver": {"cc": "Silver Veil", "dice": "1d4", "dmg": "[psychic]", "flare": f"{char_name} fades into the background noise."},
    "iron": {"cc": "Iron Howl", "dice": "1d8", "dmg": "[slashing]", "flare": "A primal ferocity heightens the strike."},
    "star": {"cc": "Starweave", "dice": "1d6", "dmg": "[force]", "flare": "The strike resonates with planar energy."},
    "earth": {"cc": "Earthheart", "dice": "1d4", "dmg": "[force]", "flare": "The ground yields to your immovable will."}
}

if mark_type not in marks:
    return f'echo Unknown mark: {mark_type}. Use ember, silver, iron, star, or earth.'

req_data = marks[mark_type]
req_cc = req_data["cc"]
dice = req_data["dice"]
dmg_type = req_data["dmg"]
flare_text = req_data["flare"]

# 3. ENFORCE THE "ONE MARK" RULE
all_cc_names = [m["cc"] for m in marks.values()]
existing_marks = [name for name in all_cc_names if ch.cc_exists(name)]

# If they have a different mark and DID NOT provide the -switch flag
if existing_marks and req_cc not in existing_marks and not switch_requested:
    old_mark = existing_marks[0]
    return f'embed -title "Attunement Conflict!" -desc "You are already attuned to the **{old_mark}**.\n\nDo you want to change your mark to **{req_cc}**?\nIf yes, run your command again and add `-switch`:\n\n`!powermark {mark_type} -switch`" -color ff0000'

init_msg = ""
# If they are switching, automatically clean up the old marks so their sheet stays neat!
if switch_requested and existing_marks and req_cc not in existing_marks:
    for old in existing_marks:
        ch.delete_cc(old)
    init_msg += f'-f "System|Unequipped previous Marks."'

# 4. The Self-Healing / Creation Logic
if not ch.cc_exists(req_cc):
    ch.create_cc(req_cc, 0, 4, "long", "bubble", None, None, 4)
    init_msg += f' -f "Setup|Created new {req_cc} counter (4/4) on your sheet!"'

# 5. Handle custom dice override
if len(args) > 1 and "d" in args[1]:
    dice = args[1]

# 6. Execute Logic
if ch.get_cc(req_cc) > 0:
    ch.mod_cc(req_cc, -1)
    my_roll = vroll(dice)
    res_field = f'-f "Effect|{my_roll.full} {dmg_type}"'
    chg_field = f'-f "Charges Remaining|{ch.get_cc(req_cc)}"'
else:
    flare_text = f"The {req_cc} flickers and fails! Out of charges."
    res_field = '-f "Effect|None"'
    chg_field = '-f "Status|Wait for a Long Rest!"'

# 7. Final Return
return f'embed -title "{char_name} activates {req_cc}!" -desc "{flare_text}" {res_field} {chg_field} {init_msg}'
</drac2>