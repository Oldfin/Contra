import arcade
import animate
from constants import *


class Bill(animate.Animate):
    def __init__(self):
        super().__init__('go_bill/0.gif', scale=SCALING)
        self.center_x = 100
        self.center_y = 100
        for i in range(6):
            self.append_texture(arcade.load_texture(f'go_bill/{i}.gif'))

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
