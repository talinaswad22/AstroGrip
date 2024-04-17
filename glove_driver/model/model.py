# for control of system
from time import sleep
import plotext as pltx
from keyboard import on_release_key

# sensors
from sensor.gaussian_sensor import GaussianSensor
from sensor.sawtooth_sensor import SawtoothSensor
from sensor.camera_sensor import CameraSensor

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
sleep_time = 0.3

# figure
#labels
containers = []
labels = None

################################
# action control
################################
def on_start_up():
    global labels, data_buffer,time_buffer
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
              "Camera"
              ]
    containers.extend([
        CSVBufferQueue(GaussianSensor(labels[0],0,1),writeBufferSize,data_buffer_size=10,time_buffer=True),
        CSVBufferQueue(SawtoothSensor(labels[3],1,4),writeBufferSize,data_buffer_size=10,time_buffer=False),
        CSVBufferQueue(GaussianSensor(labels[2],2,1),writeBufferSize,data_buffer_size=10,time_buffer=True),
        CSVBufferQueue(SawtoothSensor(labels[3],1,4),writeBufferSize,data_buffer_size=10,time_buffer=False),
        CameraBufferQueue(CameraSensor(labels[4]))
    ]
    )
    # initialize data layer session
    initialize_session(labels,labels[:-1])

    # set current buffers for plotting, otherwise they'd be None
    data_buffer = containers[state].data_buffer
    if containers[state].use_time:
        time_buffer = containers[state].time_buffer
    # needs to be here, otherwise you could call method before assignment of variables
    on_release_key('w', isr_state_transition)
    on_release_key('e', isr_state_action)


# method called for sampling passive sensors
def passive_sample():
    # sampling data
    containers[0].sample()
    containers[1].sample()


################################
# state control
################################
def isr_state_transition(keyboard_event):
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

# main loop
def animate(state):
    global data_buffer,time_buffer
    # control of what gets sampled

    # sample values

    # decide based on state
    
    
    
    match state:
        case 0: # temperature - scatter
            containers[state].sample() 
            set_up_plot()  
 
            pltx.plot(data_buffer)
        case 1: # pressure - scatter
            containers[state].sample()
            set_up_plot()
            pltx.plot(data_buffer)
                

        case 2: # distance
            containers[state].sample()
            set_up_plot()
            pltx.plot(data_buffer)
        case 3: # spectrometer
            containers[state].sample()
            set_up_plot()
            pltx.plot(data_buffer)
        case 4: # image
            if containers[state].check_for_jobs():
                containers[state].sample()
                set_up_plot()
                pltx.image_plot(create_access_path(containers[state].name,containers[state].last_job,"jpg"))
        case _:
            pass

    pltx.show()

def action_loop():
    passive_sample()
    animate(state)
    sleep(sleep_time)