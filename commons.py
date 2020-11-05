from Cryptodome.Cipher import AES

HOST = '127.0.0.1'
A_B_PORT = 62222
A_KM_PORT = 63333
CBC = 'CBC'
OFB = 'OFB'

K_prime = b'\xf9\xef\x06;\xed\xe0\xa8w6t&\x17\xf1\xe9\xf8\x94'  # K1 and K2 encryption

initialization_vector = b'/\xc9\x84B\x99j\xdd\xa9\x1e\t\xed\xd5A\x00g\x12'

# test_message = os.urandom(64)  # 512 bits - 4 blocks
test_message = open("file.txt", "r").read().encode('UTF-8')


def get_xor_result(block, iv, key):
    block_xor_iv = bytes(a ^ b for (a, b) in zip(block, iv))
    block_xor_iv_xor_key = bytes(a ^ b for (a, b) in zip(block_xor_iv, key))
    return block_xor_iv_xor_key


def CBC_encrypt(plaintext, iv, key):
    ciphertext = b''
    while plaintext:
        block = plaintext[0:16]
        plaintext = plaintext[16:]
        enc_block = get_xor_result(block, iv, key)
        ciphertext += enc_block
        iv = enc_block
    return ciphertext


def CBC_decrypt(ciphertext, iv, key):
    plaintext = b''
    while ciphertext:
        block = ciphertext[0:16]
        ciphertext = ciphertext[16:]
        dec_block = get_xor_result(block, key, iv)
        plaintext += dec_block
        iv = block
    return plaintext


def OFB_encrypt(plaintext, iv, key):
    ciphertext = b''
    while plaintext:
        block = plaintext[0:16]
        plaintext = plaintext[16:]
        enc_block = get_xor_result(iv, key, block)
        ciphertext += enc_block
        iv = bytes(a ^ b for (a, b) in zip(key, iv))
    return ciphertext


def OFB_decrypt(ciphertext, iv, key):
    plaintext = b''
    while ciphertext:
        block = ciphertext[0:16]
        ciphertext = ciphertext[16:]
        dec_block = get_xor_result(iv, key, block)
        plaintext += dec_block
        iv = bytes(a ^ b for (a, b) in zip(key, iv))
    return plaintext


def AES_encrypt(message, key):
    aes = AES.new(key, AES.MODE_ECB)
    encd = aes.encrypt(message)
    return encd


def AES_decrypt(ciphertext, key):
    aes = AES.new(key, AES.MODE_ECB)
    dec = aes.decrypt(ciphertext)
    return dec
