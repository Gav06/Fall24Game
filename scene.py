from abc import abstractmethod

# Our class for each scene.
# The abstract methods are just methods that we will define in subclasses, at a later time
class Scene:
    # Empty list of GameObject classes
    game_objects = []

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def draw_scene(self):
        pass

    @abstractmethod
    def update_scene(self, events):
        pass

    @abstractmethod
    def mouse_clicked(self, x, y, button):
        pass

    @abstractmethod
    def mouse_released(self, x, y, button):
        pass

    @abstractmethod
    def key_pressed(self, x, y, button):
        pass


class MainMenu(Scene):

    def __init__(self):
        super().__init__("mainmenu")

    def draw_scene(self):
        pass

    def update_scene(self, events):
        pass

