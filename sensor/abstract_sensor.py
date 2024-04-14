class AbstractSensor:
    def __init__(self,name):
        self.__name
        self.__initialize_sensor()

    def __initialize_sensor(self):
        raise NotImplementedError()

    def turn_on(self):
        raise NotImplementedError()

    def turn_off(self):
        raise NotImplementedError()

    def sample(self):
        raise NotImplementedError()
    
    def state_transition(self):
        pass

    @property
    def name(self):
        return self.__name

