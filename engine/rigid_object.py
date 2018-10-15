from .game_object import GameObject



class RigidObject(GameObject):
    """
    A GameObject class that does not recieve many updates.
    """
    def __new__(cls, *args, **kwargs):
        rigid_object = super().__new__(cls, *args, **kwargs)
        # Create base shape of the object
        rigid_object._base()
        return rigid_object
        # TODO maybe add something more

    def _base(self):
        """
        This will be the base look of the Object

        abstractmethod
        """
        pass

    # TODO maybe do collision info a class
    def collision_info(self, point):
        """
        This returns eventual collision with a point.

        abstractmethod
        """
        pass
