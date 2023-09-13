import pathlib
import typing
import PIL.ImageDraw
from arcade import Point
import system_script
import abstract
import arcade
import pyglet
import traceback

def callback_tester():
    print("WOORRRK")


class UiManager:
    def __init__(self, ui_list: arcade.SpriteList, mouse_sprite: arcade.Sprite):
        self.__ui: arcade.SpriteList = ui_list
        self.__mouse: arcade.Sprite = mouse_sprite

    def draw(self):
        self.__ui.draw()
        self.__mouse.draw()

    def create_button(self, text: str, callback: typing.Callable):

        obj = ButtonSprite(text=text, filepath_font="resource\\fonts\\Komi.ttf", callback=callback)
        obj.scale = 0.1
        obj.position = 1280 // 2, 720 // 2

        self.__ui.append(obj)
        print(obj, text)

    def draw_hit_boxes(self, color: tuple = (255, 0, 0), line_width: int = 1):
        self.__ui.draw_hit_boxes(color, line_width)
        self.__mouse.draw_hit_box(color, line_width)


class ButtonSprite(arcade.Sprite):
    def __init__(self, text: str, filepath_font: pathlib.Path, callback: typing.Callable, args: dict = {}, font_size: int = 500):
        image_texture = system_script._draw_button_texture(path_to_font=filepath_font, size=font_size, color=(1, 1, 1, 0), text=text)
        texture = arcade.Texture("txt__1", image=image_texture)
        super().__init__(texture=texture)
        self.__callback = callback
        self.__args = args

    def execute(self):
        """
        Выполняется скрипт
        :return:
        """
        self.__callback(**self.__args)

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        super().draw()  # Сначала рисуем задний фон спрайта


class SystemEvent:
    def __init__(self, app: arcade.Window, callback: typing.Callable, args: dict = {}):
        self.__app = app  # Сао приложение
        self.__callback = callback
        self.__args = args

    def run(self):
        self.__callback(**self.__args)


class SystemEngine(abstract.RqEngine):
    def __init__(self, app : arcade.Window):
        """
        Данный класс реализует так называемый *ПД*.
        :param app: Приложение игры
        """
        self._ui_windows = arcade.SpriteList()  # Лист содержаший в себе ui элементы
        self.mouse_tracking_sprite = arcade.Sprite(filename="resource\\cursor\\cursor.png")  # Спрайт отвечающий за мышь
        self.mouse_tracking_sprite.scale = 0.03
        self.__app = app  # Приложение игры
        self.__script_data = {}

        self.__ui_manager = UiManager(ui_list=self._ui_windows, mouse_sprite=self.mouse_tracking_sprite)  # Менеджер отрисовки ui

    def create_button(self, text: str, callback: typing.Callable):
        """
        :param text: Текст который будет писаться на кнопке
        :param callback: Функция которая будет вызываться
        :return:
        """
        self.__ui_manager.create_button(text, callback)

    def init_function(self, **kwargs):
        self.create_button("+", callback_tester)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_tracking_sprite.set_position(x, y)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        for i in arcade.check_for_collision_with_list(self.mouse_tracking_sprite, self._ui_windows):
            if isinstance(i, ButtonSprite):
                i.execute()

    def update(self):
        pass

    def on_draw(self):
        self.__ui_manager.draw()
        self.__ui_manager.draw_hit_boxes()




