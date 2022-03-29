import csv

def save_game_settings_data(data):
     with open("game_settings.txt","w") as f:
       fw = csv.writer(f)
       fw.writerow([data[4]])
      
     with open("control_settings.txt","w") as f:
       fw = csv.writer(f)
       fw.writerow([data[0]])
       fw.writerow([data[1]])
       fw.writerow([data[2]])
       fw.writerow([data[3]])

def load_game_data():
     game_data = []
     with open('game_settings.txt','r') as g_file:
             g_file_reader = csv.reader(g_file)
             print()

             for line in  g_file_reader:                
                     game_data.append(line[0])
     return game_data
