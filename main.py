import keyboard
import model.model as model



keyboard.on_release_key('w', model.isr_state_transition)
keyboard.on_release_key('e', model.isr_state_action)


no_escape = True
def esc_key_action(keyboard_event):
    global no_escape
    no_escape=False
keyboard.on_release_key('esc',esc_key_action)


while no_escape:
    model.on_start_up()
    model.action_loop()