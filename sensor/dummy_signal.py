from numpy.random import normal

period_saw = 0
def saw_signal():
    global period_saw
    period_saw +=1
    return (period_saw-1)%5

def random_signal():
    return normal()