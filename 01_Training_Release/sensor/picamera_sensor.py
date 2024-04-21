from sensor.abstract_sensor import AbstractSensor
from picamera import PiCamera

class CameraSensor(AbstractSensor):
    def __init__(self,name):
        super().__init__(name)
        self.__initialize_sensor()
        
    def __initialize_sensor(self):
        self.__cam = PiCamera()

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def sample(self):
        with Pi
        
        return image