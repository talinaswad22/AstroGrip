from collections import deque
from time import time

from model.abstract_buffer import AbstractBufferQueue
from data.access import write_data2csv

class CSVBufferQueue(AbstractBufferQueue):
    def __init__(self,sample_object,size):
        super().__init__(sample_object)
        self.__size = size
        self.__container = deque(maxlen=self.size)

    
    # queue behavior
    def on_full(self):
        write_data2csv(self.__container,f"./{self.name}")
        self.__container.clear()
    
    def append(self,values):
        self.__container.append((values,time()))
        if len(self.__container) == self.__size:
            self.on_full()

    # sample/sensor behavior
    def sample(self):
        self.append(self.__sample_object.sample())

    def transition(self):
        sample = self.__sample_object.transition()
        if sample != None:
            self.append(sample)

    