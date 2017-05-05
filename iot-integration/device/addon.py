from led import LED

class Addon(object):

    def __init__(self):
        self.led = LED(17)
        # self.blue_led = LED(27)

    def get_thermal(self):
        with open("/sys/bus/w1/devices/28-000006cc5c58/w1_slave") as fp:
            text = fp.read()
        secondline=text.split("\n")[1]
        tempdata=secondline.split(" ")[9]
        temp=float(tempdata[2:])
        temp=temp/1000
        return temp

