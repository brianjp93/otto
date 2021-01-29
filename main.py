from twitch import TwitchClient
from huecontroller import Lights
import select

tc = TwitchClient()
li = Lights(transitiontime=.2)

def handle_message(message):
    print(message)
    [*p1, m] = message.split('#import_antigrvty :')
    n = m.split()[1] if len(m.split()) > 1 else ''

    if m.startswith('!off'):
        li.all_off()
    elif m.startswith('!on'):
        li.all_on()
    elif m.startswith('!hue'):
        li.set_hue(n)
    elif m.startswith('!bri'):
        li.set_brightness(n)
    elif m.startswith('!sat'):
        li.set_saturation(n)


def main():
    tc.socket.setblocking(0)
    while True:
        ready = select.select([tc.socket], [], [], 5)
        if ready[0]:
            r = tc.socket.recv(2048).decode('utf-8')
            handle_message(r)

if __name__ == '__main__':
    main()
