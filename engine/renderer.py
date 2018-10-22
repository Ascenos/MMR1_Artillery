from abc import (
    ABC,
    abstractmethod,
)



class BaseRenderer(ABC):
    def render(self, game_objects):
        """
        Renders the supplied game objects.
        """
        for game_object in game_objects:
            # TODO define render_info structure
            # Get the render_info
            render_info = game_object.render_info()
            self._real_render(render_info)

    @abstractmethod
    def _real_render(render_info):
        """
        This will be the actual function to render the object.

        Has to be implemented in derived class
        """
        pass