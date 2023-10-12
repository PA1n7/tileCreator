import pygame
from json import loads, dumps

"""
TileMap is the final class that should be created
The parameters for the class are
screen: the screen that you are going to display the tiles
conf: the configuration or map you are going to be using, it can be either:
XXXXX
XXOXX
XXXXX
or
[['X', 'X', 'X', 'X', 'X'], ['X', 'X', 'O', 'X', 'X'], ['X', 'X', 'X', 'X', 'X']]
defs: the equivalence of a character in conf to a color or an image
squareTiles: if set to true then the tiles that appear will be square, as the name indicates
"""

class mapdisturbance(Exception):
    pass

class tiledMap:
    def __init__(self, screen:pygame.Surface, conf, defs, squareTiles = True):
        self.screen = screen
        screen_size = screen.get_size()
        self.img = pygame.display.set_mode(screen_size)
        self.conf = conf
        self.definitions = defs
        #check if definitions is a file
        if type(self.definitions) == str and self.definitions.split(".")[1] in ["txt", "json"]:
            self.definitions = loads(open(self.definitions).read())
        self.convert_conf()
        self.hSize = screen_size[0]/len(self.conf[0])
        self.vSize = screen_size[1]/len(self.conf) if not squareTiles else self.hSize
        self.hSize = int(self.hSize) + 1
        self.vSize = int(self.vSize) + 1
        self.create_map()
    def convert_conf(self):
        if len(self.conf.split("\n")) == 1 and self.conf.split(".")[1] in ["txt", "json"]:
            self.conf = open(self.conf).read()
        if type(self.conf) != list:
            self.conf = [s for s in self.conf.split("\n")]
            _temp = []
            for line in self.conf:
                _temp.append([s for s in line])
            self.conf = _temp
        #Check for no disturbance or change of length across the lines of the file
        #Checking for any dictionary definition missing
        _templength = len(self.conf[0])
        for line in self.conf:
            if _templength != len(line):
                print("Lenght across the conf changes, it shouldn't")
                raise mapdisturbance
            for item in line:
                if item not in list(self.definitions.keys()):
                    print(f"{item} not in the dictionary file")
                    raise mapdisturbance
    def create_map(self):
        for y in range(len(self.conf)):
            for x in range(len(self.conf[0])):
                _tile_rect = (self.hSize*x, self.vSize*y, self.hSize, self.vSize)
                #checking if it's img or file
                item = self.definitions[self.conf[y][x]]
                if type(item) == str:
                    #it is a file here
                    img = pygame.image.load(item).convert_alpha()
                    img = pygame.transform.scale(img, (self.hSize, self.vSize))
                    self.img.blit(img, _tile_rect)
                else:
                    #it is an color here
                    pygame.draw.rect(self.img, item, _tile_rect)
    def draw(self):
        self.create_map()
        self.screen.blit(self.img, ((0, 0), self.screen.get_size()))
    def update(self, conf = None):
        if conf != None:
            self.conf = conf
            self.convert_conf()
            self.img = pygame.display.set_mode(self.screen.get_size())
            self.create_map()