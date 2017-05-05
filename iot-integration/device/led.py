import RPi.GPIO as GPIO

class LED(object):

    def __init__(self, pin):
        self.pin = pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.led = GPIO.PWM(pin, 500)
        self.led.start(0)
        self.power = 0
    def get(self):
        return self.power

    def set(self, power):
        self.power = power
        self.led.ChangeDutyCycle(float(power))
