import random
from Card import Card
from Player import Player
from Goal import Goal
from Objective import Objective

class Round():
    def __init__(self,nb_players,M):
        self.game_finish=False
        self.num=0
        self.nb_players=nb_players
        self.ordre=list(range(1,nb_players+1))
        random.shuffle(self.ordre)
        self.nb_pays=M.nb_pays
        self.players=[]

        for k in range(0,nb_players):
            self.players.append(Player(k+1,M,self))

        #assigns playergoals
        self.goal=Goal(M,self)
        for k in range(0,nb_players):
            self.players[k].obj=Objective(self.goal,self.players[k])
        self.id_ordre=0
        self.map=M
        self.list_phase=['Placement','Attack','Movement']
        self.phase=0
        self._player_=self.ordre[self.id_ordre]

    def next(self):
        if self.players[self.player_turn-1].nb_troupes>0:
            raise ValueError('Need to deploy',self.players[self.player_turn-1].nb_troupes)

        if self.num==0: #placement phase
            self.id_ordre=(self.id_ordre+1)%len(self.ordre)
            if self.id_ordre==0:
                self.num+=1
                self.phase=(self.phase+1)%len(self.list_phase)
                
        elif self.num==1:#attack phase
            self.phase=(self.phase+1)%len(self.list_phase)
            if self.phase == 0 :
                self.phase+=1
                self.id_ordre=(self.id_ordre+1)%len(self.ordre)

                #update territory info if captured
                self.players[self.player_turn-1].win_land=False
                if self.id_ordre==0:
                    self.num+=1
                    self.phase=0

                    #updates reinforcement troops for start of player turn
                    self.players[self.player_turn-1].nb_troupes+=self.players[self.player_turn-1].sbyturn
        else:
            self.phase=(self.phase+1)%len(self.list_phase)
            if self.phase == 0 :
                self.id_ordre=(self.id_ordre+1)%len(self.ordre)

                #update territory captured boolean
                self.players[self.player_turn-1].win_land=False

                 #updates reinforcement troops for start of player turn
                self.players[self.player_turn-1].nb_troupes+=self.players[self.player_turn-1].sbyturn
                if self.id_ordre==0:
                    self.num+=1
                    
        print('Turn Number :', self.num,'order',self.ordre,'player turn', self.ordre[self.id_ordre])
        print(self.list_phase[self.phase])

    def next_player(self):
        if self.num==0: #initial placement phase
            self.id_ordre=(self.id_ordre+1)%len(self.ordre)
            if self.id_ordre==0:
                self.num+=1
                self.phase=(self.phase+1)%len(self.list_phase)
                
        elif self.num==1:#skip placement
            self.phase=1
            self.id_ordre=(self.id_ordre+1)%len(self.ordre)
            self.players[self.player_turn-1].win_land=False
            if self.id_ordre==0:
                self.num+=1
                self.phase=0
                self.players[self.player_turn-1].nb_troupes+=self.players[self.player_turn-1].sbyturn

        else:
            #move to next player turn
            self.id_ordre=(self.id_ordre+1)%len(self.ordre)
            self.phase=0
            self.players[self.player_turn-1].win_land=False
            self.players[self.player_turn-1].nb_troupes+=self.players[self.player_turn-1].sbyturn
            if self.id_ordre==0:
                self.num+=1

    def start_deploy(self):
        if self.nb_players==3:
            nb_troupes=35
        elif self.nb_players==4:
            nb_troupes=30
        elif self.nb_players==5:
            nb_troupes=25
        elif self.nb_players==6:
            nb_troupes=20
        else:
            print('Invalid # of troops selected...')
        for p in self.players:
            p.nb_troupes=nb_troupes

    #method distributes countries among # of players
    def distrib_pays(self,pays):
        lst_id_pays=[]
        for k in pays:
            lst_id_pays.append(k.id)
        random.shuffle(lst_id_pays)
        n=self.nb_pays//self.nb_players
        for idx,i in enumerate(range(0, len(lst_id_pays),n)):
            if idx<self.nb_players:
                self.players[idx].pays=lst_id_pays[i:i+n]
            else:
                for pays_restant in lst_id_pays[i:i+n]:  #after distribution, remaing countrys randomly assigned
                    self.players[random.randint(0,self.nb_players-1)].pays.append(pays_restant)
        for p in self.players:
            for pays in p.pays:
                self.map.pays[pays-1].id_player=p.id
                self.map.pays[pays-1].nb_troupes=1 #min 1 troop per territory
                p.nb_troupes-=1
        return lst_id_pays

    def throw_dices(self,atck,defense):
        d_a=[]
        d_b=[]
        pertes=[0,0,d_a,d_b] #attacker deaths, defender deaths
        
        for k in range(0,atck):
            d_a.append(random.randint(1,6))
        d_a.sort(reverse=True)
        for k in range(0,defense):
            d_b.append(random.randint(1,6))
        d_b.sort(reverse=True)
        
        for k in range(0,min(atck,defense)):
            if d_b[k]<d_a[k]: #on attacker win
                pertes[1]=pertes[1]+1
            else:
                pertes[0]=pertes[0]+1
        return pertes

    def attaque(self,pays_a,pays_d,nb_attaquants):
        res_l=[]
        while(True):
            if nb_attaquants>2:
                dice_atck=3
            elif nb_attaquants>1:
                dice_atck=2
            elif nb_attaquants>0:
                dice_atck=1
            else:
                raise ValueError('not enough troops:',nb_attaquants)
            if pays_d.nb_troupes>1:
                dice_def=2
            elif pays_d.nb_troupes>0:
                dice_def=1
            res=self.throw_dices(dice_atck,dice_def)
            print(res)
            res_l.append(res)
            pays_a.nb_troupes-=res[0]
            nb_attaquants-=res[0]
            pays_d.nb_troupes-=res[1]

            if nb_attaquants==0: #attack failed
                return False,res_l
            
            elif pays_d.nb_troupes==0: #territory captured successfuly
                
                #update list of territories for players
                self.players[pays_a.id_player-1].pays.append(pays_d.id)
                self.players[pays_d.id_player-1].pays.remove(pays_d.id)
                
                #update captured territor id
                pays_d.id_player=pays_a.id_player
                
                #moves surviving troops to new territory, remove from old
                self.deplacer(pays_a,pays_d,dice_atck)
                
                #attacjer gets a card if it is the first captured territory this turn
                if self.players[pays_a.id_player-1].win_land==False:
                    self.players[pays_a.id_player-1].win_land=True
                    
                    #if player has 5+ cards, card is discarded
                    if len(self.players[pays_a.id_player-1].cards)>4:
                        self.players[pays_a.id_player-1].del_card(0)
                        
                    self.players[pays_a.id_player-1].cards.append(Card())
                return True,res_l

    #remove troops from old territory, add survivors to new
    def deplacer(self,pays_ori,pays_dest,nb_troupes):
        pays_ori.nb_troupes-=nb_troupes
        pays_dest.nb_troupes+=nb_troupes

    #troop count updater
    def placer(self,pays,nb_troupes):
        player=next((p for p in self.players if p.id == pays.id_player), None)
        if(player.nb_troupes-nb_troupes<=0):
            pays.nb_troupes+=player.nb_troupes
            player.nb_troupes-=player.nb_troupes
            self.next()
        else:
            player.nb_troupes-=nb_troupes
            pays.nb_troupes+=nb_troupes

    def print_players(self):
        for p in self.players:
            p.print_carac()

    #setter for live text update
    @property
    def player_turn(self):
        return self.ordre[self.id_ordre]

    def print_pays(self):
        for pays in self.pays:
            pays.print_carac()

    def chemin_exist(self,pays_joueur,pays1,pays2):
        pays_reachable=[]
        if pays1.id in pays_joueur:
            pays_reachable.append(pays1.id)
            self.parcours_profondeur(pays1,pays_joueur,pays_reachable)
            if pays2.id in pays_reachable:
                print('A path exists')
                return True
            else:
                print('no valid path')
                return False
        else:
            print('player cannot select this territory')
            return False

    def parcours_profondeur(self,pays,pays_joueur,pays_reachable):
        for p_id in pays.voisins:
            if p_id in pays_joueur and p_id not in pays_reachable:
                pays_reachable.append(p_id)
                self.parcours_profondeur(self.pays[p_id-1],pays_joueur,pays_reachable)
