import RPi.GPIO as GPIO


class HallSensor:

    def __init__(self):
        self.closer = 0
        self.GPIO_Pin = 17
        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(self.GPIO_Pin, GPIO.In)
        self.GPIO.add_event_detect(self.GPIO_Pin, GPIO.Rising)

    def Door_closed(self):

        if not GPIO.add_event_detect(self.GPIO_Pin):
            self.closer = 1



