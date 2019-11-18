from math import pi, sin, cos
from math import radians
from numpy import sign
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import KeyboardButton
from panda3d.core import Filename
from direct.gui.DirectGui import *

class Map():

    def __init__(self, g):
        self.game = g
        x=-45
        y=-45
        self.walls = []
        self.coins = []
        self.passages = []
        self.doors = []
        self.teleports = []
        self.scares = []
        self.ghosts = []
        self.fruits = []
        with open('map.txt', 'r') as mapFile:
            for line in mapFile:
                for element in line:
                    if element == '\n':
                        break
                    if element == '0':
                        m = loader.loadModel(Filename.fromOsSpecific("models/wall.bam"))
                        m.setPos(x,y,0)
                        m.setScale(3,3,3)
                        m.reparentTo(self.game.render)
                        self.walls.append([x,y])
                    elif element == '1':
                        m = loader.loadModel(Filename.fromOsSpecific("models/coin.bam"))
                        m.setPos(x,y,1)
                        m.setScale(3,3,3)
                        m.reparentTo(self.game.render)
                        self.coins.append(m)
                    elif element == '2':
                        self.passages.append([x,y])
                    elif element == '3':
                        m = loader.loadModel(Filename.fromOsSpecific("models/scare.bam"))
                        m.setPos(x,y,1)
                        m.setScale(3,3,3)
                        m.reparentTo(self.game.render)
                        self.scares.append(m)
                    else:
                        pass
                    x += 3
                x = -45
                y += 3
            self.bonus = int(len(self.coins)/3)
    def addFruit(self):
        if self.game.points%self.bonus == 0:
            m = loader.loadModel(Filename.fromOsSpecific("models/fruit.bam"))
            m.setPos(-6,6,1)
            m.setScale(3,3,3)
            m.reparentTo(self.game.render)
            self.fruits.append(m)
            self.game.taskMgr.doMethodLater(10, self.clearFruits, 'clearFruits')
    def clearFruits(self, task):
        for f in self.fruits:
            f.removeNode()
        self.fruits.clear()