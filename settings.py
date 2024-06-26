import pygame as pg
pg.init()

"""
The settings module for the "A Trip Home" game. This module contains all the default settings for the gameplay. 
These settings can be easily accessed and used throughout the game by importing the module into the main game file.
"""

# Game Dimensions
WIDTH, HEIGHT = 1600, 900  # Game Window Display Dimensions
GROUND_DEPTH = 200  # Ground Depth
GROUND_HEIGHT = HEIGHT - GROUND_DEPTH  # Ground Height
GAMENAME_HEIGHT = HEIGHT // 5  # Game Name Height
GAMEMESSAGE_HEIGHT = HEIGHT // 1.25  # Game Message Height
TEXTTARGET_HEIGHT = GROUND_HEIGHT // 3  # Text Target Height
SCOREMESSAGE_HEIGHT = HEIGHT//1.25  # Score Message Height
CAT_WIDTH, CAT_HEIGHT = 162, 141  # Cat Dimensions
DOG_WIDTH, DOG_HEIGHT = 162, 141  # Dog Dimensions
TREE_WIDTH, TREE_HEIGHT = 264, 333  # Tree Dimensions
HOUSE_WIDTH, HOUSE_HEIGHT = 300, 340  # House Dimensions
HOUSE_GROUND_OFFSET = 20  # House Ground Offset

# FPS, Gravity, and Moving Speed
FPS = 60
GRAVITY = -20
MOVING_SPEED = 3

# Font
TARGET_FONT = pg.font.Font('assets/font/BubblegumSans.ttf', 150)
SCORE_FONT = pg.font.Font('assets/font/Purrfect.ttf', 100)
TITLE_FONT = pg.font.Font('assets/font/KittenSwash.ttf', 100)

# Spawn Frequence and Delay Time
TREE_SPAWN_FREQ = 3000
HOUSE_SPAWN_FREQ = 300000
DOG_SPAWN_FREQ = 30000
DELAY_TIME = 3000
EASTEREGG_PROB = 0.06

# Game Events
CORRECT_TYPING = pg.USEREVENT + 1
TREE_SPAWN = pg.USEREVENT + 2
HOUSE_SPAWN = pg.USEREVENT + 3
DOG_SPAWN = pg.USEREVENT + 4
NEXT_MUSIC = pg.USEREVENT + 5

# Image Path
SKY_BACKGROUND = 'assets/background/sky.png'
GROUND_BACKGROUND = 'assets/background/ground.png'
HOUSE = 'assets/house/home.png'
CAT_STAND = 'assets/cat/Stand.png'
CAT_WALK = ['assets/cat/Walk1.png', 'assets/cat/Walk2.png', 'assets/cat/Walk3.png', 'assets/cat/Walk4.png', 'assets/cat/Walk5.png',
            'assets/cat/Walk6.png', 'assets/cat/Walk7.png', 'assets/cat/Walk8.png', 'assets/cat/Walk9.png', 'assets/cat/Walk10.png']

CAT_JUMP = ['assets/cat/Jump1.png', 'assets/cat/Jump2.png', 'assets/cat/Jump3.png', 'assets/cat/Jump4.png',
            'assets/cat/Jump5.png', 'assets/cat/Jump6.png', 'assets/cat/Jump7.png', 'assets/cat/Jump8.png']

DOG_RUN = ['assets/dog/Run1.png', 'assets/dog/Run2.png', 'assets/dog/Run3.png', 'assets/dog/Run4.png',
           'assets/dog/Run5.png', 'assets/dog/Run6.png', 'assets/dog/Run7.png', 'assets/dog/Run8.png']

TREE_TYPE = {
    'common_tree': 'assets\plants\common_tree.png',
    'cypress_tree1': 'assets\plants\cypress_tree1.png',
    'cypress_tree2': 'assets\plants\cypress_tree2.png',
    'grass_tree1': 'assets\plants\grass_tree1.png',
    'grass_tree2': 'assets\plants\grass_tree2.png'
}

# Sound Path
JUMP_SOUND = 'assets/sound effect/Meow.ogg'
HIT_SOUND = 'assets/sound effect/hit.wav'
WIN_SOUND = 'assets/sound effect/win.ogg'
BARK_SOUND = 'assets/sound effect/dog_barking.wav'

# Music Path
PREGAME_MUSIC = 'assets/music/GrayTrip.mp3'
INGAME_MUSIC = ['assets/music/HappyTune.mp3',
                'assets/music/TakeATrip.ogg', 'assets/music/TownTheme.mp3']

# Word Bank
WORDBANK = ["apple", "banana", "cactus", "dolphin", "elephant", "fitness", "guitar", "happiness", "island", "jacket", "kitchen", "lovely", "money", "network", "ocean", "paradise", "question", "romantic", "sunset", "tourist", "universe", "vacation", "wonderful", "xylophone", "yellow", "zebra", "airport", "beautiful", "capital", "dance", "education", "freedom", "government", "hospital", "internet", "journey", "knowledge", "library", "medicine", "natural", "oasis", "peaceful", "quality", "romance", "success", "television", "ultimate", "victory", "wealth", "extraordinary", "friendship", "generous", "hospitality", "imagination", "jubilant", "kindness", "laughter", "miracle", "nature", "optimistic", "passionate", "quest", "romanticism", "satisfied", "triumph", "unbelievable", "vibrant", "wisdom", "xenial", "youthful", "zestful", "adventure", "beauty", "challenge", "dazzling", "excitement", "friendship", "generosity", "honesty", "innovation", "joyful", "kindhearted", "luxury", "music", "optimism", "passion", "quaint", "romance", "satisfaction", "travelling", "understanding", "vitality", "warmth", "xtraordinary", "youthfulness", "zeal", "affection", "blessed", "charming", "delight", "enthusiasm", "fascinating", "generous", "humility", "innovative", "jovial", "kindness", "love", "marvelous", "nourishing", "optimistic", "peace", "quality", "relaxation", "sensual", "thriving", "uplifting", "vibrance",
            "wholesome", "xceptional", "youthful", "zest", "abundance", "blissful", "calmness", "delightful", "exciting", "fantastic", "graceful", "harmony", "inspiration", "jubilation", "kindness", "lovely", "majestic", "nurturing", "oceanic", "pleasure", "quaintness", "rejuvenating", "serenity", "tranquility", "unforgettable", "vibrant", "wondrous", "xeniality", "youthfulness", "zealot", "affectionate", "breathtaking", "charming", "dazzling", "energetic", "flourishing", "glorious", "heavenly", "impressive", "joviality", "knightly", "loveable", "magnificent", "nourished", "oasis", "pleasurable", "quintessential", "refreshing", "spectacular", "thriving", "unforgotten", "vitality", "wondrous", "xpert", "yearning", "zestful", "adoration", "brilliant", "captivating", "delighted", "elegance", "fascinating", "gallant", "heartwarming", "innovative", "jubilant", "knight", "lovely", "mesmerizing", "nourishing", "optimistic", "peaceable", "pleased", "quaint", "relaxing", "satisfied", "tranquil", "unforgettable", "vibrance", "wholesome", "xceptional", "yielding", "zealous", "affectionate", "breathtaking", "charming", "dazzling", "enthusiastic", "flourishing", "glowing", "heavenly", "impressive", "jovial", "kindred", "loving", "mesmerizing", "nourished", "optimism", "peaceful", "pleased", "quaintness", "refreshing", "sensational", "thriving", "unforgotten", "vibrant", "warmhearted", "xpertise", "youthful", "zestful"]
