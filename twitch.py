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
    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(host=HOST, port=PORT)
        self.writer.write(f"PASS {TOKEN}\n".encode('utf-8'))
        self.writer.write(f"NICK {NICKNAME}\n".encode('utf-8'))
        self.writer.write(f"JOIN #{CHANNEL}\n".encode('utf-8'))

    async def read(self, buffer=2048):
        r = await self.reader.read(buffer)
        r = r.strip().decode('utf-8')
        return r

    def send(self, message):
        message = f'PRIVMSG #{CHANNEL} :{message}\n'.encode('utf-8')
        self.writer.write(message)


async def main():
    tc = TwitchClient()
    await tc.connect()
    while True:
        if hasattr(tc, 'reader'):
            r = await tc.read()
            print(r)
        else:
            await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
