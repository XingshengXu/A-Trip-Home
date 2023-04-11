import pygame as pg
pg.init()

"""
The settings module for the "A Trip Home" game. This module contains all the default settings for the gameplay. 
These settings can be easily accessed and used throughout the game by importing the module into the main game file.
"""
# Game Main Settings
WIDTH, HEIGHT = 1600, 900  # Game Window Display
GROUND_WIDTH = 200  # Ground Width
GROUND_HEIGHT = HEIGHT - GROUND_WIDTH  # Ground Height
CAT_WIDTH, CAT_HEIGHT = 162, 141  # Cat Dimension
FPS = 60  # Game FPS
TARGET_FONT = pg.font.Font('assets/font/BubblegumSans.ttf', 150)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game Events
CORRECT_TYPE = pg.USEREVENT + 1


WORDBANK = ["apple", "banana", "cactus", "dolphin", "elephant", "fitness", "guitar", "happiness", "island", "jacket", "kitchen", "lovely", "money", "network", "ocean", "paradise", "question", "romantic", "sunset", "tourist", "universe", "vacation", "wonderful", "xylophone", "yellow", "zebra", "airport", "beautiful", "capital", "dance", "education", "freedom", "government", "hospital", "internet", "journey", "knowledge", "library", "medicine", "natural", "oasis", "peaceful", "quality", "romance", "success", "television", "ultimate", "victory", "wealth", "extraordinary", "friendship", "generous", "hospitality", "imagination", "jubilant", "kindness", "laughter", "miracle", "nature", "optimistic", "passionate", "quest", "romanticism", "satisfied", "triumph", "unbelievable", "vibrant", "wisdom", "xenial", "youthful", "zestful", "adventure", "beauty", "challenge", "dazzling", "excitement", "friendship", "generosity", "honesty", "innovation", "joyful", "kindhearted", "luxury", "music", "optimism", "passion", "quaint", "romance", "satisfaction", "travelling", "understanding", "vitality", "warmth", "xtraordinary", "youthfulness", "zeal", "affection", "blessed", "charming", "delight", "enthusiasm", "fascinating", "generous", "humility", "innovative", "jovial", "kindness", "love", "marvelous", "nourishing", "optimistic", "peace", "quality", "relaxation", "sensual", "thriving", "uplifting", "vibrance",
            "wholesome", "xceptional", "youthful", "zest", "abundance", "blissful", "calmness", "delightful", "exciting", "fantastic", "graceful", "harmony", "inspiration", "jubilation", "kindness", "lovely", "majestic", "nurturing", "oceanic", "pleasure", "quaintness", "rejuvenating", "serenity", "tranquility", "unforgettable", "vibrant", "wondrous", "xeniality", "youthfulness", "zealot", "affectionate", "breathtaking", "charming", "dazzling", "energetic", "flourishing", "glorious", "heavenly", "impressive", "joviality", "knightly", "loveable", "magnificent", "nourished", "oasis", "pleasurable", "quintessential", "refreshing", "spectacular", "thriving", "unforgotten", "vitality", "wondrous", "xpert", "yearning", "zestful", "adoration", "brilliant", "captivating", "delighted", "elegance", "fascinating", "gallant", "heartwarming", "innovative", "jubilant", "knight", "lovely", "mesmerizing", "nourishing", "optimistic", "peaceable", "pleased", "quaint", "relaxing", "satisfied", "tranquil", "unforgettable", "vibrance", "wholesome", "xceptional", "yielding", "zealous", "affectionate", "breathtaking", "charming", "dazzling", "enthusiastic", "flourishing", "glowing", "heavenly", "impressive", "jovial", "kindred", "loving", "mesmerizing", "nourished", "optimism", "peaceful", "pleased", "quaintness", "refreshing", "sensational", "thriving", "unforgotten", "vibrant", "warmhearted", "xpertise", "youthful", "zestful"]
