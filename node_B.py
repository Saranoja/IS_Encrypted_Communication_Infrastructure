import socket
import commons
from CBC_mode import *
from OFB_mode import *
from AES_pack import *

key, encrypted_key = b'', b''


def get_mode_of_operation():
    mode = conn.recv(3)
    print(f'Mode of operation: {mode.decode("utf-8")}')
    return mode


def get_key_and_decrypt():
    global key, encrypted_key
    encrypted_key = conn.recv(16)
    print(f'Key from A: {encrypted_key}')
    key = AES_decrypt(encrypted_key, commons.K_prime)
    print(f'Decrypted key: {key}')


def send_start_signal():
    conn.sendall(bytes("Start", "utf-8"))


def get_message():
    file_size = conn.recv(4)
    return conn.recv(int(str(file_size, 'utf8')))


def decrypt_message_on_chosen_mode(mode, message):
    if mode == commons.CBC:
        cbc = CBC_mode(commons.initialization_vector, key)
        decrypted_data = cbc.decrypt(message)
    else:
        ofb = OFB_mode(commons.initialization_vector, key)
        decrypted_data = ofb.decrypt(message)
    return decrypted_data


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((commons.HOST, commons.A_B_PORT))
    s.listen()
    conn, _ = s.accept()
    with conn:
        mode_of_operation = get_mode_of_operation()

        get_key_and_decrypt()

        send_start_signal()

        decrypted_message = decrypt_message_on_chosen_mode(mode_of_operation.decode('utf-8'), get_message())

        print(f'Message from A: {decrypted_message.decode("utf-8")}')
