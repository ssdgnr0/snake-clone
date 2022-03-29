import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *

class Controls(DirectObject):

    def __init__(self,controls):

        self.controls = controls
        self.set_controls()

    def add_controls(self,contr_name,control):
        
        self.controls[contr_name] = contr_name
        self.accept(control[2],control[1])
    def set_controls(self):

        for c in self.controls:
            obj = self.controls[c][3]
            control_name = self.controls[c][0]
            control_func = self.controls[c][1]
            control_button = self.controls[c][2]
            obj.accept(self.controls[c][2],self.controls[c][1],extraArgs = [-.5])
            

    


