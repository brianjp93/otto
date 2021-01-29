from phue import Bridge
IP = '10.0.0.156'


class Lights:
    MAX_SAT = MAX_BRI = 2**8 - 2
    MAX_HUE = 2**16 - 1

    def __init__(self, transitiontime=None):
        self.bridge = self.init_bridge()
        self.transitiontime = transitiontime

    def init_bridge(self):
        bridge = Bridge(IP)
        bridge.connect()
        return bridge

    def get_current(self):
        """Return brightness, hue, saturation.

        Returns
        -------
        tuple
            (brightness, hue, saturation)

        """
        l = self.bridge.lights[0]
        return l.brightness, l.hue, l.saturation

    def all_on(self):
        for light in self.bridge.lights:
            light.transitiontime = self.transitiontime
            light.on = True
            light.brightness = self.MAX_BRI

    def all_off(self):
        for light in self.bridge.lights:
            light.transitiontime = self.transitiontime
            light.brightness = 0

    def set_hue(self, n):
        try:
            n = int(float(n))
            n = int(round(n * self.MAX_HUE / 100, 0))
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
            n = int(round(n * self.MAX_SAT / 100, 0))
        except:
            print(f'Invalid Number {n}')
        else:
            for light in self.bridge.lights:
                light.transitiontime = self.transitiontime
                light.saturation = n

    def set_brightness(self, n):
        try:
            n = int(float(n))
            n = int(round(n * self.MAX_BRI / 100, 0))
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
