!servalias powermark <drac2>
ch = character()
input_args = """&*&"""
args = input_args.split()
if not args:
    return 'echo "You need to specify a mark! Usage: !powermark <ember/silver>"'
mark_type = args[0].lower()
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
    return f'echo "Unknown mark: {mark_type}"'
if not ch.cc_exists(cc_name) or ch.get_cc(cc_name) < 1:
    return f'echo "Error: {cc_name} Failed! Out of charges or missing."'
ch.mod_cc(cc_name, -1)
my_roll = vroll(dice)
return f'embed -title "{cc_name} Activates!" -desc "{flare_text}" -f "Effect|{my_roll.full} {dmg_type}" -f "Charges Remaining|{ch.get_cc(cc_name)}"'
</drac2>