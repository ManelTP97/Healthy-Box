import board
import busio
import adafruit_mlx90640

class MLX90640:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
        self.mlx = adafruit_mlx90640.MLX90640(i2c)

    def getTemp(self):
        self.mlx.getFrame()
