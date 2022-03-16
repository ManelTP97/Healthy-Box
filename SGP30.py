import board
import busio
import adafruit_sgp30

class SGP30:
    def __init__(self):
        self.i2c = busio.I2C(board.SCK, board.SDA, frequency = 100000)
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(self.i2c)

    def geteCO2(self):
        self.sgp30.geteCO2

    def getTVOC(self):
        self.sgp30.TVOC
