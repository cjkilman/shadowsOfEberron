<drac2>
ch = character()
cc = "Silver Veil"

# Self-healing: Create the counter if it doesn't exist
if not ch.cc_exists(cc):
    ch.create_cc(cc, 0, 4, "long", "bubble")
    ch.set_cc(cc, 4) # Ensures the first-ever use doesn't start at 3/4 or 0/4

# Charge check
if ch.get_cc(cc) < 1:
    return f'-f "{cc} Error|You are out of charges! Reset on a Long Rest."'

# Decrement and fetch remaining
ch.mod_cc(cc, -1)
rem = ch.get_cc(cc)

# Return the combat string
# Note: [veil] is a custom label; it won't be resisted unless defined as a standard type.
return f'-d "1d4[veil]" -f "{cc} Activation|The weave blurs your form. Charges left: {rem}"'
</drac2>