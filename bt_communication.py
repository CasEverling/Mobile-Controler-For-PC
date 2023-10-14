import socket
from typing import Any

def connect(host: str, port: int):
    controler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    controler.connect((host, port))
    return controler

def send_data(connection, data):
    connection.send(data.encode())
    connection.recv(1024)



