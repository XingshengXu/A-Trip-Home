from random import choice, randint, random
from sys import exit
import pygame as pg
from settings import *


class Cat(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gravity = 0
        self.cat_index = 0

        # Cat Stand Image
        try:
            cat_image = pg.image.load(CAT_STAND).convert_alpha()
        except Exception as e:
            print(f'Error loading cat stand image: {e}')
        self.cat_stand = pg.transform.scale(
            cat_image, (CAT_WIDTH * 2, CAT_HEIGHT * 2))
        self.cat_stand_rect = self.cat_stand.get_rect(
            center=(WIDTH//2, HEIGHT//2))

        # Cat Walk Image
        self.cat_walk = []
        for i in range(len(CAT_WALK)):
            try:
                cat_image = pg.image.load(CAT_WALK[i]).convert_alpha()
            except Exception as e:
                print(f'Error loading cat walk image: {e}')
            cat_image = pg.transform.scale(cat_image, (CAT_WIDTH, CAT_HEIGHT))
            self.cat_walk.append(cat_image)
        self.image = self.cat_walk[self.cat_index]
        self.rect = self.image.get_rect(
            midbottom=(WIDTH // 2, GROUND_HEIGHT))

        # Cat Jump Image and Sound
        self.cat_jump = []
        for i in range(len(CAT_JUMP)):
            try:
                cat_image = pg.image.load(CAT_JUMP[i]).convert_alpha()
            except Exception as e:
                print(f'Error loading cat jump image: {e}')
            cat_image = pg.transform.scale(cat_image, (CAT_WIDTH, CAT_HEIGHT))
            self.cat_jump.append(cat_image)
        try:
            self.jump_sound = pg.mixer.Sound(JUMP_SOUND)
        except Exception as e:
            print(f'Error loading jump sound: {e}')

    def jump(self):
        for event in pg.event.get():
            if event.type == CORRECT_TYPING and self.rect.bottom >= GROUND_HEIGHT:
                self.cat_index = 0
                self.gravity = GRAVITY
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
        self.jump()
        self.animation()


class Dog(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.dog_index = 0

        # Dog Run Image
        self.dog_run = []
        for i in range(len(DOG_RUN)):
            try:
                dog_image = pg.image.load(DOG_RUN[i]).convert_alpha()
            except Exception as e:
                print(f'Error loading dog run image: {e}')
            dog_image = pg.transform.scale(dog_image, (DOG_WIDTH, DOG_HEIGHT))
            self.dog_run.append(dog_image)
        self.image = self.dog_run[self.dog_index]
        self.rect = self.image.get_rect(
            midbottom=(WIDTH + DOG_WIDTH, GROUND_HEIGHT))

    def run(self):
        self.rect.x -= MOVING_SPEED * 2

    def animation(self):
        self.dog_index += 0.2
        if self.dog_index >= len(self.dog_run):
            self.dog_index = 0
        self.image = self.dog_run[int(self.dog_index)]

    def update(self):
        self.run()
        self.animation()


class TextTarget(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.letter_count = 0
        self.score = 0
        self.candidate = choice(WORDBANK)
        self.image = TARGET_FONT.render(
            self.candidate, False, 'mediumslateblue')
        self.rect = self.image.get_rect(center=(WIDTH//2, TEXTTARGET_HEIGHT))

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
                center=(WIDTH//2, TEXTTARGET_HEIGHT))

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
        self.cat_dog_collision = False
        self.dog_spawn_probability = EASTEREGG_PROB
        self.game_name = TITLE_FONT.render('A Trip Home', False, 'white')
        self.game_name_rect = self.game_name.get_rect(
            center=(WIDTH//2, GAMENAME_HEIGHT))
        self.game_message = TITLE_FONT.render(
            'Press SPACE to play', False, 'white')
        self.game_message_rect = self.game_message.get_rect(
            center=(WIDTH//2, GAMEMESSAGE_HEIGHT))
        pg.display.set_caption('A Trip Home')

        try:
            self.sky_background = pg.image.load(SKY_BACKGROUND).convert()
            self.ground_background = pg.image.load(GROUND_BACKGROUND).convert()
        except Exception as e:
            print(f'Error loading background image: {e}')

        # Background Images Rescale
        self.sky_background = pg.transform.scale(
            self.sky_background, (WIDTH, HEIGHT))
        self.ground_background = pg.transform.scale(
            self.ground_background, (WIDTH, GROUND_DEPTH))

        try:
            pg.mixer.music.load(PREGAME_MUSIC)
        except Exception as e:
            print(f'Error loading pregame music: {e}')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(loops=-1)

        try:
            self.bark_sound = pg.mixer.Sound(BARK_SOUND)
        except Exception as e:
            print(f'Error loading bark sound: {e}')

        try:
            self.win_sound = pg.mixer.Sound(WIN_SOUND)
        except Exception as e:
            print(f'Error loading win sound: {e}')

        # Timer
        self.tree_timer = TREE_SPAWN
        self.house_timer = HOUSE_SPAWN
        self.dog_timer = DOG_SPAWN
        pg.time.set_timer(self.tree_timer, TREE_SPAWN_FREQ)
        pg.time.set_timer(self.house_timer, HOUSE_SPAWN_FREQ)
        pg.time.set_timer(self.dog_timer, DOG_SPAWN_FREQ)

    def display_score(self, score):
        score_text = SCORE_FONT.render(
            f'Score: {score}', False, 'white')
        score_rect = score_text.get_rect(right=WIDTH)
        self.screen.blit(score_text, score_rect)

    def collision(self):
        if pg.sprite.spritecollide(cat.sprite, dog, False):
            if not self.cat_dog_collision:
                self.bark_sound.play()
                self.cat_dog_collision = True
        else:
            self.cat_dog_collision = False

        if collided_houses := pg.sprite.spritecollide(cat.sprite, house, False):
            for collided_house in collided_houses:
                if collided_house.rect.centerx <= cat.sprite.rect.centerx:
                    self.win_sound.play()
                    pg.time.delay(DELAY_TIME)
                    trees.empty()
                    house.empty()
                    dog.empty()
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
        self.current_track = (self.current_track + 1) % len(INGAME_MUSIC)
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play()
        pg.mixer.music.set_endevent(NEXT_MUSIC)

    def main_loop(self):
        '''This is the game main loop.'''
        while True:
            self.clock.tick(FPS)
            self.flash_counter += 1
            score = text_target.sprite.score
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

                    if event.type == self.dog_timer and random() <= EASTEREGG_PROB:
                        dog.add(Dog())

                    if event.type == NEXT_MUSIC:
                        self.play_next_music()

                else:
                    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                        self.game_active = True
                        self.flash_counter = 0
                        self.current_track = 0
                        text_target.sprite.score = 0
                        text_target.sprite.letter_count = 0
                        pg.time.set_timer(self.tree_timer, TREE_SPAWN_FREQ)
                        pg.time.set_timer(self.house_timer, HOUSE_SPAWN_FREQ)
                        pg.time.set_timer(self.dog_timer, DOG_SPAWN_FREQ)

                        pg.mixer.music.stop()
                        self.play_next_music()

            if self.game_active:
                self.screen.blit(self.sky_background, (0, 0))
                self.screen.blit(self.ground_background, (0, GROUND_HEIGHT))
                self.display_score(score)
                text_target.draw(self.screen)
                trees.draw(self.screen)
                house.draw(self.screen)
                dog.draw(self.screen)
                cat.draw(self.screen)

                text_target.update()
                trees.update()
                house.update()
                dog.update()
                cat.update()

                self.game_active = self.collision()

                if not self.game_active:
                    pg.mixer.music.stop()
                    try:
                        pg.mixer.music.load(PREGAME_MUSIC)
                    except Exception as e:
                        print(f'Error loading pregame music: {e}')
                    pg.mixer.music.set_volume(0.5)
                    pg.mixer.music.play(loops=-1)

            else:
                self.screen.fill('mediumslateblue')
                self.screen.blit(cat.sprite.cat_stand,
                                 cat.sprite.cat_stand_rect)

                score_message = SCORE_FONT.render(
                    f'Your score: {score}', False, 'white')
                score_message_rect = score_message.get_rect(
                    center=(WIDTH//2, SCOREMESSAGE_HEIGHT))
                self.screen.blit(self.game_name, self.game_name_rect)

                if score == 0:
                    # Display the message for 30 frames and hide it for the next 30 frames
                    if self.flash_counter % FPS < 30:
                        self.screen.blit(self.game_message,
                                         self.game_message_rect)
                else:
                    self.screen.blit(score_message, score_message_rect)
            pg.display.update()


# Run Main Loop
game = Game()

text_target = pg.sprite.GroupSingle()
text_target.add(TextTarget())

cat = pg.sprite.GroupSingle()
cat.add(Cat())

trees = pg.sprite.Group()

house = pg.sprite.GroupSingle()

dog = pg.sprite.GroupSingle()

game.main_loop()
