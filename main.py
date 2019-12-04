from math import pi, sin, cos
from math import radians
from numpy import sign
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import KeyboardButton
from panda3d.core import Filename
from direct.gui.DirectGui import *

from Pacman import Pacman
from Map import Map
from Ghost import Ghost, Blinky, Pinky, Inky, Clyde
 
class MyApp(ShowBase):

    points = 0
    level = 1
    lives = 3
    
    def __init__(self):
        ShowBase.__init__(self)

        #Load state bar
        self.gameState = DirectFrame(frameSize=(-base.getAspectRatio(),base.getAspectRatio(),0.8,1),frameColor=(0,0,1,1))
        self.pointsLabel = DirectLabel(frameColor=(0,0,0,0),text="Points: "+str(self.points), scale=(0.1,0.1,0.1), pos=(-base.getAspectRatio()*0.8,0,0.9))
        self.levelLabel = DirectLabel(frameColor=(0,0,0,0),text="LEVEL "+str(self.level), scale=(0.1,0.1,0.1), pos=(0,0,0.9))
        self.livesLabel = DirectLabel(frameColor=(0,0,0,0),text="Lives: "+str(self.lives), scale=(0.1,0.1,0.1), pos=(base.getAspectRatio()*0.8,0,0.9))
 
        #Load scene
        self.scene = self.loader.loadModel(Filename.fromOsSpecific("models/scene.bam"))
        self.scene.reparentTo(self.render)
        self.scene.setScale(2.89,2.89,3)
        self.scene.setPos(0, 0, 1.5)
 
        # Add tasks to the task manager.
        self.taskMgr.add(self.moveTask, "MoveTask")
        self.accept("aspectRatioChanged", self.ratioChanged)

        self.map = Map(self)
        self.cameraMode=2
        self.pause = False
        self.scareMode = False
        self.ghostPts = 200

        #Ghosts
        self.ghosts = []
        g = loader.loadModel(Filename.fromOsSpecific("models/blinky.bam"))
        g.setScale(1.5,1.5,1.5)
        g.reparentTo(self.render)
        self.ghosts.append(Blinky(g,self.map,self,[0,0,1.5]))
        g = loader.loadModel(Filename.fromOsSpecific("models/pinky.bam"))
        g.setScale(1.5,1.5,1.5)
        g.reparentTo(self.render)
        self.ghosts.append(Pinky(g,self.map,self,[0,-3,1.5]))
        g = loader.loadModel(Filename.fromOsSpecific("models/inky.bam"))
        g.setScale(1.5,1.5,1.5)
        g.reparentTo(self.render)
        self.ghosts.append(Inky(g,self.map,self,[-9,-3,1.5]))
        g = loader.loadModel(Filename.fromOsSpecific("models/clyde.bam"))
        g.setScale(1.5,1.5,1.5)
        g.reparentTo(self.render)
        self.ghosts.append(Clyde(g,self.map,self,[-9,-3,1.5]))
        for i in range(len(self.ghosts)):
            g = loader.loadModel(Filename.fromOsSpecific("models/scared.bam"))
            g.setScale(1.5,1.5,1.5)
            g.reparentTo(self.render)
            self.ghosts[i].setScaredModel(g)

        #Pacman
        m = loader.loadModel(Filename.fromOsSpecific("models/pacman.bam"))
        self.pacman = Pacman(m, self.map, self)
        m.setPos(self.pacman.position[0],self.pacman.position[1],self.pacman.position[2])
        m.setScale(3,3,3)
        m.reparentTo(self.render)

        self.timer = globalClock.getFrameTime()
        
    def moveTask(self, task):
     
        is_down = base.mouseWatcherNode.is_button_down
        dt = globalClock.getFrameTime()
        dt = dt - self.timer
        self.timer = dt + self.timer
        
        if not self.pause:
     
            if is_down(KeyboardButton.up()):
                self.pacman.moveForward(dt)
            if is_down(KeyboardButton.down()):
                self.pacman.moveBack(dt)
            if is_down(KeyboardButton.left()):
                self.pacman.turnLeft(dt)
            if is_down(KeyboardButton.right()):
                self.pacman.turnRight(dt)
            if is_down(KeyboardButton.asciiKey(b"1")):
                self.cameraMode= 1
            if is_down(KeyboardButton.asciiKey(b'2')):
                self.cameraMode= 2
            if is_down(KeyboardButton.asciiKey(b'3')):
                self.cameraMode= 3
            self.pacman.checkGhosts()
            
            for g in self.ghosts:
                g.move(dt)
        
        self.pointsLabel.setText("Points: "+str(self.points))
        self.livesLabel.setText("Lives: "+str(self.lives))
        
        if self.cameraMode==1:
            self.camera.setPos(self.pacman.position[0],self.pacman.position[1],self.pacman.position[2])
            self.camera.setHpr(self.pacman.rotation[0],self.pacman.rotation[1],self.pacman.rotation[2])
        elif self.cameraMode==2:
            self.camera.setPos(self.pacman.position[0],self.pacman.position[1]-30,self.pacman.position[2]+45)
            self.camera.setHpr(0,-60,0)
        elif self.cameraMode==3:
            self.camera.setPos(0,0,180)
            self.camera.setHpr(0,-90,0)

        if len(self.map.coins) + len(self.map.scares) == 0:
            DirectLabel(frameColor=(0,1,0,1),text="VICTORY", scale=(0.5,0.5,0.5))
            self.scareMode = False
            return
        if not self.pacman.alive and not self.pause:
            self.scareMode = False
            self.lives-=1
            self.pause = True
            self.taskMgr.doMethodLater(3, self.resetGame, 'resetGame')
        return Task.cont
    def ratioChanged(self):
        if base.getAspectRatio() > 1:
            self.gameState  = DirectFrame(frameSize=(-base.getAspectRatio(),base.getAspectRatio(),0.8,1),frameColor=(0,0,1,1))
            self.pointsLabel = DirectLabel(frameColor=(0,0,0,0),text="Points: "+str(self.points), scale=(0.1,0.1,0.1), pos=(-base.getAspectRatio()*0.8,0,0.9))
            self.levelLabel = DirectLabel(frameColor=(0,0,0,0),text="LEVEL "+str(self.level), scale=(0.1,0.1,0.1), pos=(0,0,0.9))
            self.livesLabel = DirectLabel(frameColor=(0,0,0,0),text="Lives: "+str(self.lives), scale=(0.1,0.1,0.1), pos=(base.getAspectRatio()*0.8,0,0.9))
        else:
            self.gameState  = DirectFrame(frameSize=(-1,1,1/base.getAspectRatio()*0.8,1/base.getAspectRatio()),frameColor=(0,0,1,1))
            self.pointsLabel = DirectLabel(frameColor=(0,0,0,0),text="Points: "+str(self.points), scale=(0.1,0.1,0.1), pos=(-0.8,0,0.9))
            self.levelLabel = DirectLabel(frameColor=(0,0,0,0),text="LEVEL "+str(self.level), scale=(0.1,0.1,0.1), pos=(0,0,0.9))
            self.livesLabel = DirectLabel(frameColor=(0,0,0,0),text="Lives: "+str(self.lives), scale=(0.1,0.1,0.1), pos=(0.8,0,0.9))
    def endScare(self,task):
        self.scareMode = False
        self.ghostPts = 200
        for g in self.ghosts:
            g.unscare()
    def startScare(self):
        self.scareMode = True
        for g in self.ghosts:
            g.scare()
        self.taskMgr.doMethodLater(10, self.endScare, 'endScare')
        self.taskMgr.doMethodLater(0.2, self.toggleScare, 'toggleScare')
    def toggleScare(self,task):
        self.gameState.setColor((1,1,0,1))
        self.taskMgr.doMethodLater(0.2, self.toggleScare2, 'toggleScare')
    def toggleScare2(self,task):
        self.gameState.setColor((0,0,1,1))
        if self.scareMode:        
            self.taskMgr.doMethodLater(0.2, self.toggleScare, 'toggleScare')
    def resetGame(self,task):
        if self.lives==0:
            DirectLabel(frameColor=(1,0,0,1),text="GAME OVER", scale=(0.5,0.5,0.5))
        else:
            self.pacman.reset()
            for g in self.ghosts:
                g.reset()
            self.pause = False
 
 
app = MyApp()
app.run()
