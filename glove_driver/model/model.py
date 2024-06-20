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

# for different views
from View.MainScreen import MainScreenView
from View.ManualScreen import ManualScreenView


# on start up
#List of data
writeBufferSize = 50

# state control
view_state = 0
main_view = None
manual_view = None
# for controlling passive sampling
PASSIVE_SAMPLE_PERIODS = 6
passive_sample_counter = PASSIVE_SAMPLE_PERIODS
# 0.5 should be left this way, because pressure/temperature sensor could potentially not sample faster
# or needs to be adapted
sleep_time = 0.5




################################
# action control
################################
def on_start_up():
    global main_view,manual_view
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
    containers = [
        CSVBufferQueue(GaussianSensor(labels[0],0,1),writeBufferSize,data_buffer_size=10,time_buffer=True),
        CSVBufferQueue(SawtoothSensor(labels[3],1,4),writeBufferSize,data_buffer_size=10,time_buffer=False),
        CSVBufferQueue(GaussianSensor(labels[2],2,1),writeBufferSize,data_buffer_size=10,time_buffer=True),
        CSVBufferQueue(SawtoothSensor(labels[3],1,4),writeBufferSize,data_buffer_size=10,time_buffer=False),
        #CameraBufferQueue(CameraSensor(labels[4]))
    ]
    passive_containers = [0,1]
    # initialize data layer session
    initialize_session(labels,labels[:-1])

    # create Views
    main_view = MainScreenView(containers,passive_containers,labels)
    manual_view = ManualScreenView()

    # needs to be here, otherwise you could call method before assignment of variables
    on_release_key('w', isr_state_transition)
    on_release_key('e', isr_state_action)
    on_release_key("r", isr_view_transition)

def on_shutdown():
    main_view.on_shutdown()

# method called for sampling passive sensors
def passive_sample():
    main_view.passive_sample()


################################
# state control
################################
def isr_state_transition(keyboard_event):
    if view_state==0:
        main_view.isr_state_transition()
    else:
        manual_view.isr_state_transition()    
    
    
def isr_state_action(keyboard_event):
    if view_state==0:
        main_view.isr_state_action()
    else:
        manual_view.isr_state_action()

def isr_view_transition(keyboard_event):
    global view_state
    # it's the xor operator
    view_state ^= 1


################################
# set figure
################################
# main loop
def animate():   
    """
    Tip: check up if above the time, buffer is set when calling prepare time, otherwise error happens
    """
    # TODO add animate current View method
    if view_state==0:
        main_view.animate()
    else:
        manual_view.animate()
    
    
    

def action_loop():
    global passive_sample_counter, PASSIVE_SAMPLE_PERIODS
    # to ensure that the state does not get changed mid operation
    # TODO Replace passive sampling
    if not passive_sample_counter:
        passive_sample_counter-=1
        if not passive_sample_counter: passive_sample_counter= PASSIVE_SAMPLE_PERIODS
        passive_sample()
    animate()
    sleep(sleep_time)