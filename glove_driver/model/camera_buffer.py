from model.abstract_buffer import AbstractBufferQueue
from data.access import write_data2image

class CameraBufferQueue(AbstractBufferQueue):
    def __init__(self,sample_object):
        super().__init__(sample_object)
        self.__container = None
        self.__last_uuid = None # for passing a reference to the image for plotting
        self.__open_jobs = 0    # for tracking how many pictures still need to be taken
        # this is due to the fact that a user could press the record button multiple times

    
    # queue behavior
    def on_full(self):
        self.__last_uuid = write_data2image(self.__container,f"./{self.name}")
        self.__container = None

    
    def append(self,values):
        self.__container = values
        self.on_full()

    # sample/sensor behavior
    def sample(self):
        if self.__open_jobs<=0:
            raise Exception("CameraBufferQueue reached illegal state trying to take picture when no pending jobs exist.")
        self.__container-=1

        # TODO add exception check here
        self.append(self.__sample_object.sample())
        

    def transition(self):
        while self.__open_jobs>0:
            self.sample()

    def open_job(self):
        self.__open_jobs +=1

    def check_for_jobs(self):
        return self.__open_jobs>0

    @property
    def last_job(self):
        return self.__last_uuid