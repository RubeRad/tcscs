import re

def printrule(ost, oab, nab, nst, dir):
    osy = '#' if oab=='a' else '1'
    nsy = '#' if nab=='a' else '1'
    if nst=='h':
        print(f'     [ {ost}, "{osy}", "1", "h", "R" ],')
        # this prints a comma after the last rule that
        # has to be manually edited out :-(
    elif nst is None:
        pass # no rule -- error to get into this state
    else:
        print(f'     [ {ost}, "{osy}", "{nsy}", {nst}, "{dir}" ],')



print('{')
print('   "name": "Busy Beaver 3",')
print('   "description": "",')
print('   "max_state": 26,')
print('   "symbols": "1",')
print('   "tape": "",')
print('   "position": 0,')
print('   "rules": [')


# goldbach27.txt is https://gist.githubusercontent.com/anonymous/
# a64213f391339236c2fe31f8749a0df6/raw/5dd953cf549ec98e7f9ac046f7af01ac3523e292/list27.txt
# ruleset for a 27-state / 2-symbol turing machine that tests even numbers for
# being the sum of 2 primes, and halts if it ever finds one that isn't
# (i.e. a counterexample for the Goldbach conjecture)
# Example line 000(023Rb|001Rb) has two rules:
# State 0: if a, go to state 23 and move R after writing b
#          if b, go to state  1 and move R after writing b, etc
with open('goldbach27.txt', 'r') as lines:
    for line in lines:
        mch = re.search(r'(\d\d\d)\((\d\d\d)([RL])([ab])\|(\d\d\d)([RL])([ab])', line)
        if mch:
            oldstate = int(mch.group(1))   # 0-26

            newstate0 = int(mch.group(2))  # 0-26
            newdir0   = mch.group(3)       # R/L
            newsym0   = mch.group(4)       # a/b ~ 0/1

            newstate1 = int(mch.group(5))
            newdir1   = mch.group(6)
            newsym1   = mch.group(7)
        elif re.search(r'ERR', line): # 016(017Lb|ERR--)
            oldstate = 16
            newstate0 = 17
            newdir0   = 'L'
            newsym0   = 'b'
            newstate = None
        elif re.search(r'HALT', line): # 016(017Lb|ERR--)
            oldstate = 25
            newstate0 = 'h'
            newstate1 = 24
            newdir1   = 'R'
            newsym1   = 'b'

        printrule(oldstate,'a', newsym0, newstate0, newdir0)
        printrule(oldstate,'b', newsym1, newstate1, newdir1)


print('  ]')
print('}')
