from phue import Bridge

b = Bridge('10.0.0.156')
b.connect()
# r = b.get_api()
# print(r)
print(b)
print(dir(b))
print(b.lights)

b.lights[0].on = True
