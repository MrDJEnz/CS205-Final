class Player():
    def __init__(self,id,Map,turns):
        self.id=id
        self.nb_troupes=0
        self.name=""
        self.pays=[]
        self._bonus=0
        self._sbyturn=0
        self._isalive=True
        self.color=(0,0,0)
        self.map=Map
        self.turns=turns
        self.obj=None
        self.cards=[]
        self.win_land=False

    def use_best_cards(self):
        if self.turns.list_phase[self.turns.phase]=='placement':
            nb_s=[x for x in self.cards if x.type==x.types[0]]
            nb_h=[x for x in self.cards if x.type==x.types[1]]
            nb_c=[x for x in self.cards if x.type==x.types[2]]
            if len(nb_s)>0 and len(nb_h)>0 and len(nb_c)>0:
                self.use_cards([nb_s[0],nb_h[0],nb_c[0]]) #if user has 3 special cards
            elif len(nb_c)>2:#cannon type
                self.use_cards([nb_c[0],nb_c[1],nb_c[2]])
            elif len(nb_h)>2:#calvary type
                self.use_cards([nb_h[0],nb_h[1],nb_h[2]])
            elif len(nb_s)>2:#soldier type
                self.use_cards([nb_s[0],nb_s[1],nb_s[2]])
            else:#otherwise cannot
                print('No valid combination of cards')
        else:
            print('Cards can be traded in during the placement phase')

    #take only 3 cards in input
    def use_cards(self,cards):
        #triple set
        if cards[0].type==cards[1].type and cards[1].type==cards[2].type and cards[0].type==cards[2].type:
            self.nb_troupes+=cards[0].bonus
            self.cards.remove(cards[0])
            self.cards.remove(cards[1])
            self.cards.remove(cards[2])
        #matching triple
        elif cards[0].type!=cards[1].type and cards[1].type!=cards[2].type and cards[0].type!=cards[2].type:
            self.nb_troupes+=cards[0].max_bonus
            self.cards.remove(cards[0])
            self.cards.remove(cards[1])
            self.cards.remove(cards[2])

    def del_card(self,card_index):
        self.cards.pop(card_index)

    def print_carac(self):
        print(self.id,self.name,self.nb_troupes,self.sbyturn,self.pays)

    #setters updates display as soon as called
    @property
    def sbyturn(self):
        return max(3,len(self.pays)//3+self.bonus)

    @property
    def bonus(self):
        b=0
        for c in self.map.continents:
            player_have_cont=True
            for pays in c.pays:
                if pays.id not in self.pays:
                    player_have_cont=False
                    break
            if player_have_cont:
                b+=c.bonus
        return b

    #boolena getter for territory check
    @property
    def isalive(self):
        if len(self.pays)>0:
            return True
        else:
            return False
