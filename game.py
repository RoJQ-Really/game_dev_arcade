import arcade
import system
import PIL.Image


class RqWindow(arcade.Window):
    def __init__(self, physic_engine = None, world_engine = None, event_engine = None, ui_engine = None):
        super().__init__(width=1280, height=720, title="")

        self._system_engine = system.SystemEngine(self)
        self.__init_engines()

    def __init_engines(self):
        self._system_engine.init_function()

    def on_draw(self):
        self.clear()
        self._system_engine.on_draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self._system_engine.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self._system_engine.on_mouse_motion(x, y, dx, dy)

    def update(self, delta_time: float):
        self._system_engine.update()


if __name__ == '__main__':
    _window = RqWindow()
    _window.run()