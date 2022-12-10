noahcode = """M3G1R86<@0RP@#0H-"E%B8G-R869U>G9E9VT@<'EN=GIF(&=B('5N:7(@='9I
M<F$@:&,@<FEV>2X@57(@<FER82!F=G1A<G$@9W5V9B#B@)Q6(%1V:7(@2&,@
M4FEV>>`G2!N<W-V<6YI=F<@9V(@;F-C>6P@<V)E(&IB97@@;F<@9W5R(&YT
M<F%P;"X@#0I<NF65R('IN>'9A="!18F)S<F%F=7IV96=M(&QB:&4@97)F
M8V)A9G9O=GEV9VP@<6AE=F%T('5V9B!C96)O;F=V8F$@8W)E=F)Q+B-"D9U
M8FH@=79Z(&=U<B!E8F-R9BP@;F%Q('%B8>F6<@>7)G('5V>B!B:&<@8G,@
<;&)H92!F=G1U9RX-"@T*6F)A8G1E;GH@8FAG(0``"""

counts = {}
for letter in noahcode:
    if letter in counts:
        counts[letter] = counts[letter]+1
    else:
        counts[letter] = 1

for letter in counts.keys():
    print(counts[letter], letter)
