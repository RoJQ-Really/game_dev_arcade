import pathlib
import typing

from arcade import Point

import abstract
import arcade
import pyglet
import traceback

def callback_tester():
    print("WOORRRK")


class TextList:
    def __init__(self):
        self.__list: list[arcade.Text] = []

    def append(self, txt: arcade.Text):
        self.__list.append(txt)

    def draw(self):
        for txt_element in self.__list:
            txt_element.draw()


class UiManager:
    def __init__(self, ui_list: arcade.SpriteList, text_list: TextList, mouse_sprite: arcade.Sprite):
        self.__ui = ui_list
        self.__text = text_list
        self.__mouse = mouse_sprite

    def draw(self):
        self.__ui.draw()
        self.__mouse.draw()

    def create_button(self, text: str, callback: typing.Callable):
        button = arcade.Text(text, 0, 0, font_size=36, anchor_x="center", anchor_y="center")
        obj = ButtonSprite(filepath="resource\\ui\\button_texure.png", callback=callback, text=text)
        obj.scale = 0.1
        obj.position = 1280 // 2, 720 // 2
        button.position = obj.position

        self.__ui.append(obj)
        print(obj, text)

    def draw_hit_boxes(self, color: tuple = (255, 0, 0), line_width: int = 1):
        self.__ui.draw_hit_boxes(color, line_width)
        self.__mouse.draw_hit_box(color, line_width)


class ButtonSprite(arcade.Sprite):
    def __init__(self, text: str, filepath: pathlib.Path, callback: typing.Callable, args: dict = {}):
        super().__init__(filename=filepath)
        self.__callback = callback
        self.__args = args
        self.__text = arcade.Text(text=text, start_x=self.center_x, start_y=self.center_y)
        self.__text.anchor_x = "center"
        self.__text.anchor_y = "center"
        self.__content_margin_x = 5  # Внутреннее поле x
        self.__content_margin_y = 3  # Внутренее поле y

        self.width = self.__content_margin_x * 2 + self.__text.width  # Изменяю ширину под текст
        self.height = self.__content_margin_y * 2 + self.__text.height  # Изменяю высоту под текст

    @property
    def position(self) -> Point:
        """
        Get the center x and y coordinates of the sprite.

        Returns:
            (center_x, center_y)
        """
        return self._position

    @position.setter
    def position(self, new_value: Point):
        """
        Set the center x and y coordinates of the sprite.

        :param Point new_value: New position.
        """
        if new_value[0] != self._position[0] or new_value[1] != self._position[1]:
            self.clear_spatial_hashes()
            self._point_list_cache = None
            self._position = new_value
            self.add_spatial_hashes()

            for sprite_list in self.sprite_lists:
                sprite_list.update_location(self)

    @property
    def scale(self) -> float:
        """Get the scale of the sprite."""
        return self._scale

    @scale.setter
    def scale(self, new_value: float):
        """Set the center x coordinate of the sprite."""
        if new_value != self._scale:
            self.clear_spatial_hashes()
            self._point_list_cache = None
            self._scale = new_value
            if self._texture:
                self._width = self._texture.width * self._scale
                self._height = self._texture.height * self._scale
            self.__text.width *= self._scale  # custom
            self.__text.height *= self._scale  # custom
            self.add_spatial_hashes()

            for sprite_list in self.sprite_lists:
                sprite_list.update_size(self)

    def execute(self):
        """
        Выполняется скрипт
        :return:
        """
        self.__callback(**self.__args)

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        super().draw()  # Сначала рисуем задний фон спрайта
        self.__text.draw()  # Потом текст


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
        self.text_list = TextList() # Лист содержащий в себе arcade.Text элементы
        self.mouse_tracking_sprite = arcade.Sprite(filename="resource\\cursor\\cursor.png")  # Спрайт отвечающий за мышь
        self.mouse_tracking_sprite.scale = 0.03
        self.__app = app  # Приложение игры
        self.__script_data = {}

        self.__ui_manager = UiManager(ui_list=self._ui_windows, text_list=self.text_list, mouse_sprite=self.mouse_tracking_sprite)  # Менеджер отрисовки ui

    def create_button(self, text: str, callback: typing.Callable):
        """
        :param text: Текст который будет писаться на кнопке
        :param callback: Функция которая будет вызываться
        :return:
        """
        self.__ui_manager.create_button(text, callback)

    def init_function(self, **kwargs):
        pass

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


