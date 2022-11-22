from .Joystick import Joystick
class Controller:
    joystick = Joystick()

    def getControllerInput(self):
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False, 'a_pressed' : False, 'a_released' : False}
        
        if not self.joystick.button_U.value:  # up pressed
            command['up_pressed'] = True
            command['move'] = True

        if not self.joystick.button_D.value:  # down pressed
            command['down_pressed'] = True
            command['move'] = True

        if not self.joystick.button_L.value:  # left pressed
            command['left_pressed'] = True
            command['move'] = True

        if not self.joystick.button_R.value:  # right pressed
            command['right_pressed'] = True
            command['move'] = True

        if not self.joystick.button_A.value: # A pressed
            command['a_pressed'] = True
            command['move'] = True

        if self.joystick.button_A.value: # A released
            command['a_released'] = True
            command['move'] = True

        return command