import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
import pprint

class GUIManager(DirectObject):

    def __init__(self,gm):

        self.game_manager = gm
        self.counter = 0

    def setup_splash_screen(self):
           
         self.splash_screen = loader.loadModel("splash_screen.egg")
         self.splash_screen.reparentTo(aspect2d)
         self.splash_screen.setScale(0.7)
         self.textObject = OnscreenText(text = 'Pssssssssssssss!', pos = (-0.5, 0.02), scale = 0.1,fg = (1,1,1,1))
         self.textObject2 = OnscreenText(text = 'Please Press Enter', pos = (-0.5, -0.2,0.8), scale = 0.1,fg = (1,1,1,1))
         self.accept("enter",self.remove_splash_screen)
         
    def remove_splash_screen(self):
        self.textObject.destroy()
        self.textObject2.destroy()
        self.splash_screen.removeNode()     
        self.game_manager.set_state("splash_screen")
        self.ignore("enter")
        return
    
    def setup_menu_screen(self):
        self.counter += 1
        self.menu_screen = loader.loadModel("menu_screen.egg")
        self.menu_screen.reparentTo(aspect2d)
        self.menu_screen.setPos(0,2,0)
        self.menu_screen.setScale(0.4)
        self.new_game_button = DirectButton(scale = 0.08,text = ("New Game"),command = self.send_menu_selection,extraArgs = ['new_game'] ,pos = (0,0,0.5))
        self.settings_button = DirectButton(scale = 0.08,text = ("Settings"),command = self.send_menu_selection,extraArgs = ["settings"] ,pos = (0,0,0.2))
        self.load_game_button = DirectButton(scale = 0.08,text = ("Load Game"),command = self.send_menu_selection,extraArgs = ['load_game'] ,pos = (0,0,-0.1),pressEffect = 0.9)
        self.high_score_button = DirectButton(scale = 0.08,text = ("High score"),command = self.send_menu_selection,extraArgs = ['high_score'] ,pos = (0,0,-0.4),pressEffect = 0.9)
        return
    
    def remove_menu_screen(self):
        self.new_game_button.destroy()
        self.settings_button.destroy()
        self.load_game_button.destroy()
        self.high_score_button.destroy()
        self.menu_screen.removeNode()
        return
    
    def setup_settings_screen(self):

        self.settings_frame = DirectFrame(frameSize = (1,-1,1,-1),frameColor = (0.4,0,0.6,0.9),pos = (0,0,0))
        self.lbl_controls_header = DirectLabel(text = "Controls Settings",pos = (0,0,0.85),scale = 0.08,text_fg=(0.9,0.9,0.9,1),relief = None)  
        self.lbl_cntr_instructions = DirectLabel(text = "Please enter control keys from [a - z]",pos = (0,0,0.8),scale = 0.05,text_fg=(0.9,0.9,0.8,1),relief = None)     
        self.lbl_turn_up = DirectLabel(text = "Turn up",pos = (0,0,0.7),scale = 0.06,text_fg=(0.9,0.9,0.8,1),relief = None)        
        self.de_turn_up = DirectEntry(text = "" ,scale=.05,initialText="", numLines = 2,focus=1, pos = (-0.26,0,0.6))
        
        self.lbl_turn_right = DirectLabel(text = "Turn right",pos = (0,0,0.4),scale = 0.06,text_fg=(0.9,0.9,0.8,1),relief = None)        
        self.de_turn_right = DirectEntry(text = "" ,scale=.05,initialText="", numLines = 2,focus=1, pos = (-0.26,0,0.3))
        
        self.lbl_turn_left = DirectLabel(text = "Turn left",pos = (0,0,0.1),scale = 0.06,text_fg=(0.9,0.9,0.8,1),relief = None)        
        self.de_turn_left = DirectEntry(text = "" ,scale=.05,initialText="", numLines = 2,focus=1, pos = (-0.26,0,0.0))
        
        self.lbl_turn_down = DirectLabel(text = "Turn down",pos = (0,0,-0.2),scale = 0.06,text_fg=(0.9,0.9,0.8,1),relief = None)
        self.de_turn_down = DirectEntry(text = "" ,scale=.05,initialText="", numLines = 2,focus=1, pos = (-0.26,0,-0.3), focusInExtraArgs = [])
        
        self.lbl_set_level = DirectLabel(text = "Set level",pos = (-0,3,-0.5),scale = 0.08,text_fg=(0.9,0.9,0.9,1),relief = None)
        self.lbl_set_level_instrns = DirectLabel(text = "Set level [1 - 7]",pos = (-0,3,-0.55),scale = 0.04,text_fg=(0.9,0.9,0.9,1),relief = None)     
        self.de_set_level = DirectEntry(text = "" ,scale=.05,initialText="", numLines = 2,focus=1, pos = (-0.26,0,-0.64))
        self.error_text = TextNode('node name')
        self.error_text.setText("")
        self.error_textNodePath = aspect2d.attachNewNode(self.error_text)
        self.error_textNodePath.setScale(0.07)
        self.error_textNodePath.setPos(-0.28,0,-0.8)
        self.error_textNodePath.node().setTextColor(1, 0.0, 0.0, 1)
        
    def setup_HUD(self,score,level):
        
          self.HUD = TextNode('HUD')
          cmr12 = loader.loadFont('cmr12.egg')        
          self.HUD.setText("Score " + str(score) + "\nlevel " + str(level))
          self.HUD.setFont(cmr12)
          self.HUDNodePath = render.attachNewNode(self.HUD)
          self.HUDNodePath.setPos(50,37,3.0)
          self.HUDNodePath.setScale(3.00)
          self.HUD.setTextColor(0.5, 0.5, 0.5, 1)
          self.HUD.setFrameColor(1, 1, 1, 1)
          self.HUD.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)
          self.HUD.setCardColor(1, 1, 1, 1)
          self.HUD.setCardAsMargin(0, 0, 0, 0)
          self.HUD.setCardDecal(True)
          return
    
    def update_HUD(self,score,level):
        
        self.HUD.setText("Score " + str(score) + "\nlevel " + str(level))
        return
    def remove_HUD(self):
        self.HUD = None
        self.HUDNodePath.removeNode()
        return       
        
    def show_error_msg(self):
        self.error_text.setText(" Input Error \n please try again")
         
    def remove_settings_screen(self):
         
         self.settings_frame.destroy() 
         self.lbl_controls_header.destroy()
         self.lbl_turn_up.destroy()
         self.de_turn_up.destroy()
         self.lbl_turn_right.destroy()
         self.de_turn_right.destroy()
         self.lbl_turn_left.destroy()
         self.de_turn_left.destroy()
         self.lbl_turn_down.destroy()
         self.de_turn_down.destroy()
         self.lbl_set_level.destroy()
         self.de_set_level.destroy()
         self.lbl_set_level_instrns.destroy()
         self.error_textNodePath.remove()
         self.lbl_cntr_instructions.destroy()
         return
         
    def setup_hscore_screen(self):

       self.hscore_frame = DirectFrame(frameSize = (1,-1,1,-1),frameColor = (0.4,0,0.6,0.9),pos = (0,0,0))
       self.lbl_hscore = DirectLabel(text = "High Score",pos = (0,0,0.7),scale = 0.1,text_fg=(0.9,0.9,0.8,1),relief = None)  
       self.hscore_text = TextNode('node name')
       self.hscore_text.setText(self.game_manager.score_data)
       self.hscore_textNodePath = aspect2d.attachNewNode(self.hscore_text)
       self.hscore_textNodePath.setScale(0.07)
       self.hscore_textNodePath.setPos(0.0,0,0.4)
       self.hscore_textNodePath.node().setTextColor(1, 0.6, 0.0, 1)
       return

    def remove_hscore_screen(self):

        self.hscore_frame.destroy()
        self.lbl_hscore.destroy()
        self.hscore_textNodePath.remove()
        return
    
    def setup_paused_screen(self):

        self.spframe = DirectFrame(frameSize = (1,-1,1,-1),frameColor = (0.4,0,0.6,0.4),pos = (0,0,0))
        self.btn_save_game = DirectButton(scale = 0.08,text = ("Save Game"),command = self.send_menu_selection,extraArgs = ['save_game'] ,pos = (-0.3,0,-0.4),pressEffect = 0.9)
        self.btn_resume_game = DirectButton(scale = 0.08,text = ("Resume Game"),command = self.send_menu_selection,extraArgs = ['resume_game']    ,pos = (0.0,0,-0.1),pressEffect = 0.9)
        self.btn_exit_game = DirectButton(scale = 0.08,text = ("Exit"),command = self.send_menu_selection,extraArgs = ['exit_game']  ,pos = (0.3,0,-0.4),pressEffect = 0.9)
        self.lbl_game_paused = DirectLabel(text = "Game Paused",pos = (0,0,0.4),scale = 0.2,text_fg=(0.9,0.9,0.8,1),relief = None)
        self.tn_game_saved = TextNode('node name')
        self.tn_game_saved.setText("")
        self.tn_game_savedNodePath = aspect2d.attachNewNode(self.tn_game_saved)
        self.tn_game_savedNodePath.setScale(0.07)
        self.tn_game_savedNodePath.setPos(-0.28,0,-0.5)
        self.tn_game_savedNodePath.node().setTextColor(1, 0.0, 0.0, 1)
        return

    def show_saved_msg(self):
        self.tn_game_savedNodePath.node().setText('Game Saved!')
    def remove_paused_screen(self):

        self.spframe.destroy()
        self.btn_save_game.destroy()
        self.btn_resume_game.destroy()
        self.btn_exit_game.destroy()
        self.lbl_game_paused.destroy()
        self.tn_game_savedNodePath.remove()
        return

    def setup_game_over_screen(self):
        self.game_over_frame_geom = loader.loadModel("game_over_screen.egg")
        self.game_over_frame = DirectFrame(frameSize = (1,-1,1,-1),geom = self.game_over_frame_geom,frameColor = (0.4,0,0.6,0.9),pos = (0,0,0))
        self.lbl_game_over = DirectLabel(text = "Game Over",pos = (0,0,0.4),scale = 0.4,text_fg=(1,0.0,0.0,1),relief = None)
        self.btn_new_game = DirectButton(scale = 0.08,text = ("New Game"),command = self.send_menu_selection,extraArgs = ['new_game'] ,pos = (0.0,0,0.1))
        self.btn_exit = DirectButton(scale = 0.08,text = ("Load Game"),command = self.send_menu_selection,extraArgs = ["load_game"] ,pos = (0.0,0,-0.1))
        self.btn_load_game = DirectButton(scale = 0.08,text = ("Exit"),command = self.send_menu_selection,extraArgs = ['exit_game'] ,pos = (0,0,-0.3),pressEffect = 0.9)
        return
    def remove_game_over_screen(self):
        
        self.game_over_frame.destroy()
        self.lbl_game_over.destroy()
        self.btn_new_game.destroy()
        self.btn_exit.destroy()
        self.btn_load_game.destroy()
        return
             
    def send_menu_selection(self,selection):
           
        if selection == 'new_game':
             print("message_sent")
             self.game_manager.set_state("new_game")
        if selection == 'load_game':
            self.game_manager.set_state("load_game")
        if selection == 'settings':
             self.game_manager.set_state("settings")
        if selection == 'high_score':
             self.game_manager.set_state("high_score")
        if selection == 'save_game':
            self.game_manager.set_state('save_game')
        if selection == 'resume_game':
            self.game_manager.set_state('resume_game')
        if selection == 'exit_game':
            self.game_manager.set_state('exit_game')
                      
        return
    


