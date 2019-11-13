from math import pi, sin, cos
from math import radians
from numpy import sign
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import KeyboardButton
from panda3d.core import Filename
 
class MyApp(ShowBase):

    position = [0,6,1.5]
    rotation = [0,0,0]
    
    def __init__(self):
        ShowBase.__init__(self)
 
        # Load the environment model.
        self.scene = self.loader.loadModel(Filename.fromOsSpecific("models/scene.bam"))
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(2.89,2.89,3)
        self.scene.setPos(0, 0, 1.5)
 
        # Add the moveTask procedure to the task manager.
        self.taskMgr.add(self.moveTask, "MoveTask")

        self.loadMap()
        self.cameraMode=True

        self.pacman = loader.loadModel(Filename.fromOsSpecific("models/pacman.bam"))
        self.pacman.setPos(self.position[0],self.position[1],self.position[2])
        self.pacman.setScale(3,3,3)
        self.pacman.reparentTo(self.render)
        
    def moveTask(self, task):
     
        # Check if the player is holding W or S
        is_down = base.mouseWatcherNode.is_button_down
     
        if is_down(KeyboardButton.up()):
            move = [-0.2*sin(radians(self.rotation[0])),0.2*cos(radians(self.rotation[0]))]
            for wall in self.walls:
                if (abs(wall[1]-self.position[1]-move[1])<2.6) and (abs(wall[0]-self.position[0]-move[0])<2.6):
                    if (round(abs(wall[1]-self.position[1]),1)<2.6 and sign(wall[0]-self.position[0])==sign(move[0])):
                        move[0] = wall[0]-self.position[0]-2.6*sign(move[0])
                    if (round(abs(wall[0]-self.position[0]),1)<2.6 and sign(wall[1]-self.position[1])==sign(move[1])):
                        move[1] = wall[1]-self.position[1]-2.6*sign(move[1])
            self.position[1] = self.position[1]+move[1]
            self.position[0] = self.position[0]+move[0]
        if is_down(KeyboardButton.down()):
            move = [0.1*sin(radians(self.rotation[0])),-0.1*cos(radians(self.rotation[0]))]
            for wall in self.walls:
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
        if is_down(KeyboardButton.left()):
            self.rotation[0] = (self.rotation[0]+3)%360
        if is_down(KeyboardButton.right()):
            self.rotation[0] = (self.rotation[0]-3)%360
        if is_down(KeyboardButton.asciiKey('o')):
            self.cameraMode= False
        if is_down(KeyboardButton.asciiKey('i')):
            self.cameraMode= True

        self.pacman.setPos(self.position[0],self.position[1],self.position[2])
        self.pacman.setHpr(self.rotation[0],self.rotation[1],self.rotation[2])
        if(self.cameraMode):
            self.camera.setPos(self.position[0],self.position[1],self.position[2])
            self.camera.setHpr(self.rotation[0],self.rotation[1],self.rotation[2])
        else:
            self.camera.setPos(0,0,180)
            self.camera.setHpr(0,-90,0)
        return Task.cont

    def loadMap(self):
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
                        m.reparentTo(self.render)
                        self.walls.append([x,y])
                    elif element == '1':
                        m = loader.loadModel(Filename.fromOsSpecific("models/coin.bam"))
                        m.setPos(x,y,0.3)
                        m.setScale(3,3,3)
                        m.reparentTo(self.render)
                        self.coins.append([x,y])
                    elif element == '2':
                        self.passages.append([x,y])
                    elif element == '3':
                        m = loader.loadModel(Filename.fromOsSpecific("models/scare.bam"))
                        m.setPos(x,y,0.3)
                        m.setScale(3,3,3)
                        m.reparentTo(self.render)
                        self.scares.append([x,y])
                    elif element == '4':
                        m = loader.loadModel(Filename.fromOsSpecific("models/fruit.bam"))
                        m.setPos(x,y,0.3)
                        m.setScale(3,3,3)
                        m.reparentTo(self.render)
                        self.fruits.append([x,y])
                    else:
                        pass
                    x += 3
                x = -45
                y += 3
        print(self.walls)
 
 
app = MyApp()
app.run()
