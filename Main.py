import arcade
from constants import *
import bill
import line
import bullet


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg_textures = []
        for i in range(1, 16):
            self.bg_textures.append(arcade.load_texture(f'background/Map{i}.png'))
        self.index_texture = 0
        self.game = True
        self.bill = bill.Bill()
        self.is_walk = False
        self.lines = arcade.SpriteList()
        self.lines_for_level = []
        self.setup()
        self.engine = arcade.PhysicsEnginePlatformer(self.bill, self.lines, GRAVITY)
        self.jumpS = arcade.load_sound("sounds/jump.wav")
        self.bulS = arcade.load_sound("sounds/shoot.wav")
        self.bullets = arcade.SpriteList()

    def setup(self):
        for i in range(0, 801, 100):
            low_line = line.Line()
            low_line.set_position(i, 20)
            self.lines.append(low_line)
        for i, lines in enumerate(COORDS):
            print(lines)
            self.lines_for_level.append([])
            for x, y in lines:
                other_line = line.Line()
                other_line.set_position(x, y)
                self.lines_for_level[i].append(other_line)
        self.append_line(0)

    def append_line(self, side):
        if side:
            for i in range(len(self.lines_for_level[self.index_texture + side])):
                if len(self.lines) > 0:
                    self.lines.pop()
        for new_line in self.lines_for_level[self.index_texture]:
            self.lines.append(new_line)

    def on_draw(self):
        self.clear((255, 255, 255))
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                      self.bg_textures[self.index_texture])
        self.bill.draw()
        self.lines.draw()
        self.bullets.draw()

    def update(self, delta_time):
        if self.game:
            self.bill.update()
            if self.is_walk:
                self.bill.update_animation(delta_time)
            self.lines.update()
            self.engine.update()
            if self.bill.back_left():
                if self.index_texture < len(self.bg_textures)-2:
                    self.index_texture += 1
                    self.append_line(-1)
            elif self.bill.back_right():
                if self.index_texture > 0:
                    self.index_texture -= 1
                    self.append_line(1)
            self.bullets.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.is_walk = True
            self.bill.change_x = -PLAYER_MOVEMENT_SPEED
            self.bill.side = True
            self.bill.set_side()
        if key == arcade.key.D:
            self.is_walk = True
            self.bill.change_x = PLAYER_MOVEMENT_SPEED
            self.bill.side = False
            self.bill.set_side()
        if key == arcade.key.S:
            self.bill.to_down()
        if key == arcade.key.SPACE:
            if self.engine.can_jump():
                self.jumpS.play()
                self.engine.jump(JUMP)
        if key == arcade.key.ENTER:
            self.bulS.play()
            new_bullet = bullet.Bullet(self)
            new_bullet.set_position(self.bill.center_x+10,self.bill.center_y+10)
            self.bullets.append(new_bullet)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or arcade.key.D or arcade.key.S:
            self.bill.change_x = 0
            self.is_walk = False
            self.bill.set_texture(0)


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()
