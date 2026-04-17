ch = character()
cc = "Emberbrand"
if not ch.cc_exists(cc) or ch.get_cc(cc) < 1:
    return f'-f "Error|{cc} is out of charges or missing!"'
ch.mod_cc(cc, -1)
return f'-d "1d6[fire]" -f "{cc} Flare|Elemental fire surges! Charges left: {ch.get_cc(cc)}"'