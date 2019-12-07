from math import pi, sin, cos
from math import radians
from numpy import sign
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import KeyboardButton
from panda3d.core import Filename
from direct.gui.DirectGui import *

class Pacman():
    position = [0,21,1.5]
    rotation = [0,0,0]
    
    def __init__(self, m, map, g):
        self.model = m
        self.map = map
        self.game = g
        self.alive = True
    
    def moveForward(self, t):
        move = [-10*t*sin(radians(self.rotation[0])),10*t*cos(radians(self.rotation[0]))]
        for wall in self.map.walls:
            if (abs(wall[1]-self.position[1]-move[1])<2.6) and (abs(wall[0]-self.position[0]-move[0])<2.6):
                if (round(abs(wall[1]-self.position[1]),1)<2.6 and sign(wall[0]-self.position[0])==sign(move[0])):
                    move[0] = wall[0]-self.position[0]-2.6*sign(move[0])
                if (round(abs(wall[0]-self.position[0]),1)<2.6 and sign(wall[1]-self.position[1])==sign(move[1])):
                    move[1] = wall[1]-self.position[1]-2.6*sign(move[1])
        self.position[1] = self.position[1]+move[1]
        self.position[0] = self.position[0]+move[0]
        self.model.setPos(self.position[0],self.position[1],self.position[2])
        self.model.setHpr(self.rotation[0],self.rotation[1],self.rotation[2])
        self.check()
        
    def moveBack(self, t):
        move = [5*t*sin(radians(self.rotation[0])),-5*t*cos(radians(self.rotation[0]))]
        for wall in self.map.walls:
            if (abs(wall[1]-self.position[1]-move[1])<2.6) and (abs(wall[0]-self.position[0]-move[0])<2.6):
                if (round(abs(wall[1]-self.position[1]),1)<2.6):
                    move[0] = wall[0]-self.position[0]-2.6*sign(move[0])
                if (round(abs(wall[0]-self.position[0]),1)<2.6):
                    move[1] = wall[1]-self.position[1]-2.6*sign(move[1])
                if(round(abs(wall[1]-self.position[1]),1)>=2.6 and round(abs(wall[0]-self.position[0]),1)>=2.6):
                    tmp = min(abs(move[0]-wall[0]+self.position[0]+2.6*sign(move[0])),abs(move[1]-wall[1]+self.position[1]+2.6*sign(move[1])))
                    move[0] -= tmp*sign(move[0])
                    move[1] -= tmp*sign(move[1])
        self.position[1] = self.position[1]+move[1]
        self.position[0] = self.position[0]+move[0]
        self.model.setPos(self.position[0],self.position[1],self.position[2])
        self.model.setHpr(self.rotation[0],self.rotation[1],self.rotation[2])
        self.check()
        
    def turnRight(self, t):
        self.rotation[0] = (self.rotation[0]-100*t)%360
        self.model.setPos(self.position[0],self.position[1],self.position[2])
        self.model.setHpr(self.rotation[0],self.rotation[1],self.rotation[2])
        
    def turnLeft(self, t):
        self.rotation[0] = (self.rotation[0]+100*t)%360
        self.model.setPos(self.position[0],self.position[1],self.position[2])
        self.model.setHpr(self.rotation[0],self.rotation[1],self.rotation[2])
    def check(self):
        pacmanPos = self.model.getPos()
        for coin in self.map.coins:
            if abs(coin.getPos()[0]- pacmanPos[0])<2.5 and abs(coin.getPos()[1]- pacmanPos[1])<2.5 and abs(coin.getPos()[1]- pacmanPos[1])<2.5 :
                coin.removeNode()
                self.map.coins.remove(coin)
                self.game.points += 10
                self.map.addFruit()
                break
        for fruit in self.map.fruits:
            if abs(fruit.getPos()[0]- pacmanPos[0])<2.5 and abs(fruit.getPos()[1]- pacmanPos[1])<2.5 and abs(fruit.getPos()[1]- pacmanPos[1])<2.5 :
                fruit.removeNode()
                self.map.fruits.remove(fruit)
                self.game.points += 100
        for scare in self.map.scares:
            if abs(scare.getPos()[0]- pacmanPos[0])<2.5 and abs(scare.getPos()[1]- pacmanPos[1])<2.5 and abs(scare.getPos()[1]- pacmanPos[1])<2.5 :
                scare.removeNode()
                self.map.scares.remove(scare)
                self.game.points += 10
                self.game.startScare()
        self.checkGhosts()
    
    def checkGhosts(self):
        pacmanPos = self.model.getPos()
        for ghost in self.game.ghosts:
            if (ghost.getPos()[0]- pacmanPos[0])*(ghost.getPos()[0]- pacmanPos[0])+(ghost.getPos()[1]- pacmanPos[1])*(ghost.getPos()[1]- pacmanPos[1])<2.5 :
                if self.game.scareMode and ghost.alive:
                    ghost.eaten()
                    self.game.points += self.game.ghostPts
                    self.game.ghostPts*=2
                elif ghost.alive:
                    self.alive = False
                    self.rotation[1]=180
                    self.model.setHpr(self.rotation[0],self.rotation[1],self.rotation[2])
    
    def getPos(self):
        return self.model.getPos()
    
    def reset(self):
        self.position = [0,21,1.5]
        self.rotation = [0,0,0]
        self.model.setPos(self.position[0],self.position[1],self.position[2])
        self.model.setHpr(self.rotation[0],self.rotation[1],self.rotation[2])
        self.alive = True
