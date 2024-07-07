import socket
import ssl
from cryptography.fernet import Fernet

# Load the server's key
with open('server_key.key', 'rb') as key_file:
    key = key_file.read()

cipher = Fernet(key)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 9999))

message = b"Hello, Server!"
encrypted_message = cipher.encrypt(message)
client_socket.send(encrypted_message)

response = client_socket.recv(4096)
decrypted_response = cipher.decrypt(response)
print(f"Received: {decrypted_response}")

client_socket.close()
