<drac2>
ch = character()
cc = "Emberbrand"

# 1. Self-Healing: Auto-create counter if missing
if not ch.cc_exists(cc):
    ch.create_cc(cc, 0, 4, "long", "bubble")
    ch.set_cc(cc, 4)  # <--- This ensures it's full the moment it's born

# 2. Guard Clause: Check for charges
if ch.get_cc(cc) < 1:
    return f'-f "{cc} Error|Out of elemental fuel! Reset on a Long Rest."'

# 3. Execution: Spend charge and roll damage
ch.mod_cc(cc, -1)
rem = ch.get_cc(cc)

return f'-d "1d6[fire]" -f "{cc} Flare|Elemental fire surges from the mark! Charges left: {rem}"'
</drac2>