import pyautogui, socket, threading
import time

import requests


downKeys = []

def get_ip_address():
    url = 'https://api.ipify.org'
    response = requests.get(url)
    ip_address = response.text
    return ip_address

def start_server() -> socket.socket:
    HOST, PORT = '0.0.0.0', 9000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))
    server.listen()

    return server

def keyboard(key:str) -> None:
    global downKeys
    if key in downKeys:
        downKeys.remove(key)
        pyautogui.keyUp(key)
    else:
        downKeys.append(key)
        pyautogui.keyDown(key)

def manage_connection(server: socket.socket) -> socket.socket:
    conn, address = server.accept()
    return conn

def control(controler: socket.socket) -> None:
    print('connected')
    command: str = ''
    prev_command: str = ''
    

    while controler:
        threading.Thread(target= keyboard, args= (controler.recv(1024).decode(),)).start()
        controler.send(b'1')

if __name__ == '__main__':
    print(get_ip_address())
    while True:
        try:
            control(manage_connection(start_server()))
        except:
            pass


