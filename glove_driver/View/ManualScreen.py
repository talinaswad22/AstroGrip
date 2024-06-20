from View.AbstractView import AbstractView
import plotext as pltx

class ManualScreenView(AbstractView):
    def __init__(self):
        self.colors = ["red", "blue", "green"]
        self.color_state = 0

    def isr_state_transition(self):
        self.color_state = 0 if self.color_state == len(self.colors)-1 else self.color_state+1
    
    def isr_state_action(self):
        self.color_state =  len(self.colors)-1 if self.color_state==0 else self.color_state-1


    def animate(self):
        pltx.clf()
        pltx.text("Innocent Text that is not a placeholder for something really bad I wrote", x=0,y=0,alignment="center",color=self.colors[self.color_state])
        pltx.xticks([])
        pltx.yticks([])
        pltx.show()