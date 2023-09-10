import arcade


class RqWin(arcade.Window):
    def __init__(self):
        super().__init__(width=1280, height=720)
        self.hello_object = arcade.Text("Привет, любишь игры?", self.width // 2, self.height // 2)
        self.hello_object.anchor_x = "center"
        self.hello_object.anchor_y = "center"
        self.hello_object.position = (self.width // 2, self.height // 2)

    def on_draw(self):
        self.clear()
        self.hello_object.draw()


if __name__ == '__main__':
    HelloWindow = RqWin()
    HelloWindow.run()
