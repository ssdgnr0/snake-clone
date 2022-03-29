import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from panda3d.core import Point3
from pandac.PandaModules import AudioManager

class Audio():

    def __init__(self):
        self.audio_list = ["audio0.mp3"]
        self.musicMgr = base.sfxManagerList[0]
        self.music =  loader.loadSfx(self.audio_list[0])
        self.musicMgr.setVolume(0.5)
        self.music.setLoop(True)
        self.music.play()
       
