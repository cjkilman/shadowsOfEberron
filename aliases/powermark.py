<drac2>
ch = character()
# The &*& tells the website to grab whatever the player types after !powermark
args = "&*&".split()
char_name = ch.name

# 1. Basic Usage Check
if not args:
    return f'echo Usage: !powermark <ember/silver> [dice]'

mark_type = args[0].lower()

# 2. Define the Marks
if mark_type == "ember":
    cc_name = "Emberbrand"
    dice = "1d6"
    dmg_type = "[fire]"
    flare_text = "Elemental fire surges through the strike."
elif mark_type == "silver":
    cc_name = "Silver Veil"
    dice = "1d4"
    dmg_type = "[veil]"
    flare_text = "Gerolkae fades into the background noise."
else:
    return f'echo Unknown mark: {mark_type}. Use "ember" or "silver".'

# 3. The Self-Healing Counter Logic
# (name, min, max, reset, type, display, value, initial)
init_msg = ""
if not ch.cc_exists(cc_name):
    ch.create_cc(cc_name, 0, 4, "long", "bubble", None, None, 4)
    init_msg = f' -f "Setup|Created new {cc_name} counter (4/4) on your sheet!"'

# 4. Handle custom dice override
if len(args) > 1:
    dice = args[1]

# 5. Execute Logic
if ch.get_cc(cc_name) > 0:
    ch.mod_cc(cc_name, -1)
    my_roll = vroll(dice)
    res_field = f'-f "Effect|{my_roll.full} {dmg_type}"'
    chg_field = f'-f "Charges Remaining|{ch.get_cc(cc_name)}"'
else:
    flare_text = f"The {cc_name} flickers and fails! Out of charges."
    res_field = '-f "Effect|None"'
    chg_field = '-f "Status|Wait for a Long Rest!"'

# 6. Final Return
return f'embed -title "{char_name} activates {cc_name}!" -desc "{flare_text}" {res_field} {chg_field} {init_msg}'
</drac2>