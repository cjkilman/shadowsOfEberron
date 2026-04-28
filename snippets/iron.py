<drac2>
ch, cc = character(), "Iron Howl"
if not ch.cc_exists(cc):
    ch.create_cc(cc, 0, 4, "long", "bubble", None, None, 4)
    ch.set_cc(cc, 4) # Forces it to full on creation
if ch.get_cc(cc) < 1:
    return f'-f "{cc}|Depleted! Reset on a Long Rest."'
ch.mod_cc(cc, -1)
return f'-d "1d8[slashing]" -f "{cc}|A primal ferocity heightens the strike! ({ch.get_cc(cc)} left)"'
</drac2>