import pathlib
import arcade
import pyglet.window.key



class PlayerTest(arcade.Sprite):
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
        if self.facing != 0:
            print("гоним")
            self.player_animation_run.start_animation()
        if self.facing != 0:
            self.set_texture(0)

    def animation_init(self):
        """
        Данная функция инициилизирует анимации!
        :return:
        """
        self.player_animation_run = RqAnimation(anim_obj=self, animation_list=self.texture_dict.get("run"))



class RqAnimation:
    def __init__(self, anim_obj: arcade.Sprite = None, animation_list: list[arcade.Texture] = None):
        """
        Класс представляет собой базовую реализацию анимаций для спрайтов. В разработке
        :param anim_obj: Анимируемый объект
        :param animation_list: Листы анимации
        """
        if animation_list is None or anim_obj is None:
            self.loaded = False
            return
        self.loaded = True
        self.__data = animation_list
        self.__index_max = len(animation_list) - 1
        self.__index = 0
        self.anim_obj = anim_obj
        print(self.__data)
        self.__start_with = len(self.anim_obj.textures)
        tmp = self.__data + self.anim_obj.textures
        self.anim_obj.textures = tmp

    def start_animation(self):
        if self.loaded is False:
            raise AttributeError("Анимация не загруженна")

        self.anim_obj.set_texture(self.__start_with + self.__index_max)
        print(self.__index)
        if self.__index == self.__index_max:
            self.__index = 0
            return
        self.__index += 1

class RqWindow(arcade.Window):
    def __init__(self):
        super().__init__(width=1280, height=720, title="1. TestPlayer")
        self._events_list = []
        self.player_: None | PlayerTest = None

        self.create_player()

    def generate_player_texture(self, filepath : pathlib.Path):
        texture_list = arcade.load_spritesheet(file_name=filepath, sprite_width=32, sprite_height=32, columns=23, count=23*4)

        player_texture = texture_list[23]
        player_run_animation = texture_list[23::23 + 3]
        final_dict = {
            "stay": player_texture,
            "run" : player_run_animation
        }
        return final_dict

    def create_player(self):
        """
        Данная функция инициилизирует игрока
        :return:
        """
        texture_dict = self.generate_player_texture("assets\\characters.png")
        texture_stay: arcade.Texture = texture_dict.get("stay")

        self.player_ = PlayerTest("assets\\characters.png", self.keyboard, texture_dict)
        self.player_.scale = 3
        self.player_.set_position(200, 200)



    def on_draw(self):
        self.clear()
        self.player_.draw()

    def update(self, delta_time: float):
        self.player_.do_move()  # Обнавляем игрока

if __name__ == '__main__':
    app = RqWindow()
    app.run()
