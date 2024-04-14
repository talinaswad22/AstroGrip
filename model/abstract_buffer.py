class AbstractBufferQueue:
    def __init__(self,sample_object):
        self.__sample_object = sample_object
    
    # queue behavior
    def on_full(self):
        raise NotImplementedError()
    
    def append(self,scalar):
        raise NotImplementedError()

    # sample/sensor behavior
    def sample(self):
        raise NotImplementedError()
    
    def transition(self):
        raise NotImplementedError()
    
    @property
    def name(self):
        return self.sample_object.name