<drac2>
ch = character()
args = "&*&".split()

# 1. Long Rest Logic
# This triggers the standard Avrae long rest (HP/Hit Dice/Spell Slots)
ch.long_rest()

# 2. Custom Counter Resets
# We loop through your 'Foundry' counters to ensure they match the repo registry
counters = {
    "Emberbrand": 4,
    "Silver Veil": 4,
    "Dragon Ammo": 10,
    "Fuel Tank": 3,
    "Planar Battery": 5
}

reset_log = []
for name, val in counters.items():
    if ch.cc_exists(name):
        ch.set_cc(name, val)
        reset_log.append(f"{name} restored to {val}")

# 3. Mournland Flavor
title = "Long Rest: Mournland Camp Zone"
desc = "The grey mists press against the edge of the camp, muffled and heavy. Natural healing is sluggish here, but the Foundry remains operational."

# Check for a "Secure" flag if you have a Tiny Hut or Guard
is_secure = "-secure" in args
if not is_secure:
    desc += "\n\n**[WARNING]** The camp is unsecured. The mists may haunt your recovery."

fields = f'-f "Logistics|{chr(10).join(reset_log)}"'

return f'embed -title "{title}" -desc "{desc}" {fields} -color <color>'
</drac2>