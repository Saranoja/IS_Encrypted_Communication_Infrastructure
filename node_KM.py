import os
import socket
import commons

K = os.urandom(16)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((commons.HOST, commons.A_KM_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        # while True:
        data = conn.recv(1024)
        print(f'Port {commons.A_KM_PORT}: {data.decode("utf-8")}')
        conn.sendall(bytes(commons.AES_encrypt(K, commons.K_prime)))
        s.close()
