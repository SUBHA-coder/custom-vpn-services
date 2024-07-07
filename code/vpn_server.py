import socket
import ssl
from cryptography.fernet import Fernet

# Generate and save a key for encryption
key = Fernet.generate_key()
with open('server_key.key', 'wb') as key_file:
    key_file.write(key)

cipher = Fernet(key)

def handle_client(client_socket):
    request = client_socket.recv(4096)
    decrypted_request = cipher.decrypt(request)
    print(f"Received: {decrypted_request}")

    response = b"ACK"
    encrypted_response = cipher.encrypt(response)
    client_socket.send(encrypted_response)
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 9999))
server_socket.listen(5)
print("Listening on port 9999")

while True:
    client, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    handle_client(client)
