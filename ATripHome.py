from sys import exit
import pygame as pg
from random import randint, choice
from settings import *


class Cat(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gravity = 0
        self.cat_index = 0
        # Cat Stand Image
        self.cat_stand = pg.image.load('assets/cat/Stand.png').convert_alpha()
        self.cat_stand = pg.transform.scale(
            self.cat_stand, (CAT_WIDTH, CAT_HEIGHT))
        self.image = self.cat_stand
        self.rect = self.image.get_rect(
            midbottom=(WIDTH // 2, GROUND_HEIGHT))

        # Cat Jump Image and Sound
        self.cat_jump = []
        for i in range(1, 9):
            image_cache = pg.image.load(
                f'assets/cat/Jump{i}.png').convert_alpha()
            image_cache = pg.transform.scale(
                image_cache, (CAT_WIDTH, CAT_HEIGHT))
            self.cat_jump.append(image_cache)

        self.jump_sound = pg.mixer.Sound('assets/sound effect/Meow.ogg')

    def jump_state(self):
        for event in pg.event.get():
            if event.type == CORRECT_TYPE and self.rect.bottom >= GROUND_HEIGHT:
                self.gravity = -20
                self.rect.y += self.gravity
                self.jump_sound.play()
                return

        if self.rect.bottom < GROUND_HEIGHT:
            self.gravity += 1
        else:
            self.gravity = 0
            self.rect.bottom = GROUND_HEIGHT
        self.rect.y += self.gravity

    def animation(self):
        if self.rect.bottom < GROUND_HEIGHT:
            self.cat_index += 0.2
            if self.cat_index >= len(self.cat_jump):
                self.cat_index = 0
            self.image = self.cat_jump[int(self.cat_index)]
        else:
            self.image = self.cat_stand

    def update(self):
        self.jump_state()
        self.animation()


class TextTarget(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.letter_count = 0
        self.candidate = choice(WORDBANK)
        self.image = TARGET_FONT.render(self.candidate, False, (0, 0, 0))
        self.rect = self.image.get_rect(center=(WIDTH//2, GROUND_HEIGHT//3))

        self.hit_sound = pg.mixer.Sound('assets/sound effect/hit.wav')

    def type_check(self):
        if self.candidate:
            keys = pg.key.get_pressed()
            letter = self.candidate[self.letter_count]
            letter_code = ord(letter)
            for key in range(len(keys)):
                if keys[key]:
                    if key == letter_code:
                        self.candidate = self.candidate.replace(letter, '', 1)
                        self.hit_sound.play()
                        self.image = TARGET_FONT.render(
                            self.candidate, False, (0, 0, 0))
                    else:
                        break
        else:
            pg.event.post(pg.event.Event(CORRECT_TYPE))
            self.letter_count = 0
            self.candidate = choice(WORDBANK)
            self.image = TARGET_FONT.render(self.candidate, False, (0, 0, 0))
            self.rect = self.image.get_rect(
                center=(WIDTH//2, GROUND_HEIGHT//3))

    def update(self):
        self.type_check()


class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('A Trip Home')

        try:
            self.sky_background = pg.image.load(
                'assets/background/sky.png').convert()
            self.ground_background = pg.image.load(
                'assets/background/ground.png').convert()
        except pg.error:
            print('Error loading background image!')

        # Background Images Rescale
        self.sky_background = pg.transform.scale(
            self.sky_background, (WIDTH, HEIGHT))
        self.ground_background = pg.transform.scale(
            self.ground_background, (WIDTH, GROUND_WIDTH))

    def main_loop(self):
        '''This is the game main loop.'''
        while True:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            self.screen.blit(self.sky_background, (0, 0))
            self.screen.blit(self.ground_background,
                             (0, GROUND_HEIGHT))

            text_target.draw(self.screen)
            player.draw(self.screen)

            text_target.update()
            player.update()

            pg.display.update()


# Run Main Loop

game = Game()

text_target = pg.sprite.GroupSingle()
text_target.add(TextTarget())

player = pg.sprite.GroupSingle()
player.add(Cat())

game.main_loop()
