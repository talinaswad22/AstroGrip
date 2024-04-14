import sensor.abstract_sensor as abstract_sensor


class SawtoothSensor(abstract_sensor):
    def __init__(self,name,amplitude=1,frequency=4,step=0.2):
        super().__init__(name)
        self.amplitude = amplitude
        self.frequency = frequency
        self.i=0

    def __initialize_sensor(self):
        pass

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def sample(self):
        if self.frequency<self.i:
            self.i=0
        d = self.amplitude*self.i
        return d