from engine import *



class MainGameFunction(GameFunction):
    # TODO implement main logic here
    def function(self):
        print('Do some stuff')
        yield  # Return the control to the main loop
        while True:
            yield