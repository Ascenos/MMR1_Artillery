# TODO import pyqt and make frame stuff



class BaseRenderer:
    def __init__(self):
        # TODO set frame here
        self._frame = None

    def render(self, game_objects):
        """
        Renders the supplied game objects.
        """
        for game_object in game_objects:
            # Let game objects render themselves onto the frame
            game_object.render(self._frame)