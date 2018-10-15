from .game_object import GameObject
from .input import input_provider
from .base import engine



class InputObject(GameObject):
    def get_input(self):
        return engine.Input
