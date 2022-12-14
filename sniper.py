import arcade
import time
import bullet


class Sniper(arcade.Sprite):
    def __init__(self, window):
        super().__init__('sniper/sniper_forward.png', 1)
        self.lives = 3
        self.window = window
        self.sniper_left = arcade.load_texture('sniper/sniper_forward.png')
        self.sniper_right = arcade.load_texture('sniper/sniper_forward.png', flipped_horizontally=True)
        self.sniper_left_angle = arcade.load_texture('sniper/sniper_angle.png')
        self.sniper_right_angle = arcade.load_texture('sniper/sniper_angle.png', flipped_horizontally=True)
        self.last_reloading = time.time()

    def shot (self, direction_x, direction_y):
        if time.time() - self.last_reloading > 3:
            x = self.center_x
            y = self.center_y
            new_bullet = bullet.SniperBullet(self.window, direction_x, direction_y, x , y)
            self.window.snipers_bullet.append(new_bullet)
            self.last_reloading = time.time()

    def update(self):
        if self.window.bill.center_y < self.center_y:
            if self.window.bill.center_x < self.center_x:
                self.texture = self.sniper_left_angle
                self.shot(-10, -10)
            else:
                self.texture = self.sniper_right_angle
                self.shot(10, -10)
        else:
            if self.window.bill.center_x < self.center_x:
                self.texture = self.sniper_left
                self.shot(-10, 0)
            else:
                self.texture = self.sniper_right
                self.shot(10, 0)
        if self.lives <= 0:
            self.kill()

