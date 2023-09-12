import pathlib
import arcade
import pyglet


class Player(arcade.Sprite):
    def __init__(self, filename: pathlib.Path, keyboard: pyglet.window.key.KeyStateHandler, texture_dict: dict):
        """
        Данный класс представляет собой тестового игрока. В разработке
        :param filename: Путь к файлу изображения
        :param keyboard: Клавиатурный объект
        :param texture_dict: Словарь текстур для спрайта
        """
        super().__init__(filename=None)
        self.textures = [texture_dict.get("stay", None)]  # Устанавливаем базовую текстуру
        self.set_texture(0)

        self.animation_dict = {
            "stay" : None,
            "run" : None
        }

        self.texture_dict = texture_dict  # Добавляем данный словарь как поле класса
        self.facing = 1  # < if facing == 1 => вправо иначе влево
        self.keyboard_data = keyboard
        self.speed = 5  # Скорость
        self.acceleration = 2  # Ускоренние

        self.animation_init()  # Инициализация анимаций

    def do_move(self):
        self.facing = (self.keyboard_data[arcade.key.D] - self.keyboard_data[arcade.key.A])  # Определяем направление
        self._coefficient_acceleration = self.facing * (self.acceleration * self.keyboard_data[arcade.key.LSHIFT])  # Определяем коефицент ускорения
        dx = self.speed * self.facing + self._coefficient_acceleration  # Определяем смещение объекта по оси x
        self.center_x += dx  # Выполняем данное смешение