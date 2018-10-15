from .game_object import GameObject
from input import input_provider



class InputObject(GameObject):
    def

    def pull_input(self):
        """
        This method will provide the object with its needed input
        Supply your input getting routine here
        """
        return input_provider.get_input()