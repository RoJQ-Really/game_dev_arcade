import typing
import abstract
import arcade
import pyglet
import traceback

class SystemEvent:
    def __init__(self, app: arcade.Window, callback: typing.Callable, args: dict = {}):
        self.__app = app  # Сао приложение
        self.__callback = callback
        self.__args = args

    def run(self):
        self.__callback(**self.__args)


class SystemEngine(abstract.RqEngine):
    def __init__(self, app : arcade.Window):
        self._ui_windows = arcade.SpriteList()  # Лист содержаший в себе ui элементы
        self.__app = app
        self.__script_data = {
            "track_mouse_init": False
        }
        self.mouse_tracking_sprite: arcade.Sprite | None = None
        self.draw_objects = arcade.SpriteList()
        self.text_list: list[arcade.Text] = []

    def create_button(self, text: str, callback: typing.Callable):
        button = arcade.Text(text, 0, 0, font_size=36, anchor_x="center", anchor_y="center")
        obj = arcade.Sprite(filename="resource\\ui\\button_texure.png")
        obj.scale = 0.2
        obj.position = 1280 // 2, 720 // 2
        button.position = obj.position


        self._ui_windows.append(obj)
        self.text_list.append(button)



    def init_function(self, **kwargs):
        self.create_button("kek", self.callback_1)

        self.track_mouse_init()



    def callback_1(self):
        print("worked")

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.__script_data["track_mouse_init"] is False:
            return
        self.mouse_tracking_sprite.set_position(x, y)

    def track_mouse_init(self):
        self.mouse_tracking_sprite = arcade.Sprite(filename="resource\\cursor\\cursor.png")
        self.mouse_tracking_sprite.scale = 0.03
        print(self.mouse_tracking_sprite.get_hit_box())
        self.draw_objects.append(self.mouse_tracking_sprite)
        self.__script_data["track_mouse_init"] = True

    def update(self):

        if arcade.check_for_collision(self.mouse_tracking_sprite, self._ui_windows[-1]):
            self._ui_windows[-1].color = (255, 0, 255)
        else:
            self._ui_windows[-1].color = (255, 255, 255)

    def on_draw(self):
        self._ui_windows.draw()
        self._ui_windows.draw_hit_boxes(color=(255, 0, 0))
        for i in self.text_list:
            i.draw()
        self.draw_objects.draw()
        self.draw_objects.draw_hit_boxes(color=(255, 0, 0))


