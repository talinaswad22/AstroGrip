# for control of system
from time import sleep
import plotext as pltx
from keyboard import on_release_key
from time import time

# sensors
from sensor.dummy_gaussian_sensor import GaussianSensor
from sensor.dummy_sawtooth_sensor import SawtoothSensor
from sensor.dummy_camera_sensor import CameraSensor

# for data writing
from data.access import  initialize_session,create_access_path
from model.csv_buffer import CSVBufferQueue
from model.camera_buffer import CameraBufferQueue


# on start up
#List of data
writeBufferSize = 50
data_buffer = None
time_buffer = None

# state control
NUM_STATES = 5
state = 0
# for controlling passive sampling
PASSIVE_SAMPLE_PERIODS = 6
passive_sample_counter = PASSIVE_SAMPLE_PERIODS
# for controlling transition
transition_signal = False
# 0.5 should be left this way, because pressure/temperature sensor could potentially not sample faster
# or needs to be adapted
sleep_time = 0.5

# figure
#labels
containers = []
passive_containers = []
labels = None

################################
# action control
################################
def on_start_up():
    global labels, data_buffer,time_buffer, passive_containers, NUM_STATES
    # set up buffers
    # the order of passing here is important, as the animation is hard coded based on the order
    """
    Order Should be:
    0. CSV - Temperature
    1. CSV - Pressure
    2. CSV - Distance
    3. CSV - Spectrometer
    4. JPG - Image
    Make the passive sensors come first as they will always be on and not draw unnessecary power
    """
    labels = ["Gaus 1",
              "Saw 1",
              "Gaus 3",
              "Saw 1",
              #"Camera"
              ]
    containers.extend([
        CSVBufferQueue(GaussianSensor(labels[0],0,1),writeBufferSize,data_buffer_size=10,time_buffer=True),
        CSVBufferQueue(SawtoothSensor(labels[3],1,4),writeBufferSize,data_buffer_size=10,time_buffer=False),
        CSVBufferQueue(GaussianSensor(labels[2],2,1),writeBufferSize,data_buffer_size=10,time_buffer=True),
        CSVBufferQueue(SawtoothSensor(labels[3],1,4),writeBufferSize,data_buffer_size=10,time_buffer=False),
        #CameraBufferQueue(CameraSensor(labels[4]))
    ]
    )
    NUM_STATES = len(containers)

    passive_containers = [0,1]
    # initialize data layer session
    initialize_session(labels,labels[:-1])

    # set current buffers for plotting, otherwise they'd be None
    data_buffer = containers[state].data_buffer
    if containers[state].use_time:
        time_buffer = containers[state].time_buffer
    # needs to be here, otherwise you could call method before assignment of variables
    on_release_key('w', isr_state_transition)
    on_release_key('e', isr_state_action)

def on_shutdown():
    # TODO add functionality
    pass

# method called for sampling passive sensors
def passive_sample():
    pass



################################
# state control
################################
def isr_state_transition(keyboard_event):
    # TODO add state transition


def transition_action():
    # TODO add functionality
    
    
def isr_state_action(keyboard_event):
    # TODO add View call
    pass



################################
# set figure
################################






# main loop
def animate(state):   
    """
    Tip: check up if above the time, buffer is set when calling prepare time, otherwise error happens
    """
    # TODO add animate current View method
    
    
    

def action_loop():
    # to ensure that the state does not get changed mid operation
    # TODO Replace passive sampling
    if not passive_sample_counter:
        passive_sample_counter-=1
        if not passive_sample_counter: passive_sample_counter= PASSIVE_SAMPLE_PERIODS
        passive_sample()
    animate(state)
    sleep(sleep_time)