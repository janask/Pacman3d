from random import randrange
from math import floor
from copy import copy, deepcopy

class Ghost():

    def __init__(self,m,map,g,pos):
        self.normalModel = m
        self.model = self.normalModel
        self.map = map
        self.game = g
        self.position = pos
        self.initPos = copy(pos)
        self.velocity = [0,0]
        self.rotation = [0,0,0]
        self.alive = True
        self.scared = False
        
    def setScaredModel(self,m):
        self.scaredModel = m
        self.scaredModel.hide()
    
    def move(self,t):
        if(self.velocity[0]!=0 and self.position[0] != round(self.position[0]) and floor(self.position[0]/3)!=floor(self.position[0]/3+8*self.velocity[0]*t/3)):
            self.position[0] = round(self.position[0])
        else:
            self.position[0] += 8*self.velocity[0]*t
        if(self.velocity[1]!=0 and self.position[1] != round(self.position[1]) and floor(self.position[1]/3)!=floor(self.position[1]/3+8*self.velocity[1]*t/3)):
            self.position[1] = round(self.position[1])
        else:
            self.position[1] += 8*self.velocity[1]*t
        if(self.isCrossing(t) or self.velocity[0]==self.velocity[1]):
            self.setDirection()
        elif not self.goodDirection():
            self.turn()
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
        if self.scared:
            self.runAway()
        else:
            self.chase()
        self.rotation[0] = (2*floor((self.velocity[1]-1)/2)+self.velocity[0])*90
    
    def chase(self):
        self.randomDirection()
    
    def randomDirection(self):
        pacmanDir = [self.game.pacman.getPos()[0]-self.position[0],self.game.pacman.getPos()[1]-self.position[1]]
        dir = randrange(4)
        while True:
            self.velocity[0] = dir*2-1 if dir<2 else 0
            self.velocity[1] = dir*2-5 if dir>=2 else 0
            if self.goodDirection():
                break
            dir = (dir+1)%4
    
    def runAway(self):
        pacmanDir = [self.position[0]-self.game.pacman.getPos()[0],self.position[1]-self.game.pacman.getPos()[1]]
        if(floor(self.position[1]/3)==self.position[1]/3 and floor(self.position[0]/3)==self.position[0]/3):
            for dir in self.directionsSorted(pacmanDir):
                self.velocity[0] = dir[0]
                self.velocity[1] = dir[1]
                if self.goodDirection():
                    break
        elif (self.velocity[0]!=0 and pacmanDir[0]/self.velocity[0]<0) or (self.velocity[1]!=0 and pacmanDir[1]/self.velocity[1]<0):
            self.velocity[0] = -self.velocity[0]
            self.velocity[1] = -self.velocity[1]
        
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
        
    def scare(self):
        if self.alive:
            self.scared = True
            self.model.hide()
            self.setDirection()
            self.model = self.scaredModel
            self.model.setPos(self.position[0],self.position[1],self.position[2])
            self.model.setHpr(self.rotation[0],self.rotation[1],self.rotation[2])
            self.model.show()
        
    def unscare(self):
        if self.alive and self.scared:
            self.scared = False
            self.model.hide()
            self.model = self.normalModel
            self.model.setPos(self.position[0],self.position[1],self.position[2])
            self.model.setHpr(self.rotation[0],self.rotation[1],self.rotation[2])
            self.model.show()
        
    def eaten(self):
        self.alive = False
        self.model.hide()
        self.game.taskMgr.doMethodLater(randrange(10)+8, self.resetTask, 'reset')
   
    def resetTask(self,task):
        self.reset()
   
    def reset(self):
        self.alive = True
        self.scared = False
        self.velocity = [0,0]
        self.rotation = [0,0,0]
        self.model = self.normalModel
        self.position = copy(self.initPos)
        self.model.setPos(self.position[0],self.position[1],self.position[2])
        self.model.setHpr(self.rotation[0],self.rotation[1],self.rotation[2])
        self.model.show()
    
    def directionsSorted(self, pacmanDir):
        ans = []
        if pacmanDir[0]==0:
            pacmanDir[0] = randrange(1)-0.5
        if pacmanDir[1]==0:
            pacmanDir[1] = randrange(1)-0.5
        if abs(pacmanDir[0])>abs(pacmanDir[1]):
            ans.append([pacmanDir[0]/abs(pacmanDir[0]),0])
            ans.append([0,pacmanDir[1]/abs(pacmanDir[1])])
            ans.append([0,-pacmanDir[1]/abs(pacmanDir[1])])
            ans.append([-pacmanDir[0]/abs(pacmanDir[0]),0])
        else:
            ans.append([0,pacmanDir[1]/abs(pacmanDir[1])])
            ans.append([pacmanDir[0]/abs(pacmanDir[0]),0])
            ans.append([-pacmanDir[0]/abs(pacmanDir[0]),0])
            ans.append([0,-pacmanDir[1]/abs(pacmanDir[1])])
        ans.append([0,0])
        return ans
            
            


class Blinky(Ghost):
    def chase(self):
        pacmanDir = [self.game.pacman.getPos()[0]-self.position[0],self.game.pacman.getPos()[1]-self.position[1]]
        options = self.directionsSorted(pacmanDir)
        options.remove([-self.velocity[0],-self.velocity[1]])
        for dir in options:
            self.velocity[0] = dir[0]
            self.velocity[1] = dir[1]
            if self.goodDirection():
                break
           
class Inky(Ghost):
    def chase(self):
        pacmanDir = [self.game.pacman.getPos()[0]-self.position[0],self.game.pacman.getPos()[1]-self.position[1]]
        if pacmanDir[0]*pacmanDir[0]+pacmanDir[1]*pacmanDir[1]>500:
            self.randomDirection()
            return
        options = self.directionsSorted(pacmanDir)
        options.remove([-self.velocity[0],-self.velocity[1]])
        for dir in options:
            self.velocity[0] = dir[0]
            self.velocity[1] = dir[1]
            if self.goodDirection():
                break
            
class Pinky(Ghost):
    def chase(self):
        pacmanDir = [self.game.pacman.getPos()[0]-self.position[0],self.game.pacman.getPos()[1]-self.position[1]]
        if pacmanDir[0]*pacmanDir[0]+pacmanDir[1]*pacmanDir[1]>500:
            options = self.directionsSorted(pacmanDir)
            options.remove([-self.velocity[0],-self.velocity[1]])
            for dir in options:
                self.velocity[0] = dir[0]
                self.velocity[1] = dir[1]
                if self.goodDirection():
                    break
        else:
            options = self.directionsSorted([pacmanDir[1],pacmanDir[0]])
            options.remove([-self.velocity[0],-self.velocity[1]])
            for dir in options:
                self.velocity[0] = dir[0]
                self.velocity[1] = dir[1]
                if self.goodDirection():
                    break
            
class Clyde(Ghost):
    def chase(self):
        pacmanDir = [self.game.pacman.getPos()[0]-self.position[0],self.game.pacman.getPos()[1]-self.position[1]]
        if pacmanDir[0]*pacmanDir[0]+pacmanDir[1]*pacmanDir[1]>500:
            options = self.directionsSorted(pacmanDir)
            options.remove([-self.velocity[0],-self.velocity[1]])
            for dir in options:
                self.velocity[0] = dir[0]
                self.velocity[1] = dir[1]
                if self.goodDirection():
                    break
        else:
            self.runAway()

    