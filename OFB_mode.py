from commons import *


class OFB_mode:
    def __init__(self, iv, k):
        self.initialization_vector = iv
        self.key = k

    def encrypt(self, plaintext):
        ciphertext = b''
        iv = self.initialization_vector
        while plaintext:
            block = plaintext[0:16]
            block = block + b'\0' * (16 - len(block))
            plaintext = plaintext[16:]
            enc_block = get_xor_result(iv, self.key, block)
            ciphertext += enc_block
            iv = bytes(a ^ b for (a, b) in zip(self.key, iv))
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b''
        iv = self.initialization_vector
        while ciphertext:
            block = ciphertext[0:16]
            ciphertext = ciphertext[16:]
            dec_block = get_xor_result(iv, self.key, block)
            plaintext += dec_block
            iv = bytes(a ^ b for (a, b) in zip(self.key, iv))
        return plaintext
