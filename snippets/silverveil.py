ch = character()
cc = "Silver Veil"
if not ch.cc_exists(cc) or ch.get_cc(cc) < 1:
    return f'-f "Error|{cc} is out of charges or missing!"'
ch.mod_cc(cc, -1)
return f'-d "1d4[veil]" -f "{cc} Activation|The weave blurs your form. Charges left: {ch.get_cc(cc)}"'