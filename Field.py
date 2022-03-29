from direct.directbase import DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import*
import pprint

class Tile(DirectObject):
    instance_count = 0 
    def __init__(self,name,pos,field,row):
        Tile.instance_count = Tile.instance_count  + 1
        self.id = Tile.instance_count
        self.name = name
        self.model = loader.loadModel("Tile.egg")
        self.model.setPos(pos)
        self.jewell =  False
        self.taken = False
        self.row = row
        self.model.reparentTo(render)

class Field(DirectObject):
  
    def __init__(self,cols,rows):

        row_index = 0
        self.numOfCols = cols
        self.numOfRows = rows
        self.rows = {}
        self.field = {}
        self.startXPos = 0
        self.startZPos = 0
        self.background = loader.loadModel('game_bg.egg')
        self.background.reparentTo(base.camera)
        self.background.setPos(25,39,25) 
        self.background.setBin('background',1000)
        self.background.setScale(20)
        #Construct the field
        for r in range(self.numOfRows):
           
            for c in range(self.numOfCols):
                tile = Tile(str(self.startXPos) + str(self.startZPos) ,(self.startXPos,38,self.startZPos),self,"ROW_" + str(r))           
                self.field.setdefault(str(int(self.startXPos)) +'_'+ str(int(self.startZPos)),tile)               
                self.startXPos += (2.0)
            self.rows.setdefault("ROW_" + str(row_index),[])
            self.startXPos = 0
            self.startZPos += (2.0)
            row_index = row_index + 2
    def destroy(self):
        
       for t in self.field:
         self.field[t].model.remove()
       self = None
       return
       

   
