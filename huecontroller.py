from phue import Bridge
IP = '10.0.0.156'


class Lights:
    def __init__(self, transitiontime=None):
        self.bridge = self.init_bridge()
        self.transitiontime = transitiontime

    def init_bridge(self):
        bridge = Bridge(IP)
        bridge.connect()
        return bridge

    def all_on(self):
        for light in self.bridge.lights:
            light.transitiontime = self.transitiontime
            light.on = True
            light.brightness = 255

    def all_off(self):
        for light in self.bridge.lights:
            light.transitiontime = self.transitiontime
            light.brightness = 0

    def set_hue(self, n):
        try:
            n = int(float(n))
            n = int(n * 655.35)
        except Exception as e:
            print(e)
            print(f'Invalid Number {n}')
        else:
            for light in self.bridge.lights:
                light.transitiontime = self.transitiontime
                light.hue = n

    def set_saturation(self, n):
        try:
            n = int(float(n))
            n = int(n * 2.55)
        except:
            print(f'Invalid Number {n}')
        else:
            for light in self.bridge.lights:
                light.transitiontime = self.transitiontime
                light.saturation = n

    def set_brightness(self, n):
        try:
            n = int(float(n))
            n = int(n * 2.55)
        except:
            print(f'Invalid Number {n}')
        else:
            for light in self.bridge.lights:
                light.transitiontime = self.transitiontime
                light.brightness = n


if __name__ == '__main__':
    l = Lights(transitiontime=.5)
    for light in l.bridge.lights:
        light.saturation = 100
