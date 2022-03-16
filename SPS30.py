from sps30 import SPS30


class SPS30:
    def __init__(self):

        self.sps = SPS30(1)
        self.sps.start_measurement()

    def getPM(self):
        self.PM = []

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
        
