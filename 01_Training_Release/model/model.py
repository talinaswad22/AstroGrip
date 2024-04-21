# for control of system
from time import sleep
import plotext as pltx
from keyboard import on_release_key
from time import time

# sensors
from sensor.sensor_adapter import AdapterSensor
from sensor.bmp581_sensor import BMP581Sensor
from sensor.spectrometer_sensor import SpectrometerSensor

# for data writing
from data.access import  initialize_session
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
    labels = ["Temperature",
              "Saw 1",
              "Gaus 3",
              ]
    shared_bmp = BMP581Sensor("Temperature-/Pressuresensor")
    containers.extend([
        CSVBufferQueue(AdapterSensor("Temperature",shared_bmp,lambda x:x.sample_temperature())
                       ,storage_buffer_size=writeBufferSize,data_buffer_size=10,time_buffer=True),
        CSVBufferQueue(AdapterSensor("Pressure",shared_bmp,lambda x:x.sample_pressure())
                       ,storage_buffer_size=writeBufferSize,data_buffer_size=10,time_buffer=True),
        CSVBufferQueue(SpectrometerSensor("Spectrometer"),writeBufferSize,data_buffer_size=10,time_buffer=False)
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
    # this function only gets called, when shutting down, do for example an interrupt
    # so catching anything is reasonable, due to trying to free resources
    for con in containers:
        try:
            con.close()
        except:
            pass

# method called for sampling passive sensors
def passive_sample():
    # sampling data
    [containers[i].sample() for i in passive_containers if i != state]



################################
# state control
################################
def isr_state_transition(keyboard_event):
    global transition_signal
    transition_signal = True

def transition_action():
    global state, data_buffer, time_buffer
    # transition of sensor and associated storage before into inactive state
    # as of now only active for taking image with camera
    containers[state].transition()
    state+=1
    if state==NUM_STATES:
        state=0

    data_buffer = containers[state].data_buffer
    if containers[state].use_time:
        time_buffer = containers[state].time_buffer
    
def isr_state_action(keyboard_event):
    global state
    # this is just used for setting an open job
    # for taking a picture, but could be used for other tasks
    # should only change the internal state of a data collection object
    containers[state].open_job()



################################
# set figure
################################
def set_state_labels():
    global state
    pltx.subplot(1,2)
    temp = labels.copy()
    temp[state] = f"> {temp[state]}"
    [pltx.text(temp[i], x=1,y=i,alignment="center",color="red") for i in range(len(temp))]

def set_up_plot():
    pltx.clf()
    pltx.subplots(1,2)      
    set_state_labels()
    pltx.subplot(1,1)

def prepare_time_data(time_ar):
    t = time()
    return [x-t for x in time_ar]

# main loop
def animate(state):
    global data_buffer,time_buffer
    # control of what gets sampled

    # sample values

    # decide based on state
    
    """
    Tip: check up if above the time, buffer is set when calling prepare time, otherwise error happens
    """
    
    
    match state:
        case 0: # temperature - scatter
            containers[state].sample() 
            set_up_plot()  
            #pltx.plot(data_buffer)
            pltx.plot(prepare_time_data(time_buffer),data_buffer)
        case 1: # pressure - scatter
            containers[state].sample()
            set_up_plot()
            #pltx.plot(data_buffer)
            pltx.plot(prepare_time_data(time_buffer),data_buffer)
                

        case 2: # distance
            containers[state].sample()
            set_up_plot()
            #TODO add wavelength area
            pltx.plot(data_buffer)
        case _:
            pass

    pltx.show()

def action_loop():
    global transition_signal, passive_sample_counter
    # to ensure that the state does not get changed mid operation
    if transition_signal:
        transition_signal = False
        transition_action()
    # 
    if not passive_sample_counter:
        passive_sample_counter-=1
        if not passive_sample_counter: passive_sample_counter= PASSIVE_SAMPLE_PERIODS
        passive_sample()
    
    animate(state)
    sleep(sleep_time)