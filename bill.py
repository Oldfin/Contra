import arcade
import animate
from constants import *


class Bill(animate.Animate):
    def __init__(self):
        super().__init__('go_bill/0.gif', scale=SCALING)
        self.center_x = 100
        self.center_y = 100
        self.side = False
        self.left_textures = []
        self.right_textures = []
        self.jump = False
        for i in range(6):
            self.left_textures.append(arcade.load_texture(f'go_bill/{i}.gif', flipped_horizontally=True))
            self.right_textures.append(arcade.load_texture(f'go_bill/{i}.gif'))
        self.right_down = arcade.load_texture('bill_textures/BillLayingDown.png')
        self.left_down = arcade.load_texture('bill_textures/BillLayingDown.png', flipped_horizontally=True)

    def set_side(self):
        if self.side:
            self.textures = self.left_textures
        else:
            self.textures = self.right_textures

    def back_left(self):
        if self.left > SCREEN_WIDTH:
            self.center_x = 0
            return True
        return False

    def back_right(self):
        if self.right < 0:
            self.center_x = SCREEN_WIDTH
            return True
        return False

    def to_down(self):
        if self.side:
            self.texture = self.left_down
        else:
            self.texture = self.right_down

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
