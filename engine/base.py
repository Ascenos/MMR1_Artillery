from .renderer import BaseRenderer



class GameBehaviour:
    def __init__(self, function, root):
        # Maybe initialize something?
        try:
            self._iter_function = iter(root.function())
        # TODO make explicit error catch
        except:
            raise ValueError('This cannot be a Behavior.') from None
        self._base_function = function

    @property
    def ID(self):
        return id(self)

    @property
    def base_function(self):
        return self._base_function

    def __next__(self):
        return next(self._iter_function)

class Engine:
    # TODO improve docstring
    """
    Main class for the Engine, the handeling and stuff.

    DON'T use this class directly. Instead use the wrappers provided in
    GameObject to interact with this thing
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Implement singleton structure, only one engine should run a time
        """
        if cls.__instance == None:
            # Singleton not created, let's do that
            engine = super().__new__(cls, *args, **kwargs)
            cls.__instance = engine
            return engine
        else:
            # Tried to create another instance, raise the Runtime Error
            raise RuntimeError('Another Instance of the Engine was created.')

    def __init__(self):
        """
        Set up basic things
        """
        self.renderer = BaseRenderer()
        self._game_objects = []
        self._game_behaviors = []

    def _active_game_objects(self):
        """
        Return a list of game objects that are active
        """
        return [
            game_object
            for game_object in self._game_objects
            if game_object.ACTIVE
        ]

    def _visibles(self):
        """
        Return a list of visible gameObjects, that therefore need to be drawn.
        """
        return [
            game_object
            for game_object in self._active_game_objects()
            if game_object.VISIBLE
        ]

    def search_for_objects(self, object_type):
        """
        Uses isinstance to filter the loaded GameObject list
        """
        return [
            game_object
            for game_object in self._active_game_objects()
            if isinstance(game_object, object_type)
        ]

    def add_object(self, game_object):
        """
        Add a game object to the engines object list
        """
        self._game_objects.append(game_object)

    def remove_game_object(self, game_object):
        """
        Removes a game object from the game
        """
        for game_object in self._game_objects:
            if id(game_object) == id(remove_object):
                

    def start_behavior(self, behavior):
        """
        Adds a coroutine to be run every update (maybe more frequently(?))
        """
        self._game_routines.append(behavior)

    def stop_behavior(self, remove_id):
        """
        Stops the first coroutine as same as the routine
        """
        for behavior in self._game_behaviors:
            # Check if their base functions are the same
            if behavior.ID == remove_id:
                self._coroutines.remove(behavior)
                return

    def stop_all_behaviors(self):
        """
        Stops all coroutines.

        Be sure to start the next routine in the same iteration
        """
        self._game_routines = []


    def update(self):
        # Let the renderer draw the Objects that are visible
        self.renderer.render(self._visibles())
        for behavior in self._game_behaviors:
            try:
                value = next(coroutine)
            except StopIteration:
                # Coroutine was stopped normaly, continue
                self.StopCoroutine(coroutine)

# Use this singleton instance in the main project
engine = Engine()