import sensor.abstract_sensor as abstract_sensor
from numpy.random import normal

class GaussianSensor(abstract_sensor):
    def __init__(self,name,mean=0,cov=1):
        super().__init__(name)
        self.mean = mean
        self.cov = cov

    def __initialize_sensor(self):
        pass

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def sample(self):
        return normal(self.mean,self.cov)