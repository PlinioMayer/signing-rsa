import argparse
from random import randrange, getrandbits

def generate_keys():
    print('Generating keys:')
    p = generate_prime_number()
    q = generate_prime_number()

    n = p * q
    e = 65537
    



def config_argparse():
    parser = argparse.ArgumentParser(description='Generates key and signs messages using RSA.')
    parser.add_argument('-k', action = 'store_true', help = 'Generates private key (private.key) and public key (public.key) in keys folder')
    return parser

def main():
    parser = config_argparse()
    arguments = parser.parse_args()

    if (arguments.k):
        generate_keys()

    print('Done! Press Enter to close.')
    input()


if __name__ == '__main__':
    main()


def is_prime(n, k=128):

    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True

def generate_prime_candidate(length):

    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length=1024):
    
    p = 4
    # keep generating while the primality test fail
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p