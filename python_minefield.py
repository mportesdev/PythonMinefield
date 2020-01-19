import random

import arcade

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Python Minefield'


class FlyingSprite(arcade.Sprite):
    def update(self):
        super().update()


class SpaceShooter(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.mines_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        arcade.set_background_color((20, 20, 40))

        self.player = arcade.Sprite('images/ufo.png')
        self.player.center_y = self.height / 2
        self.player.left = 100

        self.all_sprites.append(self.player)

        arcade.schedule(self.add_mine, 0.3)
        arcade.schedule(self.add_missile, 10)
        arcade.schedule(self.add_cloud, 0.6)

        self.paused = False
        self.dead = False

    def add_mine(self, delta_time: float):
        if self.paused:
            return

        mine = FlyingSprite(random.choice(('images/mine_violet_small.png',
                                           'images/mine_violet.png',
                                           'images/mine_cyan_small.png',
                                           'images/mine_cyan.png')))
        mine.left = self.width
        mine.top = random.randint(mine.height, self.height)
        mine.velocity = (random.randint(-250, -150), random.randint(-20, 20))

        self.mines_list.append(mine)
        self.all_sprites.append(mine)

    def add_missile(self, delta_time: float):
        if self.paused:
            return

        missile = FlyingSprite('images/missile.png')
        missile.left = self.width
        missile.center_y = self.player.center_y
        missile.velocity = (-400, 0)

        self.mines_list.append(missile)
        self.all_sprites.append(missile)

    def add_cloud(self, delta_time: float):
        if self.paused:
            return

        cloud = FlyingSprite(random.choice(('images/cloud_violet.png',
                                            'images/cloud_violet_small.png',
                                            'images/cloud_cyan.png',
                                            'images/cloud_cyan_small.png',)))
        cloud.left = self.width
        cloud.top = random.randint(cloud.height, self.height)
        cloud.velocity = (random.randint(-100, -20), 0)

        self.clouds_list.append(cloud)
        self.all_sprites.append(cloud)

    def on_draw(self):
        arcade.start_render()
        self.all_sprites.draw()

    def on_update(self, delta_time: float):
        if self.paused:
            return

        if self.dead:
            try:
                self.player.alpha -= 3
            except OverflowError:
                arcade.close_window()

        if self.player.collides_with_list(self.mines_list):
            self.dead = True

        for s in self.all_sprites:
            s.center_x += s.change_x * delta_time
            s.center_y += s.change_y * delta_time
            if s.right < 0:
                s.remove_from_sprite_lists()

        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.Q:
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol in (arcade.key.I, arcade.key.UP):
            self.player.change_y = 200

        if symbol in (arcade.key.K, arcade.key.DOWN):
            self.player.change_y = -200

        if symbol in (arcade.key.J, arcade.key.LEFT):
            self.player.change_x = -200

        if symbol in (arcade.key.L, arcade.key.RIGHT):
            self.player.change_x = 200

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in (arcade.key.I, arcade.key.K,
                      arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0

        if symbol in (arcade.key.J, arcade.key.L,
                      arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0


if __name__ == '__main__':
    app = SpaceShooter(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    app.setup()
    arcade.run()
