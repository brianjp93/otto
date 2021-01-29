import asyncio
import os
import socket
import time
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
NICKNAME = os.getenv('NICKNAME')
CHANNEL = os.getenv('CHANNEL')
TOKEN = os.getenv('TOKEN')


class TwitchClient():
    def __init__(self):
        self.socket = self.connect()

    def connect(self):
        sock = socket.socket()
        sock.connect((HOST, PORT))
        sock.send(f"PASS {TOKEN}\n".encode('utf-8'))
        sock.send(f"NICK {NICKNAME}\n".encode('utf-8'))
        sock.send(f"JOIN {CHANNEL}\n".encode('utf-8'))
        return sock

if __name__ == '__main__':
    tc = TwitchClient()
    while True:
        resp = tc.socket.recv(2048).decode('utf-8')
        print(resp)
