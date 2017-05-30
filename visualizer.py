#visualizes character web data based on:
#   absolute importance of character (size)
#   relative importance of characters (line strength, distance)
import pygame, sys
from pygame.locals import *
import math
import numpy as np

#settings for the map

relationshipThreshold = .5 #minimum relationship value to constitude relationship
#maximum and minimum sizes for character circles
circleMax = 200
circleMin = 50
#max and minumum sizes for relation lines
lineMax = 20
lineMin = 2
#max and min distance for character seperation
distMax = 500
distMin = 150

def clip(lo, x, hi):
    return max(lo, min(hi, x))

class Relation:
    def __init__(self, char1, char2, strength):
        self.char1 = char1
        self.char2 = char2
        self.strength = strength

    def draw(self, surface):
        pygame.draw.line(surface, (255, 0, 255), self.char1.position, self.char2.position, clip(lineMin, int(self.strength), lineMax))

class Character:
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength
        self.relations = []
        self.position = (500, 500)
        self.size = self.strength

    def draw(self, surface, font):
        pygame.draw.circle(surface, (0, 255, 255), self.position, clip(circleMin, int(pow(self.strength,.75)), circleMax), 3)
        surface.blit(font.render(self.name, False, (0, 255, 0)), self.position)


datafile = open('web.txt', "r");

characterdata = [] #absolute character strengths - created characters
relationdata = [] #relation strengths between characters - creates connections
relationing = False
for line in datafile: #reading data from text file
    if "RELATIONING" in line: #splits characters and relations data
        relationing = True
    elif not relationing:
	    characterdata.append(line.strip("\n").split(","))
    elif relationing:
        relationdata.append(line.strip("\n").split(","))

characterDict = dict([(c[0], c[1]) for c in characterdata])
characterDict = sorted(characterDict.values())
print(characterDict)
#creating characters
characters = {} #key is name value is character
relations = {}  #key is strength value is relation
for c in characterdata:
    characters[c[0]] = Character(c[0], float(c[1]))

for r in relationdata:
    relations[r[2]] = Relation(characters[r[0]], characters[r[1]], float(r[2]))



pygame.init()
pygame.font.init()
webSurface = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Character Web")

font = pygame.font.SysFont("Comic Sans MS", 30)
#calculating positions for characters
#treat every character like a weight and every connection like a spring
#more important characters are heavier and have longer springs
#more important connections have higher spring constants

#starting with sorted list



while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #drawing everything
    [r.draw(webSurface) for k,r in relations.items()]
    [c.draw(webSurface, font) for k,c in characters.items()]

    pygame.display.update()
