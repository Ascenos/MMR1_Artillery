# TODO implement this



class Input:
    pass

class InputProvider:
    def __init__(self):
        self._input_buffer = []

    def get_input(self, empty_buffer=True):
        """
        Empty buffer and return all the inputs saved in it
        """
        _temp_buffer = self._input_buffer
        if empty_buffer:
            self._input_buffer = []
        return _temp_buffer

input_provider = InputProvider()
