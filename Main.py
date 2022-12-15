import arcade
from constants import *
import bill
import line
import bullet
import runman
import random
import sniper
import live
import time


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg_textures = []
        for i in range(1, 16):
            self.bg_textures.append(arcade.load_texture(f'background/Map{i}.png'))
        self.index_texture = 0
        self.game = True
        self.bill = bill.Bill(self)
        self.is_walk = False
        self.enemies = arcade.SpriteList()
        self.lines = arcade.SpriteList()
        self.lives = arcade.SpriteList()
        self.game_over = arcade.load_texture('game_over.jpg')
        self.win = False
        self.time_win = time.time()
        self.lines_for_level = []
        self.runmans_for_level = []
        self.runmans_engine = []
        self.snipers_engine = []
        self.snipers_for_level = []
        self.coin_sound = arcade.load_sound('sounds/coin.wav')
        self.snipers = arcade.SpriteList()
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
            self.runmans_for_level.append([])
            for x, y in lines:
                other_line = line.Line()
                other_line.set_position(x, y)
                self.lines_for_level[i].append(other_line)
                new_runman = runman.Runman(self)
                if x == -100:
                    new_runman.set_position(random.randint(50, SCREEN_WIDTH - 50), 100)
                else:
                    new_runman.set_position(x, y+50)
                self.runmans_for_level[i].append(new_runman)
        for i, snipers in enumerate(COORDS_SNIPERS):
            self.snipers_for_level.append([])
            for x, y in snipers:
                new_sniper = sniper.Sniper(self)
                new_sniper.set_position(x, y)
                self.snipers_for_level[i].append(new_sniper)

        self.append_line(0)
        for i in range(self.bill.lives):
            bill_live = live.Live()
            bill_live.set_position(50+40*i, SCREEN_HEIGHT-50)
            self.lives.append(bill_live)

    def append_runman(self, side):
        self.runmans_engine.clear()
        if side:
            for i in range(len(self.runmans_for_level[self.index_texture + side])):
                if len(self.enemies):
                    self.enemies.pop()
        for new_runman in self.runmans_for_level[self.index_texture]:
            self.enemies.append(new_runman)
            self.runmans_engine.append(arcade.PhysicsEnginePlatformer(new_runman, self.lines, GRAVITY))

    def append_sniper(self, side):
        self.snipers_engine.clear()
        if side:
            for i in range(len(self.snipers_for_level[self.index_texture + side])):
                if len(self.snipers):
                    self.snipers.pop()
        for new_sniper in self.snipers_for_level[self.index_texture]:
            self.snipers.append(new_sniper)

    def append_line(self, side):
        self.snipers_bullet = arcade.SpriteList()
        self.append_runman(side)
        self.append_sniper(side)
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
        self.enemies.draw()
        self.snipers.draw()
        self.snipers_bullet.draw()
        self.lives.draw()
        if not self.game and not self.win:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.game_over)
        if self.win and time.time()- self.time_win > 3:
            self.end_game = arcade.load_texture('endgame.png')
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.end_game)
            self.game = False

    def update(self, delta_time):
        if self.game:
            self.bill.update()
            self.snipers_bullet.update()
            if self.is_walk:
                self.bill.update_animation(delta_time)
            self.lines.update()
            self.engine.update()
            if self.bill.back_left():
                if self.index_texture < len(self.bg_textures) - 2:
                    self.index_texture += 1
                    self.append_line(-1)
            elif self.bill.back_right():
                if self.index_texture > 0:
                    self.index_texture -= 1
                    self.append_line(1)
            self.bullets.update()
            self.enemies.update()
            self.enemies.update_animation()
            for runman_engine in self.runmans_engine:
                runman_engine.update()
            self.snipers.update()
            if self.index_texture == len(self.bg_textures) - 2 and not len(self.snipers) and not len(self.enemies):
                self.index_texture += 1
                self.win = True

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
            new_bullet.set_position(self.bill.center_x + 10, self.bill.center_y + 10)
            self.bullets.append(new_bullet)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A or arcade.key.D or arcade.key.S:
            self.bill.change_x = 0
            self.is_walk = False
            self.bill.set_texture(0)


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()
