import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
import random
import pprint

class Jewell(DirectObject):
    
    dlight = DirectionalLight('my dlight')
    dlnp = render.attachNewNode(dlight)
    def __init__(self,field):

        self.model = loader.loadModel('jewell.egg')
        self.model.reparentTo(render)
        self.field = field
        self.pos_tile = self.get_pos_tile(random.choice([1,2,2,2,2,1]))      
        self.model.setPos(self.pos_tile.model.getPos())
        self.pos_tile.jewell = True
        Jewell.dlnp.setPos(self.model.getX() + 3,30,self.model.getZ())
        self.model.setLight(Jewell.dlnp)
        
    def get_pos_tile(self,picker):
        pos_found = False
        picke = 1
        if picke == 1:
            while not pos_found:
                x = random.randrange(10,36,2)
                y = random.randrange(10,36,2)
                pos_tile = self.field.field[str(x)+'_'+str(y)]
                if not pos_tile.taken:
                    pos_found = True
                    return pos_tile
                else:
                    continue

    def place_jewell(self,pos):

         self.pos_tile.jewell = False
         self.pos_tile = self.field.field[str(pos[0]) + '_' + str(pos[1])]
         self.model.setPos(self.pos_tile.model.getPos())
         self.pos_tile.jewell = True
         return
   
    def destroy(self):

        self.model.remove()      
        self.pos_tile.jewell = False
        self.model =  None
        self.field = None
        self.pos_tile = None
        self = None
        return
                

    
        

        
