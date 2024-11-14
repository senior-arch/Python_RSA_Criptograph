import random

class RSA:
    def __init__(self, bit_length=8):
        self.bit_length = bit_length
        self.public_key, self.private_key = self.generate_keys()

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def mod_inverse(self, a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    def is_prime(self, num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    def generate_prime_candidate(self):
        while True:
            candidate = random.getrandbits(self.bit_length)
            if self.is_prime(candidate):
                return candidate

    def generate_keys(self):
        p = self.generate_prime_candidate()
        q = self.generate_prime_candidate()
        n = p * q
        phi = (p - 1) * (q - 1)

        e = random.randrange(1, phi)
        while self.gcd(e, phi) != 1:
            e = random.randrange(1, phi)

        d = self.mod_inverse(e, phi)
        return ((e, n), (d, n))

    def encrypt(self, plaintext, pub_key):
        e, n = pub_key
        cipher_text = [pow(ord(char), e, n) for char in plaintext]
        return cipher_text

    def decrypt(self, cipher_text, priv_key):
        d, n = priv_key
        plaintext = ''.join([chr(pow(char, d, n)) for char in cipher_text])
        return plaintext