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
circleMax = 150
circleMin = 30
#max and minumum sizes for relation lines
lineMax = 20
lineMin = 2
#max and min distance for character seperation
distMax = 500
distMin = 100
#max and min relational values
relMax = 100
relMin = 0

def clip(lo, x, hi):
    return max(lo, min(hi, x))

class Relation:
    def __init__(self, char1, char2, strength):
        self.char1 = char1
        self.char2 = char2
        self.strength = strength
        self.thickness = 5

    def draw(self, surface):
        pygame.draw.line(surface, (255, 0, 255), self.char1.position, self.char2.position, clip(lineMin, int(self.thickness), lineMax))

class Character:
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength
        self.relations = []
        self.position = (1000, 500)
        self.size = self.strength

    def draw(self, surface, font):
        pygame.draw.circle(surface, (0, 255, 255), self.position, clip(circleMin, int(self.strength), circleMax), 3)
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

characterDict = dict([(c[0], float(c[1])) for c in characterdata])
characterDict = sorted(characterDict, key=characterDict.get, reverse = True)
#creating characters
characters = {} #key is name value is character
relations = {}  #key is strength value is relation
for c in characterdata:
    characters[c[0]] = Character(c[0], np.log(float(c[1])+1))

for r in relationdata:
    relations[r[2]] = Relation(characters[r[0]], characters[r[1]], np.log(float(r[2])+1))

[print(v.strength) for c,v in characters.items()]

pygame.init()
pygame.font.init()
webSurface = pygame.display.set_mode((1900, 1000))
pygame.display.set_caption("Character Web")

font = pygame.font.SysFont("Comic Sans MS", 30)
#calculating positions for characters
#treat every character like a weight and every connection like a spring
#more important characters are heavier and have longer springs
#more important connections have higher spring constants

#first we normalize all of the values so they aren't too crazy different
maxAbsolute = max([v.strength for v in characters.values()])
absMaxRatio = circleMax/maxAbsolute #scaling so most important character is max size
for v in characters.values():
    v.strength *= absMaxRatio

maxRelative = max([v.strength for v in relations.values()])
relMaxRatio = relMax/maxRelative
relThickRatio = relMax/lineMax
for v in relations.values():
    v.strength *= relMaxRatio
    v.thickness = v.strength/relThickRatio + lineMin


#using character dict, the sorted array of characters by absolute imporatance
#uniformly distribute everything in circle around main character to start at max distance
delta = (2*3.1415)/(len(characterDict)-1)
theta = 0
anchor = characters[characterDict[0]].position
for n in characterDict:
    if n != characterDict[0]:
        characters[n].position = (int(math.sin(theta)*distMax)+anchor[0], int(math.cos(theta)*distMax)+anchor[1])
        theta += delta


#for it in range(len(characters))
adjusting = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #drawing everything
    while adjusting:
        for c in characters:
            if name != characterDict[0]: #most important character is anchored
                for r in c.relations:
                    pass

    [r.draw(webSurface) for k,r in relations.items()]
    [c.draw(webSurface, font) for k,c in characters.items()]

    pygame.display.update()
