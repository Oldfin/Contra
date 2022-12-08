import arcade


class Bullet(arcade.Sprite):
    def __init__(self, window):
        super().__init__('bullet.png', 0.03)
        self.window = window
        self.change_x = 25
        if self.window.bill.side:
            self.change_x = -25
        else:
            self.change_x = 25

    def update(self):
        self.center_x += self.change_x
        if abs(self.center_x - self.window.bill.center_x) > 300:
            self.kill()
