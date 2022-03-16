import board
import adafruit_bme680

class BME680:
    def __init__(self):
        self.i2c = board.I2C()
        self.sensor = adafruit_bme680.Adafruit_BME680_I2C(self.i2c)

    def getTemps(self):
        return self.sensor.temperature

    def getGas(self):
        return self.sensor.gas

    def getHumidity(self):
         return self.sensor.humidity

    def getPressure(self):
         return self.sensor.pressure

