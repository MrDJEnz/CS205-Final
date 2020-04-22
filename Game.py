# Game can be run by itself for debugging, run the RiskGUI to setup player settings

# Imports needed modules
import functools
import glob
import pickle
import pygame
from pygame import *

from ColorMap import ColorMap
from GamePara import GamePara
from SpritePays import SpritePays

import Constants as c

# Class contains pygame methods
class Game():
    def __init__(self, pygameWindow, Round): #Initializes surfaces for pygame given pygame and round instances
        self.pygameWindow = pygameWindow

        # Updates current objects
        self.game = GamePara()
        self.map = Round.map
        self.players = Round.players
        self.Round = Round

        self.numTroops = 25 #Sets number of troops
        self.selectedTerritory = None

        self.dices = [] #Contains dice results
        self.functions = [] #Contains function calls
        self.interfaceText = [] #Contains text layers for HUD
        self.surfaces = [] #Contains surface layers
        self.tempTerritoryList = [] #Contains territory layers
        self.textList = [] #Contains text overlays
        self.topLevel = [] #Used to hold help and win screen

    @property # Decorator overwrites get/set, method checks min deployment troops
    def troopCount(self):
        if self.Round.phase == 0:
            return min(self.numTroops, self.players[self.Round.player_turn-1].nb_troupes) #Cannot deploy more then total - 1 troops from territory
        else:
            return self.numTroops

    @troopCount.setter # Alternative corresponding decorator
    def troopCount(self, troopVal):
        if self.Round.phase == 0: #Checks troop placement during different phases
            if troopVal < 1:
                self.numTroops = 1
                print("Too few troops")
            elif troopVal > self.players[self.Round.player_turn - 1].nb_troupes:
                self.numTroops = self.players[self.Round.player_turn - 1].nb_troupes
                print("Too many troops")
        else: 
            if troopVal < 0:
                self.numTroops = 0
                print("Too few troops")
            elif troopVal > self.selectedTerritory.nb_troupes - 1:
                self.numTroops = self.selectedTerritory.nb_troupes - 1 #Minimum of 1 troop per territory
                print("Too many troops")
                
        self.numTroops = troopVal

    # Sets a color layer on territory sprites based on player color
    def colorTerritories(self, sprites):
        for p in self.players:
            for pays in p.pays:
                sprite = next((s for s in sprites if s.id == pays), None)
                color_surface(sprite, p.color, 255)

    # Method initialzes map surface
    def run(self):
        self.surfaces=[]
        background = pygame.image.load(c.backgroundPath + c.backgroundImage).convert()

        #Auto resize to fit background
        resize = c.windowLength/background.get_width()
        w = int(resize * background.get_width())
        h = int(resize * background.get_height())
        background = pygame.transform.scale(background, (w, h))

        #Auto resize to fit base map
        worldMap = pygame.image.load(c.imagePath + c.mapImages).convert_alpha()
        resize = c.windowLength/worldMap.get_width()
        w = int(resize * worldMap.get_width())
        h = int(resize * worldMap.get_height())
        worldMap = pygame.transform.scale(worldMap, (w, h))

        #Player HUD
        barre = pygame.image.load(c.imagePath + c.bareImage).convert_alpha()
        barre = pygame.transform.scale(barre, (c.windowLength, c.windowWidth - h))

        self.functions = []
        self.surfaces.extend([[background, (0, 0)], [barre, (0, h)], [worldMap, (0, 0)]])

    # Method utilizes overlay methods to update pygameWindow
    def display(self, function = None):
        colormap = ColorMap()

        # Boolean flags for player functions
        select = False
        atck_winmove = False
        help_menu = False
        hide = True

        worldTerritories = glob.glob(c.mapPath + "*.png")
        territorySprites = []
        
        id_c = 0
        sprite_select = -1
        display = 1

        territorySpriteLayer = []

        # Updating territory sprites
        for i, j in enumerate(worldTerritories):
            s = pygame.image.load(j).convert()
            resize = c.windowLength/s.get_width()
            s = pygame.transform.scale(s, (int(resize * s.get_width()),int(resize * s.get_height())))
            
            sp = SpritePays(s, j)
            sp_masque = SpritePays(s.copy(),j)
            
            color_surface(sp_masque, (1, 1, 1), 150)
            territorySprites.append(sp)
            territorySpriteLayer.append(sp_masque)

        self.colorTerritories(territorySprites)
        for i, spr in enumerate(territorySprites):
            if i == 0:
                merged_pays = spr.map_pays.copy()
            else:
                merged_pays.blit(spr.map_pays, (0, 0))

        # Update visual troop numbers
        troopDisplay(self.textList, territorySprites, self.map)

        # Event handler
        while display:
            for event in pygame.event.get():
                if event.type == QUIT:
                    display = 0
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        display = 0
                    elif event.key == K_n:
                        try:
                            self.Round.next()
                        except ValueError as e:
                            print(e.args)
                        self.tempTerritoryList=[]
                        select=False
                        sprite_select=0
                    elif event.key == K_p:
                        try:
                            self.Round.next_player()
                        except ValueError as e:
                            print(e.args)
                        self.tempTerritoryList=[]
                        select=False
                        sprite_select=0
                    elif event.key == K_w:# for debugging
                        self.Round.game_finish=True
                    elif event.key == K_h:
                        help_menu = not help_menu
                    elif event.key == K_c:
                        self.tempTerritoryList=[]
                        display_continent(self.Round.map.continents[id_c],self.tempTerritoryList,territorySpriteLayer)
                        id_c=(id_c+1)%len(self.Round.map.continents)
                    elif event.key == K_u:#use cards
                        self.Round.players[self.Round.player_turn-1].use_best_cards()
                    elif event.key == K_d:#show/hide player objectives
                        hide = not hide
                    elif event.key == K_s:#save
                        save_game(self)
                    elif event.key == K_r:#restoration
                        restore_game(self.Round)
                elif event.type == MOUSEBUTTONDOWN:
                    try:
                        if event.button==3: #rigth click to unselect
                            self.tempTerritoryList=[]
                            select=False
                            sprite_select=0
                        elif event.button==4:#scroll wheel up
                            self.troopCount+=1
                        elif event.button==5:#scroll wheel down
                            if self.troopCount>0:
                                self.troopCount-=1
                    except AttributeError as e:
                        print('You should select a country first')
                    except ValueError as e:
                        print(e.args)

            for surface in self.surfaces:
                self.pygameWindow.blit(surface[0],surface[1])
            for dice in self.dices:
                self.pygameWindow.blit(dice[0],dice[1])
            self.pygameWindow.blit(merged_pays,(0,0))
            for tempTerritoryList in self.tempTerritoryList:
                self.pygameWindow.blit(tempTerritoryList,(0,0))
            for texte in self.textList:
                self.pygameWindow.blit(texte[0],texte[1])
            for t in self.interfaceText:
                self.pygameWindow.blit(t[0],t[1])
            for final in self.topLevel:
                self.pygameWindow.blit(final[0],final[1])
            if self.functions != []:
                for f in self.functions:
                    f()

            # Screen for when player wins
            if self.Round.players[self.Round.player_turn-1].obj.get_state()==True:
                self.topLevel=[]
                win_screen = pygame.Surface(self.pygameWindow.get_size())
                win_screen = win_screen.convert()
                win_screen.fill(colormap.black)
                win_screen.set_alpha(180)
                self.topLevel.append([win_screen,(0,0)])
                display_win(self.topLevel,self.players)
            else:
                if help_menu:
                    self.topLevel=[]
                    win_screen = pygame.Surface(self.pygameWindow.get_size())
                    win_screen = win_screen.convert()
                    win_screen.fill(colormap.black)
                    win_screen.set_alpha(180)
                    self.topLevel.append([win_screen,(0,0)])
                    display_help(self.topLevel,colormap)
                else:
                    self.topLevel=[]

            mouse = pygame.mouse.get_pos()
            try:
                mouse_color=self.surfaces[2][0].get_at((mouse[0],mouse[1]))
            except IndexError as e:
                pass

            try:
                if mouse_color != (0,0,0,0) and mouse_color != (0,0,0,255):
                    temptroopValID=mouse_color[0]-100
                    sp_msq=next((sp for sp in territorySpriteLayer if sp.id == temptroopValID), None)
                    if temptroopValID != sprite_select:
                        self.pygameWindow.blit(sp_msq.map_pays,(0,0))
                        pygame.display.update(sp_msq.map_pays.get_rect())
                    click=pygame.mouse.get_pressed()
                    if self.Round.list_phase[self.Round.phase] == 'Placement':
                            if click[0]==1:
                                pays=next((p for p in self.map.pays if p.id == temptroopValID), None) 
                                if pays.id_player==self.Round.player_turn:
                                    self.Round.placer(pays,self.troopCount)
                                    pygame.time.wait(100)
                                else:
                                    print('This territory does not belong to the player!')
                    elif self.Round.list_phase[self.Round.phase] == 'Attack':
                        if click[0]==1 and not select: #selection du pays attaquant 
                            pays1=next((p for p in self.map.pays if p.id == temptroopValID), None)
                            self.selectedTerritory=pays1
                            if pays1.id_player==self.Round.player_turn and pays1.nb_troupes>1:
                                self.troopCount=pays1.nb_troupes-1
                                self.tempTerritoryList.append(sp_msq.map_pays)
                                select=True 
                                sprite_select=temptroopValID
                        elif click[0]==1:#selection du pays attaqué
                            pays2=next((p for p in self.map.pays if p.id == temptroopValID), None)
                            if atck_winmove and pays2 == pays_atck and pays1.nb_troupes>1:#mouvement gratuit apres attaque reussi
                                self.Round.deplacer(pays1,pays2,self.troopCount)
                                select=False
                                self.tempTerritoryList=[]
                                atck_winmove=False
                            elif atck_winmove:
                                select=False
                                self.tempTerritoryList=[]
                                atck_winmove=False
                            elif pays2.id_player!=self.Round.player_turn and pays2.id in pays1.voisins:
                                try:
                                    self.dices=[]         #on efface les ancians sprites des dice                                
                                    atck,res_l=self.Round.attaque(pays1,pays2,self.troopCount)
                                    print(res_l)
                                    for i,res in enumerate(res_l):
                                        roll_dices(self,res[0],res[2],600,territorySprites[0].map_pays.get_height()+10+i*c.diceSize*1.1)#pas propre
                                        roll_dices(self,res[1],res[3],800,territorySprites[0].map_pays.get_height()+10+i*c.diceSize*1.1)
                                    pygame.time.wait(100) #pas propre
                                    #print(res)
                                except ValueError as e:
                                    print(e.args)
                                    atck=False
                                    select=False
                                    self.tempTerritoryList=[]
                                if atck:
                                    sprite=next((s for s in territorySprites if s.id == temptroopValID), None)
                                    color_surface(sprite,self.Round.players[self.Round.player_turn-1].color,255)
                                    merged_pays.blit(sprite.map_pays,(0,0))
                                    atck_winmove=True
                                    pays_atck=pays2
                                    self.troopCount=pays1.nb_troupes-1
                                else:
                                    select=False
                                    self.tempTerritoryList=[]
                    elif self.Round.list_phase[self.Round.phase] == 'Movement':
                        if click[0]==1 and not select:
                            pays1=next((p for p in self.map.pays if p.id == temptroopValID), None)
                            self.selectedTerritory=pays1
                            if pays1.id_player==self.Round.player_turn and pays1.nb_troupes>1:
                                self.troopCount=pays1.nb_troupes-1
                                self.tempTerritoryList.append(sp_msq.map_pays)
                                select=True 
                                sprite_select=temptroopValID
                        elif click[0]==1:
                            pays2=next((p for p in self.map.pays if p.id == temptroopValID), None)
                            chemin=self.map.chemin_exist(self.Round.players[self.Round.player_turn-1].pays,pays1,pays2) #checks if path exists
                            select=False
                            sprite_select=0
                            self.tempTerritoryList=[]
                            if chemin and pays2.id != pays1.id:
                                self.Round.deplacer(pays1,pays2,self.troopCount)
                                self.Round.next()
                    #affichage des troupes
                    self.textList=[]
                    troopDisplay(self.textList,territorySprites,self.map)
                    #break
            except ValueError as e:
                pass #pas propre

            #HUD
            self.interfaceText=[]
            display_hud(self.troopCount,self.interfaceText,self.Round,(75,territorySprites[0].map_pays.get_height()+10),hide)
            pygame.display.flip()

#############################
def text_objects(text, font,color=(0,0,0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(pygameWindow, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            Win.functions.append(action)
    else:
        pygame.draw.rect(pygameWindow, ic,(x,y,w,h))

    smallText = pygame.font.Font(None,15)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    pygameWindow.blit(textSurf, textRect)



# Color setter
def color_surface(sprite,color,alpha):
    for x in range(0,sprite.bounds.width):
        for y in range(0,sprite.bounds.height):
            if sprite.map_pays.get_at((sprite.bounds.x+x,sprite.bounds.y+y))!=(0,0,0):
                sprite.map_pays.set_at((sprite.bounds.x+x,sprite.bounds.y+y),color)
                sprite.map_pays.set_alpha(alpha)

def add_text(layer,message,pos,font,color=(0,0,0)):
    textSurf, textRect = text_objects(message, font,color)
    textRect.topleft = pos
    layer.append([textSurf, textRect])

# Update troop visual count
def troopDisplay(textList,sprites,Map):
    smallText = pygame.font.Font(None,13)
    for sprite in sprites:
        pays=Map.pays[sprite.id-1]
        textSurf, textRect = text_objects(str(pays.nb_troupes), smallText)
        textRect.center = sprite.bounds.center
        textList.append([textSurf, textRect])

def display_win(topLevel,players):
    bigText = pygame.font.Font(None,35)
    marge=50
    pos=(200,200)
    for p in players:
        if p.obj.get_state()==True:
            p_win=p
            #player win
            textSurf, textRect = text_objects(p_win.name+' win', bigText,p_win.color)
            textRect.topleft = pos
            pos=(pos[0],pos[1]+marge)
            topLevel.append([textSurf, textRect])
            #objective
            textSurf, textRect = text_objects('Objective '+p_win.obj.description, bigText,p_win.color)
            textRect.topleft = pos
            pos=(pos[0],pos[1]+marge)
            topLevel.append([textSurf, textRect])

def display_help(topLevel,colormap):
    bigText = pygame.font.Font(None,40)
    marge=50
    pos=(200,200)
    add_text(topLevel,'ESC : exit game',pos,bigText,colormap.white)
    pos=(pos[0],pos[1]+marge)
    add_text(topLevel,'n : next phase',pos,bigText,colormap.white)
    pos=(pos[0],pos[1]+marge)
    add_text(topLevel,'p : next player turn',pos,bigText,colormap.white)
    pos=(pos[0],pos[1]+marge)
    add_text(topLevel,'h : show/hide help menu',pos,bigText,colormap.white)
    pos=(pos[0],pos[1]+marge)
    add_text(topLevel,'d : show/hide quest',pos,bigText,colormap.white)
    pos=(pos[0],pos[1]+marge)
    add_text(topLevel,'u : use your cards',pos,bigText,colormap.white)

# Player interface text updates
def display_hud(troopCount,interfaceText,Round,pos,hide):
    smallText = pygame.font.Font(None,15)
    marge=20
    col=[100,400,700,1000]
    row=pos[1]
    
    textSurf, textRect = text_objects('Turn : '+str(Round.num), smallText)
    textRect.topleft = pos
    interfaceText.append([textSurf, textRect])
    textSurf, textRect = text_objects('Player : ',smallText)
    pos=(pos[0],pos[1]+marge)
    textRect.topleft = pos
    interfaceText.append([textSurf, textRect])
    textSurf, textRect = text_objects(Round.players[Round.player_turn-1].name, smallText,Round.players[Round.player_turn-1].color)
    textRect.topleft = (pos[0]+70,pos[1])
    interfaceText.append([textSurf, textRect])
    textSurf, textRect = text_objects('Phase : '+Round.list_phase[Round.phase], smallText)
    pos=(pos[0],pos[1]+marge)
    textRect.topleft = pos
    interfaceText.append([textSurf, textRect])
    textSurf, textRect = text_objects('Troops per turn : '+str(Round.players[Round.player_turn-1].sbyturn), smallText)
    pos=(pos[0],pos[1]+marge)
    textRect.topleft = pos
    interfaceText.append([textSurf, textRect])
    textSurf, textRect = text_objects('Troops to deploy : '+str(Round.players[Round.player_turn-1].nb_troupes), smallText)
    pos=(pos[0],pos[1]+marge)
    textRect.topleft = pos
    interfaceText.append([textSurf, textRect])
    textSurf, textRect = text_objects('# of Selected Troops : '+str(troopCount), smallText)
    pos=(pos[0],pos[1]+marge)
    textRect.topleft = pos
    interfaceText.append([textSurf, textRect])

    #Player objectives
    textSurf, textRect = text_objects('Objective(s) ', smallText)
    pos=(col[1],row)
    textRect.topleft = pos
    interfaceText.append([textSurf, textRect])
    if hide==False:
        try:
            textSurf, textRect = text_objects(str(Round.players[Round.player_turn-1].obj.description), smallText)
        except AttributeError as e:
            print (e.args)
        pos=(col[1],row+marge)
        textRect.topleft = pos
        interfaceText.append([textSurf, textRect])
        try:
            textSurf, textRect = text_objects('Status : '+str(Round.players[Round.player_turn-1].obj.get_state()), smallText)
        except AttributeError as e:
            print (e.args)
        pos=(col[1],row+2*marge)
        textRect.topleft = pos
        interfaceText.append([textSurf, textRect])

    # Player cards
    textSurf, textRect = text_objects('Cards ', smallText)
    pos=(col[1],row+3*marge)
    textRect.topleft = pos
    interfaceText.append([textSurf, textRect])
    if hide==False:
        textSurf, textRect = text_objects(str(Round.players[Round.player_turn-1].cards), smallText)
        pos=(col[1],row+4*marge)
        textRect.topleft = pos
        interfaceText.append([textSurf, textRect])

    pos=(col[3],row)
    textSurf, textRect = text_objects('Continent Bonuses', smallText)
    textRect.topleft = pos
    interfaceText.append([textSurf, textRect])
    for i,c in enumerate(Round.map.continents):
        pos=(col[3],row+(i+1)*marge)
        textSurf, textRect = text_objects(c.name+' '+str(c.bonus), smallText)
        textRect.topleft = pos
        interfaceText.append([textSurf, textRect])

def display_continent(cont,temp_layer,territorySpriteLayer):
    for p in cont.pays:
        temp_layer.append(next((x.map_pays for x in territorySpriteLayer if x.id == p.id), None))

def save_game(obj_lst):
    with open('saved_game', 'wb') as f:
        pickle.dump(obj_lst, f)
        print('Game has been saved')

def restore_game(obj_lst):
    # Getting back the objects:
    with open('saved_game','rb') as f:
        obj_lst=pickle.load(f)
        print('Game has been restored')


def roll_dices(Win,pertes,number,x,y):
    L=[]
    for i,d in enumerate(number):
        de=pygame.image.load(c.dicePath+str(d)+".png").convert_alpha()
        resize_de=pygame.transform.scale(de,(c.diceSize,c.diceSize))
        L.append([resize_de,Win.pygameWindow.blit(resize_de,(i*c.diceSize*1.1+x,y))])

    for i_p in range(0,pertes):
        deadhead=pygame.image.load(c.dicePath+c.deadImage).convert_alpha()
        resize_dh=pygame.transform.scale(deadhead,(c.diceSize,c.diceSize))
        L.append([resize_dh,Win.pygameWindow.blit(resize_dh,(x-(i_p+1)*c.diceSize*1.1,y))])
    Win.dices.extend(L) 



# Secondary run, used for debugging
if __name__ == '__main__':
    from tkinter import *
    import random
    import copy
    
    from Map import Map
    from Player import Player
    from Goal import Goal
    from Objective import Objective
    from Card import Card
    from Round import Round

    import Constants as c

    # Test map initialization
    tempMap = Map('Terre')
    Continents=tempMap.continents
    T=Round(3,tempMap)
    T.start_deploy()
    print(T.distrib_pays(tempMap.pays))
    T.print_players()

    Colors=ColorMap()
    T.players[0].color=Colors.dark_purple
    T.players[1].color=Colors.dark_green
    T.players[2].color=Colors.dark_red
##    T.players[3].color=Colors.white
    # T.players[4].color=Colors.yellow
    # T.players[5].color=Colors.cian
    
    T.players[0].name='Duncan'
    T.players[1].name='Isaac'
    T.players[2].name='Finn'
##    T.players[3].name='Kevin'
    # T.players[4].name='Anna'
    # T.players[5].name='Justin'

    pygame.init()
    clock = pygame.time.Clock()
    pygameWindow = pygame.display.set_mode((c.windowLength, c.windowWidth))
    Win=Game(pygameWindow,T)
    Win.game.nb_joueurs=3
    Win.game.joueurs=['TestPlayer1','TestPlayer2','TestPlayer3']
    Win.functions.append(Win.run)

    Win.display()
