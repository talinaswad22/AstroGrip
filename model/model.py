# for control of system
from time import sleep
import plotext as pltx

# sensors
from sensor.camera import cam_start_up,capture_image
from sensor.gaussian_sensor import GaussianSensor
from sensor.sawtooth_sensor import SawtoothSensor

# for data writing
from data.access import  initialize_session,write_data2image, write_data2csv
from model.abstract_buffer import CSVBufferQueue

# TODO Löse folgende Liste
"""
- Camera aufnahme für transitions machen
- passives Samples einabuen
    - passive und aktive liste bereitstellen
    - leer verhalten für Zustände einbauen
- control layer zwischen model und data
"""

# on start up
#List of data
dataList = [0]
imageTaken = False
bufferSize = 50
# state control
NUM_STATES = 5
state = 0
sleep_time = 0.3
# figure
#labels
containers = []
row_names = []

################################
# action control
################################
def on_start_up():
    initialize_session()
    cam_start_up()
    # set up buffers
    # the order of passing here is important, as the animation is hard coded based on the order
    containers.extend(
        CSVBufferQueue(GaussianSensor("Gaus 1",0,1),bufferSize),
        CSVBufferQueue(GaussianSensor("Gaus 2",1,1),bufferSize),
        CSVBufferQueue(GaussianSensor("Gaus 3",2,1),bufferSize),
        CSVBufferQueue(SawtoothSensor("Saw 1",1,4),bufferSize),
        BufferQueue(GaussianSensor(),bufferSize),
        # camera
    )

# method called for sampling passive sensors
def passive_sample():
    # sampling data


    #storing data
    
    pass


################################
# state control
################################
def isr_state_transition(keyboard_event):
    global state, imageTaken

    state+=1
    if state==NUM_STATES:
        state=0
    if imageTaken:
        imageTaken = False
        # TODO implement imaging taking and image saving


    # TODO implement video capture if image could not be captured in time
    
def isr_state_action(keyboard_event):
    global state, imageTaken
    match state:
        case 0: # plot
            pass
        case 1: # image
            imageTaken = True
        case 2: # hist
            pass
        case 3: # hist
            pass
        case 4: # hist
            pass
        case _:
            pass



################################
# set figure
################################
def set_state_labels(keyboard_event):
    global state
    pltx.subplot(1,2)
    temp = row_names.copy()
    temp[state] = f"> {temp[state]}"
    [pltx.text(temp[i], x=1,y=i,aligment="center",color="red") for i in range(len(temp))]


# main loop
def animate(dataList,state, imageTaken):
    # control of what gets sampled

    # sample values

    # decide based on state
    
    pltx.subplots(2,1)      
    set_state_labels()
    
    match state:
        case 0: # plot
            pltx.clf()
        case 1: # image
            if imageTaken:
                pltx.clf()
                imageTaken = False
                # Capture an image
                image = capture_image()

                # TODO implement saving of data

                # TODO adapt image plotting
                

        case 2: # hist
            pltx.clf()
        case 3: # hist
            pltx.clf()
        case 4: # hist
            pltx.clf()
        case _:
            pass

    pltx.show()

def action_loop():
    passive_sample()
    animate(dataList=dataList,state=state,imageTaken=imageTaken)
    sleep(sleep_time)