import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from Game import Game
from GUIManager import GUIManager
from GameAudio import Audio
import SaveData
import pprint
import csv

class GameManager(DirectObject):

    def __init__(self):

        self.game_states =('splash_screen','menu_screen','pause_screen','playing','game_over_screen')
        self.gui = GUIManager(self)
        self.game_state = 'splash_screen'
        self.game_data = SaveData.load_game_data()
        self.audio = Audio()
        self.gui.setup_splash_screen()

    def set_state(self,state):
       
        if state == 'splash_screen':
            self.gui.setup_menu_screen()
            self.game_state = 'menu_screen'
            self.prev_state = 'splash_screen'
            return
        if self.game_state == 'menu_screen':
          
            if state == "new_game":
                self.gui.remove_menu_screen()
                self.start_new_game()
                self.game_state = 'playing'
                self.accept('escape',self.pause_game)
            if state == "load_game":
                self.load_game()
            if state == 'settings':
                self.gui.remove_menu_screen()
                self.gui.setup_settings_screen()
                self.accept("escape",self.exit_settings_screen)
            if state == 'high_score':
                self.gui.remove_menu_screen()
                self.gui.setup_hscore_screen()
                self.accept("escape",self.exit_hscore_screen)
        if self.game_state == 'playing':
           
            if state == 'save_game':
                self.save_game()
            if state == 'resume_game':
                self.resume_game()
            if state == 'exit_game':
                self.exit_game()
        if self.game_state == 'game_over_screen':
             if state == 'new_game':
                self.gui.remove_game_over_screen()
                self.start_new_game()
                self.game_state = 'playing'
                self.accept('escape',self.pause_game)
             if state == 'load_game':
                self.gui.remove_game_over_screen()
                self.load_game()
             if state == 'exit_game':
                self.exit_game()
            
                
            
            
                
                
    def start_new_game(self):
        self.game = Game()
        self.game.level = int(self.game_data[0])
        if self.game.level > 1: self.game.set_level()
        self.gui.setup_HUD(self.game.score,self.game.level)
        taskMgr.add(self.update, "Update")
    def pause_game(self):
        self.game.pause_game()
        self.ignore('escape')
        self.gui.setup_paused_screen()
        self.accept('escape',self.resume_game)
    def resume_game(self):
        self.gui.remove_paused_screen()
        self.game.resume_game()
        self.accept('escape',self.pause_game)
    def save_game(self):
        self.game.save_game()
    def exit_settings_screen(self):
        
        if self.save_game_settings():
           self.gui.remove_settings_screen()
           self.ignore('escape')
           self.gui.setup_menu_screen()
        else:
            self.gui.show_error_msg()
    def exit_hscore_screen(self):
        self.gui.remove_hscore_screen()
        self.ignore('escape')
        self.gui.setup_menu_screen()
    def save_game_settings(self):
        self.game_settings_data = []
        temp = [self.gui.de_turn_up.get(),self.gui.de_turn_right.get(),
                                    self.gui.de_turn_left.get(), self.gui.de_turn_down.get(),
                                    self.gui.de_set_level.get()]
        
        #print(self.game_settings_data)
        for c in temp:
             if c in ['a','b','c','d','e','f','g',
                                'h','i','j','k','l','m','n','o',
                                'p','q','r','s','t','u','v','w','x','y','z'
                                ]:
                 self.game_settings_data.append(c)
        if temp[4] in ['1','2','3','4','5','6','7']:
            self.game_settings_data.append(temp[4])
            
            
        if len(self.game_settings_data) != 5:
            return False
                         
        SaveData.save_game_settings_data(self.game_settings_data)
        return True

    def load_game(self):
        self.gui.remove_menu_screen()
        self.sgame_data = []
        with open('saved_game.txt','r') as saved_game_file:
            saved_game_file_reader = csv.reader(saved_game_file)
            for line in saved_game_file_reader:
                self.sgame_data.append(line)
        print(self.sgame_data)
        self.game = Game()
        self.game.load_game(self.sgame_data)
        self.gui.setup_HUD(self.game.score,self.game.level)
        self.game_state = 'playing'
        self.accept('escape',self.pause_game)
        taskMgr.add(self.update, "Update")
        
           
    def exit_game(self):
        exit()
    
    
    def end_game(self):
        self.ignore('escape')
        taskMgr.remove('Update')
        self.gui.setup_game_over_screen()
        self.gui.remove_HUD()
        self.game = None
    def update(self,task):
       
        if self.game_state == 'playing':
            
            self.gui.update_HUD(self.game.score,self.game.level)
            if self.game.bgame_over:
               self.game_state = "game_over_screen"
               self.end_game()
      
        return task.cont
        
        
        
game = GameManager()
run()
    
