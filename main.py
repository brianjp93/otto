import asyncio
from twitch import TwitchClient
from huecontroller import Lights
import select


li = Lights(transitiontime=.2)

async def handle_message(message, tc):
    print(message)
    [*p1, m] = message.split('#import_antigrvty :')
    n = m.split()[1] if len(m.split()) > 1 else ''
    try:
        n = int(n)
    except:
        n = -1

    if message.startswith('PING'):
        print('found ping message')
        tc.writer.write('PONG'.encode('utf-8'))
    elif m.startswith('!commands'):
        m = [
            'Light commands: ',
            '!hue <n>, !bri <n>, !sat <n>, !on, !off'
        ]
        m = ' '.join(m)
        tc.send(m)
    elif m.startswith('!off'):
        li.all_off()
        tc.send('Turning off the lights.')
    elif m.startswith('!on'):
        li.all_on()
        tc.send('Turning on the lights.')
    elif m.startswith('!hue'):
        li.set_hue(n)
        if 0 <= n <= 100:
            tc.send(f'Setting hue to {n}.')
        else:
            tc.send(f'Argument must be between 0 and 100.')
    elif m.startswith('!bri'):
        li.set_brightness(n)
        if 0 <= n <= 100:
            tc.send(f'Setting brightness to {n}.')
        else:
            tc.send(f'Argument must be between 0 and 100.')
    elif m.startswith('!sat'):
        li.set_saturation(n)
        if 0 <= n <= 100:
            tc.send(f'Setting saturation to {n}.')
        else:
            tc.send(f'Argument must be between 0 and 100.')


async def main(tc):
    await tc.connect()
    while True:
        if hasattr(tc, 'reader'):
            r = await tc.read()
            await handle_message(r, tc)
        else:
            await asyncio.sleep(1)

if __name__ == '__main__':
    tc = TwitchClient()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(tc))
