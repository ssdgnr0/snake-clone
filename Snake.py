import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
import pprint

class SnakeNodes(DirectObject):
    
    def __init__ (self,head):

        self.model = loader.loadModel("snake_body.egg")
        if head: self.model = loader.loadModel("snake_head.egg")
        self.model.reparentTo(render)
        self.next = None
        self.prev = None
        self.prevPos = None
       
class Snake(DirectObject):
    
    cam = base.cam
    cam.setPos(25,-64,25)
    def __init__(self,field,controls):
        
        self.head = SnakeNodes(True)
        self.nodes = []
        self.controls = controls
        self.Field = field
        self.nodes.append(self.head)
        p = (self.Field.field['14_14'].model)
        self.head.model.setPos(p.getX(),38,p.getZ())
        self.head.prevPos = (self.head.model.getX() - 2,self.head.model.getY(),self.head.model.getZ())
        prev = self.head
        self.alive = True
        self.speed_lim = 1
        for i in range(3):
            node =  SnakeNodes(False)
            pos = prev.model
            node.model.setPos(prev.model.getX()-2,38,prev.model.getZ())
            self.nodes.append(node)
            node.next = prev
            node.prevPos = (node.model.getX() - 2,node.model.getY(),node.model.getZ())
            prev = node
        self.dt = 0  
        self.tail = self.nodes[len(self.nodes)-1]
        self.direction = "Horizontal"
        self.displacement = 2
        self.compass = 2
        self.found_jewell = False
        self.length = len(self.nodes)
        self.accept(controls[0],self.turn,extraArgs = ['Vertical',-90])
        self.accept(controls[3],self.turn,extraArgs = ['Vertical',90])
        self.accept(controls[1],self.turn,extraArgs = ['Horizontal',0])
        self.accept(controls[2],self.turn,extraArgs = ['Horizontal',180])
        taskMgr.add(self.update, "UpdateSnake")
           
    def can_translate(self, direction, displacement):
        
        if self.direction == "Vertical":
           next_pos = (str(int(self.head.model.getX())) +'_'+ str(int(self.head.model.getZ() + self.compass)))
           if next_pos in self.Field.field and not self.Field.field[next_pos].taken:
               return True
                   
        if self.direction == "Horizontal":
            next_pos = (str(int(self.head.model.getX() + self.compass)) +'_'+ str(int(self.head.model.getZ())))
            if next_pos in self.Field.field and not self.Field.field[next_pos].taken:
                return True
        return False

    def translate(self,direction):
            
            if self.can_translate(self.direction,self.displacement):     
                if direction == 'Vertical':
                   self.head.prevPos = self.head.model.getPos()
                   self.Field.field[(str(int(self.head.prevPos[0])) +'_'+ str(int(self.head.prevPos[2])))].taken = False
                   self.head.model.setFluidX(self.head.model,self.displacement)
                   self.Field.field[str(int(self.head.model.getX())) +'_'+ str(int(self.head.model.getZ()))].taken = True
                   for i in range(self.length):
                      if self.nodes[i].next != None:
                         self.Field.field[str(int(self.nodes[i].model.getX())) +'_'+ str(int(self.nodes[i].model.getZ()))].taken = False
                         self.nodes[i].prevPos = self.nodes[i].model.getPos()
                         self.nodes[i].model.setPos(self.nodes[i].next.prevPos)
                         self.Field.field[str(int(self.nodes[i].model.getX())) +'_'+ str(int(self.nodes[i].model.getZ()))].taken = True
                                     
                if direction == 'Horizontal':

                     self.head.prevPos = self.head.model.getPos()
                     self.Field.field[(str(int(self.head.prevPos[0])) +'_'+ str(int(self.head.prevPos[2])))].taken = False
                     self.head.model.setFluidX(self.head.model,self.displacement)
                     self.Field.field[str(int(self.head.model.getX())) +'_'+ str(int(self.head.model.getZ()))].taken = True
                     for i in range(self.length):
                         if self.nodes[i].next != None:                
                            self.Field.field[str(int(self.nodes[i].model.getX())) +'_'+ str(int(self.nodes[i].model.getZ()))].taken = False
                            self.nodes[i].prevPos = self.nodes[i].model.getPos()
                            self.nodes[i].model.setPos(self.nodes[i].next.prevPos)
                            self.Field.field[str(int(self.nodes[i].model.getX())) +'_'+ str(int(self.nodes[i].model.getZ()))].taken = True
            else:
                self.game_over()
                                               
    def turn(self,direction,degrees):
        
        if self.direction == direction:
            return
        if direction == 'Vertical':
            if self.head.model.getX() == self.nodes[1].model.getX(): return
            self.head.model.setR(degrees)
            self.direction = direction
            if degrees == 90:
                self.compass = -2
            else:  self.compass = 2
            
        if direction == 'Horizontal':
            if self.head.model.getZ() == self.nodes[1].model.getZ(): return
            self.head.model.setR(degrees)
            self.direction = direction
            if degrees == 180:
                self.compass = -2
            else:  self.compass = 2
    def addNode(self):

        node = SnakeNodes(False)
        node.next = self.nodes[len(self.nodes)-1]
        node.model.setPos(node.next.prevPos)
        node.model.reparentTo(render)
        self.nodes.append(node)
        self.length = len(self.nodes)
        return
    def load_body(self,data):

        for i in range(1,4):
             self.Field.field[str(int(self.nodes[1].model.getX())) +'_'+ str(int(self.nodes[1].model.getZ()))].taken = False
             self.nodes[1].model.remove()
             
             del self.nodes[1]
        
        taskMgr.remove('UpdateSnake')
        prev = self.head 
        for n in range(len(data)):
            node =  SnakeNodes(False)
            pos = prev.model
            node.model.setPos(int(data[n][0]),38,int(data[n][1]))
            self.nodes.append(node)
            node.next = prev
            node.prevPos = (node.model.getX(),node.model.getY(),node.model.getZ())
            prev = node
        self.length = 1 + len(data)
        if abs(self.head.model.getR()) == 90: self.direction = 'Vertical'
        if self.direction == 'Vertical' and self.head.model.getR() == 90: self.compass = -2
        if self.direction == 'Horizontal' and self.head.model.getR() == 180: self.compass = -2
        taskMgr.add(self.update, "UpdateSnake")
        return
        
    def pause(self):
        taskMgr.remove('UpdateSnake')
    def resume(self):
        taskMgr.add(self.update, "UpdateSnake")
    def game_over(self):
         
         for n in self.nodes:
             n.model.remove()
         self.nodes = None
         self.alive = False
         taskMgr.remove('UpdateSnake')
         
         self.ignore(self.controls[0])
         self.ignore(self.controls[1])
         self.ignore(self.controls[2])
         self.ignore(self.controls[3])
         self = None
        
    def update(self,task):
       
        self.dt += globalClock.getDt()
        if self.dt > self.speed_lim:
            self.translate(self.direction)
            self.dt = 0       
            if self.Field.field[(str(int(self.head.prevPos[0])) +'_'+ str(int(self.head.prevPos[2])))].jewell:
               self.found_jewell = True
               self.addNode()
               print("Shadow shuriken jutsu")
                   
        return task.cont
            
                

            
            
        
