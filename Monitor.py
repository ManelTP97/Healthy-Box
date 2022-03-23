import RPi.GPIO as GPIO
import adafruit_bme680
import board
from sps30 import SPS30
import busio
import adafruit_sgp30


class Monitoring:
    def __init__(self):
        self.i2c = board.I2C()

        GPIO.setmode(GPIO.BCM)

        self.pinVent = 22
        GPIO.setup(self.pinVent, GPIO.OUT)

        self.pinDoor = 27
        GPIO.setup(self.pinDoor, GPIO.OUT)

        self.pinHall = 17
        GPIO.setup(self.pinHall, GPIO.IN)
        GPIO.add_event_detect(self.pinHall, GPIO.RISING)

        self.sps = SPS30(1)

    # BME680 Temperatur  und Gas
    def getTemp(self):
        self.sensor = adafruit_bme680.Adafruit_BME680_I2C(self.i2c)
        return self.sensor.temperature

    def getGas(self):
        return self.sensor.gas

    def getHumidity(self):
        return self.sensor.humidity

    def getPressure(self):
        return self.sensor.pressure

    # SPS30 Feinstaub und Gas als Liste
    def getPM(self):
        self.PM = []
        self.sps.start_measurement()

        while True:

            if self.sps.read_measured_values() == self.sps.MEASURED_VALUES_ERROR:
                raise Exception("Measured Values CRC Error")
            else:
                self.PM.append(str(self.sps.dict_values['pm1p0']))
                self.PM.append(str(self.sps.dict_values['pm2p5']))
                self.PM.append(str(self.sps.dict_values['pm4p0']))
                self.PM.append(str(self.sps.dict_values['pm10p0']))
                self.sps.start_fan_cleaning()
                break

        return self.PM

    def getNC(self):
        self.NC = []
        self.sps.start_measurement()

        while True:

            if self.sps.read_measured_values() == self.sps.MEASURED_VALUES_ERROR:
                raise Exception("Measured Values CRC Error")
            else:
                self.NC.append(str(self.sps.dict_values['nc0p5']))
                self.NC.append(str(self.sps.dict_values['nc1p0']))
                self.NC.append(str(self.sps.dict_values['nc2p5']))
                self.NC.append(str(self.sps.dict_values['nc4p0']))
                self.NC.append(str(self.sps.dict_values['nc10p0']))
                self.sps.start_fan_cleaning()
                break

        return self.NC

    # SGP30 eCO2 und TVOC
    def geteCO2(self):
        self.i2c2 = busio.I2C(board.SCK, board.SDA, frequency=100000)
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(self.i2c2)
        return self.sgp30.eCO2

    def getTVOC(self):
        self.i2c2 = busio.I2C(board.SCK, board.SDA, frequency=100000)
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(self.i2c2)
        return self.sgp30.TVOC

    # Lüfter
    def ventOn(self):
        GPIO.output(self.pinvent, 1)

    def ventOff(self):
        GPIO.output(self.pinvent, 0)

    # Magnetschloss
    def doorOpen(self):
        GPIO.output(self.pindoor, 0)

    def doorClose(self):
        GPIO.output(self.pindoor, 1)

    # Hall-Sensor
    def getDoor(self):
        # 0 = auf, 1 = zu
        self.door = 0

        if GPIO.event_detected(self.pinhall):
            self.door = 1

        return self.door
