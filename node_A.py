import socket
import commons

OPERATING_MODE = commons.OFB


def build_network(B_port, KM_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as kms:
            kms.connect((commons.HOST, KM_port))
            kms.sendall(bytes(OPERATING_MODE, "utf-8"))

            encrypted_key = kms.recv(128)
            print(f'Key received from node_KM: {encrypted_key}')
            key = commons.AES_decrypt(encrypted_key, commons.K_prime)
            print(f'Decrypted key: {key}')
            kms.close()

            s.connect((commons.HOST, B_port))
            s.sendall(bytes(OPERATING_MODE, "utf-8"))
            s.sendall(encrypted_key)

            data = s.recv(1024)
            print(f'Message from B: {data.decode("utf-8")}')
            file_size = len(commons.test_message)
            s.sendall(bytes(str(file_size), 'utf8'))
            if OPERATING_MODE == commons.CBC:
                encrypted_message = commons.CBC_encrypt(commons.test_message, commons.initialization_vector, key)
            else:
                encrypted_message = commons.OFB_encrypt(commons.test_message, commons.initialization_vector, key)
            print(f'Sending encrypted message to B: {encrypted_message}')
            s.sendall(encrypted_message)


if __name__ == "__main__":
    build_network(commons.A_B_PORT, commons.A_KM_PORT)
