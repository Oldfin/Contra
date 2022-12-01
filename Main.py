import arcade
from constants import *
import bill


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.setup()
        self.bg_textures = []
        for i in range (1, 16):
            self.bg_textures.append(arcade.load_texture(f'background/Map{i}.png'))
        self.index_texture = 0
        self.game = True
        self.bill = bill.Bill()

    def setup(self):
        pass

    def on_draw(self):
        self.clear((255, 255, 255))
        arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_textures[self.index_texture])
        self.bill.draw()

    def update(self, delta_time):
        if self.game:
            self.bill.update()

    def on_key_press(self, key, modifiers):
        pass

    def on_key_release(self, key, modifiers):
        pass


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()
