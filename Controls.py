import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
import csv
import SaveData
import pprint

class Controls(DirectObject):

     def __init__(self):

         self.control_keys = ['a','b','c','d']
         temp = []
         with open('control_settings.txt','r') as contr_file:
             contr_file_reader = csv.reader(contr_file)
             print()

             for line in  contr_file_reader:
                 if line[0] in ['a','b','c','d','e','f','g',
                                'h','i','j','k','l','m','n','o',
                                'p','q','r','s','t','u','v','w','x','y','z'
                                ]:
                     temp.append(line[0])
             if len(temp) == 4:
                self.control_keys = temp
     def save_controls(self,controls):
        
         with open('control_settings.txt','w') as contr_file:
            contr_file_writer = csv.writer(contr_file_file)
            for key in contr_file:
                contr_file_writer.writerow(key)
                
             
                 
                 
                 
             
             
d = Controls()        
