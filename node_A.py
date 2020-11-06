import socket
import commons
import random
from CBC_mode import *
from OFB_mode import *
from AES_pack import *

available_modes = [commons.OFB, commons.CBC]
MODE_OF_OPERATION = random.choice(available_modes)
key, encrypted_key = b'', b''


def send_mode_of_operation_to(sock):
    sock.sendall(bytes(MODE_OF_OPERATION, "utf-8"))
    sock.sendall(encrypted_key)


def get_key_and_decrypt(sock):
    global key, encrypted_key
    encrypted_key = sock.recv(16)
    print(f'Key received from node_KM: {encrypted_key}')
    key = AES_decrypt(encrypted_key, commons.K_prime)
    print(f'Decrypted key: {key}')


def get_start_signal(sock):
    data = sock.recv(5)
    print(f'Signal received from B: {data.decode("utf-8")}')


def retrieve_text_from_file(f):
    try:
        file_text = f.read()
        return file_text
    except PermissionError:
        print("No permission to read from the file")


def send_file_size_to(sock, text):
    file_size = len(text)
    sock.sendall(bytes(str(file_size), 'utf8'))


def encrypt_message_on_chosen_mode(message):
    if MODE_OF_OPERATION == commons.CBC:
        cbc = CBC_mode(commons.initialization_vector, key)
        encrypted_message = cbc.encrypt(message)
    else:
        ofb = OFB_mode(commons.initialization_vector, key)
        encrypted_message = ofb.encrypt(message)
    return encrypted_message


def send_encrypted_message(sock, message):
    print(f'Sending encrypted message: {message}')
    sock.sendall(message)


def connect_to_KM(KM_port):
    global key, encrypted_key
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as kms:
        kms.connect((commons.HOST, KM_port))

        send_mode_of_operation_to(kms)

        get_key_and_decrypt(kms)


def connect_to_B(B_port):
    global key, encrypted_key
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((commons.HOST, B_port))

        send_mode_of_operation_to(s)
        get_start_signal(s)

        try:

            with open("file.txt", "rb") as f:
                file_text = retrieve_text_from_file(f)
                send_file_size_to(s, file_text)
                encrypted_message = encrypt_message_on_chosen_mode(file_text)
                send_encrypted_message(s, encrypted_message)

        except FileNotFoundError:
            print("Did not find the requested file")


if __name__ == "__main__":
    connect_to_KM(commons.A_KM_PORT)
    connect_to_B(commons.A_B_PORT)
