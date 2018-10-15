from .game_object import GameObject



class RigidObject(GameObject):
    """
    A GameObject class that does not recieve many updates.
    """
    # TODO implement more convinience functions
    def __init__(self):
        self._base()
        # TODO maybe add something more

    def _base(self):
        """
        This will be the base look of the Object

        abstractmethod
        """
        pass

    # TODO maybe do collision info a class
    def collision_info(self):
        """
        This returns eventual collision info that can be used by other objects

        abstractmethod
        """
        pass

    # TODO make render info a class
    def render_info(self):
        """
        This returns the render information that the renderer can
        use to draw the object

        abstractmethod
        """
        pass
