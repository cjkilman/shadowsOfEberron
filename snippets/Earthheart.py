<drac2>
ch = character()
cc = "Earthheart"
dmg = "1d4[force]"
flavor = "The ground yields to your immovable will."

# 1. Dependency Check: The Mark MUST be equipped via !powermark
if not ch.cc_exists(cc):
    return f'-f "System Error|You are not attuned to {cc}. Run your attunement command first!" '

# 2. Guard Clause: Check for charges
if ch.get_cc(cc) < 1:
    return f'-f "{cc} Error|Out of power! Reset on a Long Rest." '

# 3. Execution: Spend charge and output mechanics
ch.mod_cc(cc, -1)
rem = ch.get_cc(cc)

return f'-d "{dmg}" -f "{cc} Activated|{flavor}\n*Charges remaining: {rem}/4*" '
</drac2>