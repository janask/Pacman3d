from random import randrange
from math import floor
from copy import copy

class Ghost():

    def __init__(self,m,map,g,pos):
        self.model = m
        self.map = map
        self.game = g
        self.position = pos
        self.initPos = copy(pos)
        self.velocity = [0,0]
        self.rotation = [0,0,0]
        
    def move(self,t):
        if(self.velocity[0]!=0 and self.position[0] != round(self.position[0]) and floor(self.position[0]/3)!=floor(self.position[0]/3+8*self.velocity[0]*t/3)):
            self.position[0] = round(self.position[0])
            if not self.goodDirection():
                self.turn()
        else:
            self.position[0] += 8*self.velocity[0]*t
        if(self.velocity[1]!=0 and self.position[1] != round(self.position[1]) and floor(self.position[1]/3)!=floor(self.position[1]/3+8*self.velocity[1]*t/3)):
            self.position[1] = round(self.position[1])
            if not self.goodDirection():
                self.turn()
        else:
            self.position[1] += 8*self.velocity[1]*t
        if(self.isCrossing(t) or self.velocity[0]==self.velocity[1]):
            self.setDirection()
        self.model.setPos(self.position[0],self.position[1],self.position[2])
        self.model.setHpr(self.rotation[0],self.rotation[1],self.rotation[2])
        
    def isCrossing(self,t):
        if(floor(self.position[1]/3)==self.position[1]/3 and floor(self.position[0]/3)==self.position[0]/3):
            lockedWay=0
            for wall in self.map.walls:
                if (wall[0]==self.position[0] and abs(wall[1]-self.position[1])==3) or (wall[1]==self.position[1] and abs(wall[0]-self.position[0])==3):
                    lockedWay+=1
            return lockedWay<2
        return False
        
    def setDirection(self):
        dir = randrange(4)
        while True:
            self.velocity[0] = dir*2-1 if dir<2 else 0
            self.velocity[1] = dir*2-5 if dir>=2 else 0
            if self.goodDirection():
                break
            dir = (dir+1)%4
        self.rotation[0] = (2*floor((self.velocity[1]-1)/2)+self.velocity[0])*90
        
    def goodDirection(self):
        for wall in self.map.walls:
                if (wall[0]==self.position[0]+self.velocity[0]*3 and wall[1]==self.position[1]+self.velocity[1]*3):
                    return False
        return True
        
    def getPos(self):
        return self.model.getPos()
        
    def turn(self):
        tmp = self.velocity[0]
        self.velocity[0] = self.velocity[1]
        self.velocity[1] = tmp
        if not self.goodDirection():
            self.velocity[0] = -self.velocity[0]
            self.velocity[1] = -self.velocity[1]
        self.rotation[0] = (2*floor((self.velocity[1]-1)/2)+self.velocity[0])*90
        
    def reset(self):
        self.velocity = [0,0]
        self.rotation = [0,0,0]
        self.position = copy(self.initPos)
        self.model.setPos(self.position[0],self.position[1],self.position[2])
        self.model.setHpr(self.rotation[0],self.rotation[1],self.rotation[2])
