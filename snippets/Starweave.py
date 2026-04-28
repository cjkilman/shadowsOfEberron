<drac2>
ch, cc = character(), "Starweave"
if not ch.cc_exists(cc):
    ch.create_cc(cc, 0, 4, "long", "bubble", None, None, 4)
    ch.set_cc(cc, 4)
if ch.get_cc(cc) < 1:
    return f'-f "{cc}|Depleted! Reset on a Long Rest."'
ch.mod_cc(cc, -1)
return f'-d "1d6[force]" -f "{cc}|The strike resonates with planar energy! ({ch.get_cc(cc)} left)"'
</drac2>