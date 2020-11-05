import socket
import commons

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((commons.HOST, commons.A_B_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        mode = conn.recv(3)
        print(f'Opperation mode: {mode.decode("utf-8")}')
        encrypted_key = conn.recv(16)
        print(f'Key from A: {encrypted_key}')
        key = commons.AES_decrypt(encrypted_key, commons.K_prime)
        print(f'Decrypted key: {key}')

        conn.sendall(bytes("Start", "utf-8"))
        file_size = conn.recv(4)
        if mode.decode("utf-8") == commons.CBC:
            decrypted_data = commons.CBC_decrypt(file_size, commons.initialization_vector, key)
            # print(f'Message from A: {file_size.decode("utf-8")}')
            data = conn.recv(int(str(file_size, 'utf8')))
            decrypted_data = commons.CBC_decrypt(data, commons.initialization_vector, key)
        else:
            decrypted_data = commons.OFB_decrypt(file_size, commons.initialization_vector, key)
            # print(f'Message from A: {file_size.decode("utf-8")}')
            data = conn.recv(int(str(file_size, 'utf8')))
            decrypted_data = commons.OFB_decrypt(data, commons.initialization_vector, key)
        print(f'Message from A: {decrypted_data.decode("utf-8")}')
