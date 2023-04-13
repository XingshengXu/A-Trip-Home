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
        try:
            image_cache = pg.image.load(CAT_STAND).convert_alpha()
        except Exception as e:
            print(f'Error loading cat stand image: {e}')
        self.cat_stand = pg.transform.scale(
            image_cache, (CAT_WIDTH * 2, CAT_HEIGHT * 2))
        self.cat_stand_rect = self.cat_stand.get_rect(
            center=(WIDTH//2, HEIGHT//2))

        # Cat Walk Image
        self.cat_walk = []
        for i in range(len(CAT_WALK)):
            try:
                image_cache = pg.image.load(CAT_WALK[i]).convert_alpha()
            except Exception as e:
                print(f'Error loading cat walk image: {e}')
            image_cache = pg.transform.scale(
                image_cache, (CAT_WIDTH, CAT_HEIGHT))
            self.cat_walk.append(image_cache)
        self.image = self.cat_walk[self.cat_index]
        self.rect = self.image.get_rect(
            midbottom=(WIDTH // 2, GROUND_HEIGHT))

        # Cat Jump Image and Sound
        self.cat_jump = []
        for i in range(len(CAT_JUMP)):
            try:
                image_cache = pg.image.load(CAT_JUMP[i]).convert_alpha()
            except Exception as e:
                print(f'Error loading cat jump image: {e}')
            image_cache = pg.transform.scale(
                image_cache, (CAT_WIDTH, CAT_HEIGHT))
            self.cat_jump.append(image_cache)
        try:
            self.jump_sound = pg.mixer.Sound(JUMP_SOUND)
        except Exception as e:
            print(f'Error loading jump sound: {e}')

    def jump_state(self):
        for event in pg.event.get():
            if event.type == CORRECT_TYPING and self.rect.bottom >= GROUND_HEIGHT:
                self.cat_index = 0
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
        self.cat_index += 0.2
        if self.rect.bottom < GROUND_HEIGHT:
            if self.cat_index >= len(self.cat_jump):
                self.cat_index = 0
            self.image = self.cat_jump[int(self.cat_index)]
        else:
            if self.cat_index >= len(self.cat_walk):
                self.cat_index = 0
            self.image = self.cat_walk[int(self.cat_index)]

    def update(self):
        self.jump_state()
        self.animation()


class TextTarget(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.letter_count = 0
        self.score = 0
        self.candidate = choice(WORDBANK)
        self.image = TARGET_FONT.render(
            self.candidate, False, 'mediumslateblue')
        self.rect = self.image.get_rect(center=(WIDTH//2, GROUND_HEIGHT//3))

        try:
            self.hit_sound = pg.mixer.Sound(HIT_SOUND)
        except Exception as e:
            print(f'Error loading hit sound: {e}')

    def typing_check(self):
        if self.candidate:
            keys = pg.key.get_pressed()
            letter = self.candidate[0]
            letter_code = ord(letter)
            for key in range(len(keys)):
                if keys[key]:
                    if key == letter_code:
                        self.candidate = self.candidate.replace(letter, '', 1)
                        self.letter_count += 1
                        self.hit_sound.play()
                        self.image = TARGET_FONT.render(
                            self.candidate, False, 'mediumslateblue')
                    else:
                        break
        else:
            pg.event.post(pg.event.Event(CORRECT_TYPING))
            self.score = self.letter_count
            self.candidate = choice(WORDBANK)
            self.image = TARGET_FONT.render(
                self.candidate, False, 'mediumslateblue')
            self.rect = self.image.get_rect(
                center=(WIDTH//2, GROUND_HEIGHT//3))

    def update(self):
        self.typing_check()


class Trees(pg.sprite.Sprite):
    def __init__(self, treeType):
        super().__init__()

        file_path = TREE_TYPE.get(treeType)
        try:
            tree_image = pg.image.load(file_path).convert_alpha()
        except Exception as e:
            print(f'Error loading tree image: {e}')
        if treeType in ['grass_tree1', 'grass_tree2']:
            self.image = tree_image
        else:
            self.image = pg.transform.scale(
                tree_image, (TREE_WIDTH, TREE_HEIGHT))
        self.rect = self.image.get_rect(midbottom=(
            randint(WIDTH, WIDTH * 2), GROUND_HEIGHT))

    def animation(self):
        self.rect.x -= MOVING_SPEED

    def destroy(self):
        if self.rect.x <= -WIDTH:
            self.kill()

    def update(self):
        self.animation()
        self.destroy()


class House(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        try:
            house_image = pg.image.load(HOUSE).convert_alpha()
        except Exception as e:
            print(f'Error loading house image: {e}')
        self.image = pg.transform.scale(
            house_image, (HOUSE_WIDTH, HOUSE_HEIGHT))
        self.rect = self.image.get_rect(midbottom=(
            WIDTH + HOUSE_WIDTH, GROUND_HEIGHT + HOUSE_GROUND_OFFSET))

    def animation(self):
        self.rect.x -= MOVING_SPEED

    def update(self):
        self.animation()


class Game:
    def __init__(self):
        pg.init()
        self.game_active = False
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.flash_counter = 0
        self.current_track = 0
        self.game_name = TITLE_FONT.render('A Trip Home', False, 'white')
        self.game_name_rect = self.game_name.get_rect(
            center=(WIDTH//2, HEIGHT//5))
        self.game_message = TITLE_FONT.render(
            'Press SPACE to play', False, 'white')
        self.game_message_rect = self.game_message.get_rect(
            center=(WIDTH//2, HEIGHT//1.25))
        pg.display.set_caption('A Trip Home')
        try:
            pg.mixer.music.load(PREGAME_MUSIC)
        except Exception as e:
            print(f'Error loading pregame music: {e}')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(loops=-1)

        try:
            self.win_sound = pg.mixer.Sound(WIN_SOUND)
        except Exception as e:
            print(f'Error loading win sound: {e}')

        # Timer
        self.tree_timer = TREE_SPAWN
        self.house_timer = HOUSE_SPAWN
        pg.time.set_timer(self.tree_timer, TREE_SPAWN_FREQ)
        pg.time.set_timer(self.house_timer, HOUSE_SPAWN_FREQ)

        try:
            self.sky_background = pg.image.load(SKY_BACKGROUND).convert()
            self.ground_background = pg.image.load(GROUND_BACKGROUND).convert()
        except Exception as e:
            print(f'Error loading background image: {e}')

        # Background Images Rescale
        self.sky_background = pg.transform.scale(
            self.sky_background, (WIDTH, HEIGHT))
        self.ground_background = pg.transform.scale(
            self.ground_background, (WIDTH, GROUND_WIDTH))

    def display_score(self, score):
        score_text = SCORE_FONT.render(
            f'Score: {score}', False, 'white')
        score_rect = score_text.get_rect(right=WIDTH)
        self.screen.blit(score_text, score_rect)

    def collision(self):
        if collided_houses := pg.sprite.spritecollide(player.sprite, house, False):
            for collided_house in collided_houses:
                if collided_house.rect.centerx <= player.sprite.rect.centerx:
                    self.win_sound.play()
                    pg.time.delay(DELAY_TIME)
                    trees.empty()
                    house.empty()
                    return False
                else:
                    return True
        else:
            return True

    def play_next_music(self):
        try:
            pg.mixer.music.load(INGAME_MUSIC[self.current_track])
        except Exception as e:
            print(f'Error loading imgame music: {e}')
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play()
        pg.mixer.music.set_endevent(NEXT_MUSIC)
        self.current_track = (self.current_track + 1) % len(INGAME_MUSIC)

    def main_loop(self):
        '''This is the game main loop.'''
        while True:
            self.clock.tick(FPS)
            score = text_target.sprite.score
            self.flash_counter += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if self.game_active:
                    if event.type == self.tree_timer:
                        tree_type = choice(list(TREE_TYPE.keys()))
                        trees.add(Trees(tree_type))

                    if event.type == self.house_timer:
                        house.add(House())

                    if event.type == NEXT_MUSIC:
                        self.play_next_music()

                else:
                    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                        self.game_active = True
                        text_target.sprite.score = 0
                        text_target.sprite.letter_count = 0
                        self.flash_counter = 0
                        self.current_track = 0
                        pg.time.set_timer(self.tree_timer, TREE_SPAWN_FREQ)
                        pg.time.set_timer(self.house_timer, HOUSE_SPAWN_FREQ)

                        pg.mixer.music.stop()
                        self.play_next_music()

            if self.game_active:
                self.screen.blit(self.sky_background, (0, 0))
                self.screen.blit(self.ground_background, (0, GROUND_HEIGHT))
                self.display_score(score)
                text_target.draw(self.screen)
                trees.draw(self.screen)
                house.draw(self.screen)
                player.draw(self.screen)

                text_target.update()
                trees.update()
                house.update()
                player.update()

                self.game_active = self.collision()
                if not self.game_active:
                    pg.mixer.music.stop()
                    try:
                        pg.mixer.music.load(PREGAME_MUSIC)
                        pg.mixer.music.set_volume(0.5)
                    except Exception as e:
                        print(f'Error loading pregame music: {e}')
                    pg.mixer.music.play(loops=-1)

            else:
                self.screen.fill('mediumslateblue')
                self.screen.blit(player.sprite.cat_stand,
                                 player.sprite.cat_stand_rect)

                score_message = SCORE_FONT.render(
                    f'Your score: {score}', False, 'white')
                score_message_rect = score_message.get_rect(
                    center=(WIDTH//2, HEIGHT//1.25))
                self.screen.blit(self.game_name, self.game_name_rect)

                if score == 0:
                    if self.flash_counter % FPS < 30:  # Display the message for 30 frames and hide it for the next 30 frames
                        self.screen.blit(self.game_message,
                                         self.game_message_rect)
                else:
                    self.screen.blit(score_message, score_message_rect)
            pg.display.update()


# Run Main Loop
game = Game()

text_target = pg.sprite.GroupSingle()
text_target.add(TextTarget())

player = pg.sprite.GroupSingle()
player.add(Cat())

trees = pg.sprite.Group()

house = pg.sprite.GroupSingle()

game.main_loop()
