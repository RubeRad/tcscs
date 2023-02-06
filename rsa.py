import random


# a^k mod n, more efficiently for HUGE numbers
def powmod(a,k,n):
    if k==1:       # base case: if exponent is 1
        return a%n # a is the answer (mod n)

    half_k = k // 2

    # recursive step, compute a^(k/2) mod n
    half_answer = powmod(a, half_k, n)

    # now build the answer back up
    answer = (half_answer * half_answer) % n
    # if exponent is even, thats the answer!

    if k%2==1:                    # but if odd
        answer = (answer * a) % n # just need one more a

    return answer


# use Fermat's little theorem to (probably) test
# whether n is prime
def probably_prime(n):
    if n<2:          # stupid cases first
        return False
    if n==2:
        return True
    for i in range(100):
        a = random.randint(2,n-1)   # if we find any witness
        fermat = powmod(a, n-1, n)  # such that a^(n-1) mod n
        if fermat != 1:             # is not 1
            return False            # n is NOT prime

    # if we make it through all the tests without failing
    # then n is prime with very high probability
    return True



# generate a random prime
# for instance if lo=100, then range will be 100-1000
# i.e. 3 digits just like lo
def random_prime(lo):
    while True:
        candidate = random.randint(lo, 10*lo)
        if probably_prime(candidate):
            return candidate


if __name__ == '__main__':
    for i in range(2,110):
        if probably_prime(i):
            print(i)


    # Factors of RSA-100 challenge
    p = 37975227936943673922808872755445627854565536638199
    q = 40094690950920881030683735292761468389214899724061
    n = p*q
    print('prime:', probably_prime(p))
    print('prime:', probably_prime(q))
    print('not prime', probably_prime(n))

        
    lo = 1
    for i in range(100):
        lo = lo*10
        print(random_prime(lo))
