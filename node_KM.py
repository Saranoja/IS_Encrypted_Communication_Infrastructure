import os
import socket
import commons
from AES_pack import *

K = os.urandom(16)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((commons.HOST, commons.A_KM_PORT))
    s.listen()
    conn, _ = s.accept()
    with conn:
        data = conn.recv(1024)
        print(f'Requested mode of operation: {data.decode("utf-8")}')
        conn.sendall(bytes(AES_encrypt(K, commons.K_prime)))
