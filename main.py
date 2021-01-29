import asyncio
from twitch import TwitchClient
from huecontroller import Lights


class TwitchBot:
    def __init__(self, tc: TwitchClient, li: Lights):
        self.tc = tc
        self.li = li
        self.cmd = {
            '!commands': self.handle_commands,
            '!bri': self.handle_bri,
            '!hue': self.handle_hue,
            '!sat': self.handle_sat,
            '!off': self.handle_off,
            '!on': self.handle_on,
            '!current': self.handle_current,
        }

    def handle_commands(self, *args):
        m = [
            'Light commands: ',
            '!hue <n>, !bri <n>, !sat <n>, !on, !off'
        ]
        m = ' '.join(m)
        self.tc.send(m)

    def handle_current(self, *args):
        bri, hue, sat = self.li.get_current()
        bri = round((bri / self.li.MAX_BRI) * 100)
        hue = round((hue / self.li.MAX_HUE) * 100)
        sat = round((sat / self.li.MAX_SAT) * 100)
        m = f'Brightness: {bri}, Hue: {hue}, Saturation: {sat}'
        self.tc.send(m)

    def handle_on(self, *args):
        self.li.all_on()
        self.tc.send('Turning on lights.')

    def handle_off(self, *args):
        self.li.all_off()
        self.tc.send('Turning off lights.')

    def handle_hue(self, n):
        self.li.set_hue(n)
        if 0 <= n <= 100:
            self.tc.send(f'Setting hue to {n}.')
        else:
            self.tc.send('Argument must be between 0 and 100.')

    def handle_bri(self, n):
        self.li.set_brightness(n)
        if 0 <= n <= 100:
            self.tc.send(f'Setting brightness to {n}.')
        else:
            self.tc.send('Argument must be between 0 and 100.')

    def handle_sat(self, n):
        self.li.set_saturation(n)
        if 0 <= n <= 100:
            self.tc.send(f'Setting saturation to {n}.')
        else:
            self.tc.send('Argument must be between 0 and 100.')

    async def handle_message(self):
        message = await self.tc.read()
        if not message:
            return
        print(message)
        [*p1, m] = message.split('#import_antigrvty :')
        cmd = m.split()[0] if m else ''
        n = m.split()[1] if len(m.split()) > 1 else ''
        try:
            n = int(float(n))
        except:
            n = -1

        if message.startswith('PING'):
            print('found ping message')
            self.tc.writer.write('PONG'.encode('utf-8'))
        else:
            fn = self.cmd.get(cmd)
            fn(n) if fn else None


async def main():
    li = Lights(transitiontime=.2)
    tc = TwitchClient()
    await tc.connect()
    tb = TwitchBot(tc, li)
    while True:
        if hasattr(tb.tc, 'reader'):
            await tb.handle_message()
        else:
            await asyncio.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
