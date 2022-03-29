import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
import random
import pprint

class Obstacles(DirectObject):

    def __init__(self,field,o_type = random.randint(0,3)):

        self.types = [['18_20','20_20','22_20','24_20','26_20','28_20','30_20','32_20','34_20',
                      '24_22','24_24','24_26','24_28','26_28','28_28','28_30'],
                      ['16_20','18_20','20_20','22_20','24_20','26_20','28_20','30_20','32_20','34_20',
                       '16_22','16_24','16_26','16_28','16_30','16_32','18_32','20_32','22_32','28_32','30_32','32_32',
                       '34_20','34_22','34_24','34_26','34_28','34_30','34_32'],
                      ['10_40','12_40','14_40','16_40','32_40','34_40','36_40','38_40','10_10','12_10','14_10','16_10','32_10','34_10','36_10','38_10','16_20','16_22',
                       '16_24','16_26','16_28','18_24','20_24','22_24','24_24','26_24','28_24','30_24','32_24','34_24','34_20','34_22','34_26','34_28'],
                      ['18_18','18_20','18_22','18_24','18_26','18_28','18_30','18_32','18_34','20_26','22_26','24_26','26_26','28_18','28_20','28_22','28_24',
                       '28_26','28_28','28_30','28_32','28_34']]
        
        self.field = field
        self.type = o_type
        self.pieces = []
        self.place_obstacle(self.types[self.type])
        self.dt = 0
      
        
        
    def place_obstacle(self,obstacle):

        for t in obstacle:
            pos_tile = self.field.field[t]
            tile = loader.loadModel('obstacle.egg')
            tile.reparentTo(render)
            tile.setPos(pos_tile.model.getX(),38,pos_tile.model.getZ())
            self.pieces.append(tile)
            pos_tile.taken = True
            pos_tile.model.hide()
        taskMgr.add(self.update,'UpdateObstacle')
        return
            
    def destroy(self):
        taskMgr.remove("UpdateObstacle")
        for ob in self.pieces:
            tile_key = (str(int(ob.getX())) +'_'+ str(int(ob.getZ())))
            self.field.field[tile_key].taken = False
            self.field.field[tile_key].model.show()
            ob.remove()
        
        self.pices = None
        self.field = None
        self = None       
        return
    def update(self,task):

        self.dt += globalClock.getDt()
        if self.dt > 1:
            self.dt = 0
        return task.cont
            
        
        
        
