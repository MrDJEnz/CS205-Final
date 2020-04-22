from tkinter import *
import Start
from Start import *
import Constants as c
from Map import Map
import random
import copy
from Player import Player
from Goal import Goal
from Objective import Objective
from Card import Card
from Turns import Turns

fields = []
CLOCK_TICK=60 #refresh rate

def fetch(entries):
   for entry in entries:
      field = entry[0]
      text = entry[1].get()
      color=entry[2].get()
      print('%s: "%s" %s' % (field, text,color))

def correspondance_colors(nameofcolor,colormap):
   if nameofcolor =='red':
      return colormap.red
   elif nameofcolor=='green':
      return colormap.green
   elif nameofcolor=='blue':
      return colormap.blue
   elif nameofcolor=='yellow':
      return colormap.yellow
   elif nameofcolor=='purple':
      return colormap.purple
   elif nameofcolor=='cian':
      return colormap.cian

def launch_game(entries):
   #on verifie que deux joueurs n'ont pas la meme couleur, pas de nom vide
   try:
      players_names=[]
      players_colors=[]
      for entry in entries:
         players_names.append(entry[1].get())
         if entry[1].get()=='':
            raise ValueError('you must enter player name')
         players_colors.append(entry[2].get())
      seen = set()
      uniq = []
      for c in players_colors:
         if c not in seen:
           uniq.append(c)
           seen.add(c)
      if not len(uniq)==len(players_names):
         raise ValueError('each player must have their own colors:')
   except ValueError as e:
         print (e.args)
   else:
      root.destroy() #exiting the players choicd window

      print("== Game launched ==")
      M=Map('Terre')
      Continents=M.continents
      nb_players=len(players_names)
      T=Turns(nb_players,M)
      T.start_deploy()
      print(T.distrib_pays(M.pays))
      T.print_players()

      colors=ColorMap()
      for idx,play_name in enumerate(players_names):
         T.players[idx].color=correspondance_colors(players_colors[idx],colors)
         T.players[idx].name=play_name

      pygame.init()
      clock = pygame.time.Clock()
      fenetre = pygame.display.set_mode((1280, 800)) #cant use constants for so
      Win=CurrentWindow(fenetre,T)
      Win.game.nb_joueurs=nb_players
      Win.game.joueurs=players_names
      menu(Win)
      Win.fonctions.append(Win.start_game)
      clock.tick(CLOCK_TICK)

      Win.afficher() #on rentre dans la boucle while d'affichage


def save(entries):
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()

def check_colors(entries,lst1):
   for entry in entries:
      if entry[2].get() in lst1: lst1.remove(entry[2].get())   

def makeform(root, fields):
   entries = []
   for idx,field in enumerate(fields):
      lab = Label(root, width=15, text=field, anchor='w')
      ent = Entry(root)
      lab.grid(row=idx, column=0)
      ent.grid(row=idx, column=1)
      lst1 = c.COLORS
      var1 = StringVar()
      Drop = OptionMenu(root,var1,*lst1)
      Drop.grid(row=idx, column=2,sticky="ew") # make option menu with uniform width for all the rows 
      entries.append((field, ent,var1))
   return entries

def checkPlayers():
   nb_joueurs = int(Entry1.get())
   if nb_joueurs<c.minPlayers:
      print("Minimum players number is "+str(c.minPlayers))
      nb_joueurs=c.minPlayers
   elif nb_joueurs>c.maxPlayers:
      print("Maximum players number is "+str(c.maxPlayers))
      nb_joueurs=c.maxPlayers
   else:
      print(nb_joueurs)
   for k in range(0,nb_joueurs):
      fields.append("Player "+str(k+1))
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))
   b1.grid_forget()
   Entry1.grid_forget()
   Lbl1.grid_forget()
   b2 = Button(root, text='Play',command=lambda e=ents: launch_game(e)) 
   b2.grid(row=20, column=0)
   b3.grid(row=20, column=1)
   
if __name__ == '__main__':
   root = Tk()
   root.title("Risk Setup")

##  ###
##   tempEntries = []
##   tempEntries.append(("Player 1", "jack","Cyan"))
##   launch_game(tempEntries)
##   ##

   Lbl1 = Label(root, text="Number of Players:")
   Lbl1.grid(row=0, column=0,columnspan=2)
   Entry1 = Entry(root, bd = 1)
   Entry1.grid(row=1, column=0,columnspan=2)

   b1 = Button(root, text='Done',command=checkPlayers)
   b1.grid(row=2, column=0)
    
   b3 = Button(root, text='Quit', command=root.quit)
   b3.grid(row=2, column=1)
   root.mainloop()


 
