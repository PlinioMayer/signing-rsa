import argparse
from random import randrange, getrandbits, choice
from string import ascii_letters
from hashlib import sha3_512, sha3_256
import base64
import pathlib
import os

def config_argparse():
    parser = argparse.ArgumentParser(description='Generates key and signs messages using RSA.')
    parser.add_argument('-g', action = 'store_true', help = 'Generates private key (private.key) and public key (public.key) in keys folder')
    parser.add_argument('-m', nargs = 1, metavar = 'message', dest = 'message')
    parser.add_argument('-s', nargs = 1, metavar = 'signature', dest = 'signature')
    parser.add_argument('-k', nargs = 1, metavar = 'key', dest = 'key')
    return parser

def main():
    parser = config_argparse()
    arguments = parser.parse_args()

    if arguments.g:
        if (arguments.message or arguments.key or arguments.signature):
            raise 'You can\'t pass other arguments when using -g'
        generate_keys()
    elif arguments.message:
        if (not arguments.key):
            raise 'You must specify a key to sign your message'

        message = None

        with open(arguments.message[0], 'rb') as file:
            message = base64.b64encode(file.read())

        key = None

        with open(arguments.key[0], 'r', encoding = 'utf-8') as file:
            first_line = file.readline().replace('\r', '\n').replace('\n', '').split('=')
            second_line = file.readline().replace('\r', '\n').replace('\n', '').split('=')

            if not arguments.signature and second_line[0] != 'd':
                raise 'You must use a private key to sign the message'
            elif arguments.signature and second_line[0] != 'e':
                raise 'You must use a public key to verify the message'
            
            key = (first_line[1], second_line[1])

        if arguments.signature:
            signature = None

            with open(arguments.signature[0], 'r', encoding = 'utf-8') as file:
                signature = file.read()

            verify_signature(message, key, signature)
        else:
            sign_message(message, key)
    else:
        oaep_encode(sha3_256(b'').digest())
        print('Nothing to do.')

    print('Done! Press Enter to close.')
    input()

def verify_signature(message, key, signature):
    hash = int.from_bytes(sha3_256(message).digest(), byteorder = 'big')
    hashFromSignature = pow(int(signature), int(key[1]), int(key[0]))

    print(hash)
    print(int.from_bytes(oaep_decode(hashFromSignature), byteorder = 'big'))
    if hash == int.from_bytes(oaep_decode(hashFromSignature), byteorder = 'big'):
        print('Valid signature.')
    else:
        print('invalid signature.')

def sign_message(message, key):
    hash = int.from_bytes(oaep_encode(sha3_256(message).digest()), byteorder = 'big')
    signature = pow(hash, int(key[1]), int(key[0]))

    signature_path = pathlib.Path('signature.txt').absolute()
    print(f"Writing signature to {signature_path}")

    with open(signature_path, 'w', encoding = 'utf-8') as file:
        file.write(f"{signature}")

def generate_keys():
    print ('generating p and q...')
    p = generate_prime_number()
    q = generate_prime_number()
    n = p * q
        
    print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        e = randrange(2 ** 1, 2 ** 16)
        if gcd(e, (p - 1) * (q - 1)) == 1:
            break
    
    print('Calculating d that is mod inverse of e...')
    d = findModInverse(e, (p - 1) * (q - 1))

    folder_path = pathlib.Path('keys').absolute()
   
    if (not os.path.exists(folder_path)):
        os.makedirs(folder_path)

    print(f"Saving keys in {folder_path}...")
    with open(pathlib.Path("keys/public.key").absolute(), 'w', encoding = 'utf-8') as file:
        file.write(f"n={n}\ne={e}")

    with open(pathlib.Path(f"keys/private.key").absolute(), 'w', encoding = 'utf-8') as file:
        file.write(f"n={n}\nd={d}")

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

def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def findModInverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def xor(a, b):
    assert len(a) == len(b)
    return bytearray([ aa ^ bb for aa, bb in zip(a, b)])

def oaep_encode(message):
    mm = message + (b'\x00' * 32)
    r = ''.join(choice(ascii_letters) for i in range(64)).encode('ascii')
    G = sha3_512(r).digest()
    X = xor(mm, G)
    H = sha3_512(X).digest()
    Y = xor(r, H)

    return X + Y

def oaep_decode(signature):
    XY = int(signature).to_bytes(128, 'big')
    r = xor(XY[64:], sha3_512(XY[:64]).digest())
    mm = xor(XY[:64], sha3_512(r).digest())
    return mm[0:32]

if __name__ == '__main__':
   main()