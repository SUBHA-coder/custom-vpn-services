from flask import Flask, request, jsonify, render_template_string
import socket
import ssl
from cryptography.fernet import Fernet

app = Flask(__name__)

# Load the server's key
with open('server_key.key', 'rb') as key_file:
    key = key_file.read()

cipher = Fernet(key)

def send_message_to_server(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    secure_socket = context.wrap_socket(client_socket, server_hostname="your_cloud_vm_public_ip")
    secure_socket.connect(("your_cloud_vm_public_ip", 9999))

    encrypted_message = cipher.encrypt(message.encode())
    secure_socket.send(encrypted_message)

    response = secure_socket.recv(4096)
    decrypted_response = cipher.decrypt(response).decode()
    secure_socket.close()
    return decrypted_response

@app.route('/')
def index():
    return render_template_string("""
        <!doctype html>
        <title>Custom VPN</title>
        <h1>Send a Message to the VPN Server</h1>
        <form action="/send" method="post">
            <label for="message">Message:</label>
            <input type="text" id="message" name="message">
            <input type="submit" value="Send">
        </form>
    """)

@app.route('/send', methods=['POST'])
def send():
    message = request.form['message']
    response = send_message_to_server(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
