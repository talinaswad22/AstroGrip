import keyboard
from model.model import on_start_up, action_loop, isr_state_transition, isr_state_action






no_escape = True
def esc_key_action(keyboard_event):
    global no_escape
    no_escape=False
keyboard.on_release_key('esc',esc_key_action)

on_start_up()
while no_escape:
    action_loop()