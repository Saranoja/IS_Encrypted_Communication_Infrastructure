from Cryptodome.Cipher import AES

HOST = '127.0.0.1'
A_B_PORT = 62222
A_KM_PORT = 63333
CBC = 'CBC'
OFB = 'OFB'

K_prime = b'\xf9\xef\x06;\xed\xe0\xa8w6t&\x17\xf1\xe9\xf8\x94'  # used for K encryption
initialization_vector = b'/\xc9\x84B\x99j\xdd\xa9\x1e\t\xed\xd5A\x00g\x12'


def get_xor_result(block, iv, key):
    block_xor_iv = bytes(a ^ b for (a, b) in zip(block, iv))
    block_xor_iv_xor_key = bytes(a ^ b for (a, b) in zip(block_xor_iv, key))
    return block_xor_iv_xor_key


def AES_encrypt(message, key):
    aes = AES.new(key, AES.MODE_ECB)
    enc = aes.encrypt(message)
    return enc


def AES_decrypt(ciphertext, key):
    aes = AES.new(key, AES.MODE_ECB)
    dec = aes.decrypt(ciphertext)
    return dec
