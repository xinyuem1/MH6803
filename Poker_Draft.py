import random
# from typing_extensions import Self
import pandas as pd


class Poker: #initialize cards and draw() from the top
    def __init__(self):
        suits = ["♥", "♠", "♣", "♦"]
        points = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        #box = []
        #cards = []
        n = 51

        box = [i+j for i in suits for j in points]

        '''
        for i in suits:
            for j in points:
                k = i + j
                box.append(k)
        while n >= 0:
            index = random.randint(0, n)
            cards.append(box[index])
            box.pop(index)
            n -= 1
        '''
        random.shuffle(box)

        self.c = box
        self.t = -1
        print(self.c)

    

    def draw(self):
        self.t += 1
        return self.c[self.t]


P = Poker()        


class ComputerPlayer:
    # record player's status
    def __init__(self):
        self.name = None    #player name
        self.alive = True #alive status
        self.fold = False   #fold or not
        self.allin = False  #allin or not
        self.chips = 500    #chips total
        self.bet = 0    #total bet amount
        self.seat = None    #seat no.
        self.hands = [] #hand cards
        self.score = 0  #score from card type
        self.type = None    #card type
        self.blind = True   #small blind/big blind
        self.need = 0


        
    def w_init(self):   #initialize new round
        self.need = 0
        self.fold = False
        self.allin = False
        self.bet = 0
        self.hands = []
        self.score = 0
        self.type = None
        self.blind = True
        if self.chips == 0:
            self.alive = 0
    
    
    
    def r_hands(self):  #draw cards(each player)
        self.hands = [P.draw(), P.draw()]



    def w_st(self, s_t):    # store card type and corresponding score
        self.score = s_t[0]
        self.type = s_t[1]
        

    def bet_strategy(self, board, need, stage):
        hand_num = (self.hands[0][1], self.hands[1][1])
        bet_amount = 0
        board_num = [i[1]for i in board]
        L = ['A', '2', '3', '4', '5', '6', '7']
        r1 = random.random()
        r2 = random.random()
        # if any one pair with existing cards, high chance on bet/allin
        if self.hands[0][1] in board_num or self.hands[1][1] in board_num:
            r_fold = 0
            r_add = 0.1

        # elif high number on card, still high chance but lower than pairs
        elif hand_num in [("A", "A"), ("A", "K"), ("A", "K"), ("K", "K"), (("Q", "Q"))]:
            r_fold = 0.1
            r_add = 0.2
            
        elif need > 0.6*self.chips:
            r_fold = 0.7
            r_add = 0.05
            
        elif hand_num[0] == hand_num[1]:
            r_fold = 0.2
            r_add = 0.1

        # elif player only hold small cards
        elif (hand_num[0] in L) and (hand_num[1] in L):
            r_fold = 0.6
            r_add = 0
            if stage in ['river', 'turn']:
                r_fold = 1

        # other cards
        else:
            r_fold = 0.3
            r_add = 0.05
        
        if stage == 'preflop':
            if self.hands[0][0] == self.hands[1][0]:
                r_fold -= 0.1
                r_add += 0.05
        
        # need random on bet or not&bet amount
        if r1 < r_fold:
            self.fold = True
        else:
            if r2 < r_add:
                bet_amount = need
            else:
                bet_amount = need + self.chips * random.random() * 0.5

        # if bet, return (False, bet amount); if fold, return (True, 0)
        return bet_amount


        
    # decide action for player
    def decision(self, stage, pod, highbet, board):
        bet = 0 # former bet amount
        needed = highbet - self.bet #least bet amount

        if self.alive:
    
            if (not self.fold) and (not self.allin):
                
                if stage == 'preflop': #preflop round
                    if self.blind:  #bet if SBlind/BBlind
                        if self.seat == 'SB':
                            bet = 1
                        elif self.seat == 'BB':
                            bet = 2
                        else:
                            # if need random 
                            bet = self.bet_strategy(board, needed, stage)
                        self.blind = False
                    else:
                        bet = self.bet_strategy(board, needed, stage)                  
                else:
                    bet = self.bet_strategy(board, needed, stage)
                # if intended bet amount larger than chips, indicate "all in"
                bet = round(bet)
                if bet > self.chips:
                    bet = self.chips
                    self.allin = True
                self.chips -= bet
                self.bet += bet
                            
            #return[bet amount，total be amount，all in or not
            return [bet, self.bet, self.allin, self.fold] 
            
        
        
        
        
class You: ###mutual port
    # record player's status
    def __init__(self):
        self.name = None    #player name
        self.alive = True #alive status
        self.fold = False   #fold or not
        self.allin = False  #allin or not
        self.chips = 500    #chips total
        self.bet = 0    #total bet amount
        self.seat = None    #seat no.
        self.hands = [] #hand cards
        self.score = 0  #score from card type
        self.type = None    #card type
        self.blind = True   #small blind/big blind
        self.need = 0
        self.bet_amount = 0

        
    def w_init(self):   #initialize new round
        self.fold = False
        self.allin = False
        self.bet = 0
        self.hands = []
        self.score = 0
        self.type = None
        self.blind = True
        self.need = 0
        self.bet_amount = 0
        if self.chips == 0:
            self.alive = 0
            
            
    def r_hands(self):  #draw cards(each player)
        self.hands = [P.draw(), P.draw()]


    def w_st(self, s_t):    # store card type and corresponding score
        self.score = s_t[0]
        self.type = s_t[1]
        
    
    def call(self, highbet=0):
        self.need = highbet - self.bet
        self.bet_amount = self.need
        print("call", self.need, self.bet_amount)

    def rise(self, bet):
        self.bet_amount = bet
        print("amount", self.bet_amount)

    def decision(self, stage, pod, highbet, board):
        bet = 0  # former bet amount
        self.need = highbet - self.bet  # least bet amount

        if self.alive:
            if (not self.fold) and (not self.allin):
                if stage == 'preflop':  # preflop round
                    if self.blind:  # bet if SBlind/BBlind
                        if self.seat == 'SB':
                            bet = 1
                        elif self.seat == 'BB':
                            bet = 2
                        else:
                            # if need random
                            bet = self.bet_amount
                        self.blind = False
                else:
                    bet = self.bet_amount
                # if intended bet amount larger than chips, indicate "all in"
                bet = round(bet)
                if bet >= self.chips:
                    bet = self.chips
                    self.allin = True
                self.chips -= bet
                self.bet += bet

            # return[bet amount，total be amount，all in or not
            print(f"{self.name}, bet:{bet}, bet_amount{self.bet_amount}, need{self.need}")

            return [bet, self.bet, self.allin, self.fold]







           
           
           
# deal cards
class Dealer: 
    def __init__(self, n):
        self.winner = ''
        # store player information
        self.players = [] 
        HP = You()
        P1 = ComputerPlayer()
        P2 = ComputerPlayer()
        P3 = ComputerPlayer()
        P4 = ComputerPlayer()
        P5 = ComputerPlayer()
        P6 = ComputerPlayer()
        P7 = ComputerPlayer()
        P8 = ComputerPlayer()
        P9 = ComputerPlayer()
        P10 = ComputerPlayer()
        l_P = [HP, P1, P2, P3, P4, P5, P6, P7, P8, P9]
        name = ['You', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10']
        for i in range(n):
            l_P[i].name = name[i]
            self.players.append(l_P[i])
        self.pod = 0 #prize pool amount
        self.board = [] #public card (five cards in the middle)
        self.stage = 'begin' #current stage
        self.order = [] #player order
        self.highbet = 0 #current highest bit
        self.done = 0 #currents no. of player finished decisions
        self.actionable = 0
        
        
    # initialize new round
    def w_init(self): 
        self.pod = 0
        self.board = []
        self.highbet = 0
        self.done = 0
        self.actionable = len(self.players)
        
        
        
    def left(self): #return current alive player list
        l = []
        for i in range(len(self.players)):
            if self.players[i].alive:
                l.append(i)
        return l
    
    
    
    def notfold(self): #list of player no. who didn't fold
        l = []
        for i in range(len(self.players)):
            if not self.players[i].fold:
                l.append(i)
        return l
                

    #game finished, computer player wins
    def end(self): 
        rank = len(self.left()) + 1
        print('You are #' + str(rank))
        print('Congratulations!')
        
        
    #game finished, you win
    def win(self): 
        print('Winner Winner')
        print('Chicken Dinner!')
        
        
    #juage on cards, return [highest score from all possible card type, corresponding card type name]
    def judge(self, hands): 
        score = 0
        flush = False
        straight = False
        Types = None
        l = self.board + hands
        suits = [i[0] for i in l]
        points = [i[1] for i in l]
        
        H = []
        S = []
        C = []
        D = []
        P_1 = []
        P_2 = []
        P_3 = []
        P_4 = []
        P_5 = []
        P_6 = []
        P_7 = []
        P_8 = []
        P_9 = []
        P_10 = []
        P_11 = []
        P_12 = []
        P_13 = []
        P_14 = []
        
        for i in range(len(suits)):
            if suits[i] == "♥":
                H.append(i)
            if suits[i] == "♠":
                S.append(i)
            if suits[i] == "♣":
                C.append(i)
            if suits[i] == "♦":
                D.append(i)
        for i in range(len(points)):
            if points[i] == 'A':
                P_1.append(i)
                P_14.append(i)
            if points[i] == '2':
                P_2.append(i)
            if points[i] == '3':
                P_3.append(i)
            if points[i] == '4':
                P_4.append(i)
            if points[i] == '5':
                P_5.append(i)
            if points[i] == '6':
                P_6.append(i)
            if points[i] == '7':
                P_7.append(i)
            if points[i] == '8':
                P_8.append(i)
            if points[i] == '9':
                P_9.append(i)
            if points[i] == '10':
                P_10.append(i)
            if points[i] == 'J':
                P_11.append(i)
            if points[i] == 'Q':
                P_12.append(i)
            if points[i] == 'K':
                P_13.append(i)
            
        Suits = [H, S, C, D]
        Points = [P_1, P_2, P_3, P_4, P_5, P_6, P_7, P_8, P_9, P_10, P_11, P_12, P_13, P_14]
        
        #four of kind
        for i in Points:
            if len(i) == 4:
                score = 7E8
                
        # full house   
        if score == 0:
            for i in range(len(Points)):
                if len(Points[i]) == 3:
                    for j in range(len(Points)):
                        if i != j:
                            if len(Points[j]) >= 2:
                                score = 6E8 + max([i, j])
                        
        # flush
        if score == 0:
            h1 = 0
            h2 = 0
            h3 = 0
            h4 = 0
            h5 = 0
            for i in Suits:
                if len(i) > 4:
                    nf = i
                    for j in range(len(Points)):
                        if len(Points[j]) == 3:
                            h5 = h4
                            h4 = h3
                            h3 = j
                            h2 = j
                            h1 = j
                        if len(Points[j]) == 2:
                            h5 = h4
                            h4 = h3
                            h3 = h2
                            h2 = j
                            h1 = j
                        if len(Points[j]) == 2:
                            h5 = h4
                            h4 = h3
                            h3 = h2
                            h2 = h1
                            h1 = j
                    score = 5E8 + 20000*h1 + 2000*h2 + 200*h3 + 20*h4 + h5
                    flush = True
                
        # straight
        if score == 0 or flush:
            for i in range(11):
                if len(Points[i]) > 0:
                    n = 0
                    while True:
                        n += 1
                        if i+n <= 13:
                            if len(Points[i+n]) == 0:
                                break
                        if i+n > 13:
                            break
                    if n == 5:
                        score = 4E8 + i + n
                        straight = True
                        ns = []
                        for j in range(i, i+n):
                            ns.append(Points[j])
                        
        
        # three of kind
        if score == 0:
            h1 = 0
            h2 = 0
            for i in range(len(Points)):
                if len(Points[i]) == 3:
                    for j in range(len(Points)):
                        if len(Points[j]) == 1:
                            h2 = h1
                            h1 = j
                            score = 3E8 + h1*20 + h2
        
        # two plairs
        if score == 0:
            n = 0
            p1 = 0
            p2 = 0
            for i in range(len(Points)):
                if len(Points[i]) == 2:
                    n += 1
                    p2 = p1
                    p1 = i
            if n >= 2:
                for j in range(len(Points)):
                    if len(Points[j]) > 0:
                        score = 2E8 + p1*200 + p2*20 + j
                        
        # one pair
        if score == 0:
            h1 = 0
            h2 = 0
            h3 = 0
            for i in range(len(Points)):
                if len(Points[i]) == 2:
                    for j in range(len(Points)):
                        if len(Points[j]) > 0:
                            h3 = h2
                            h2 = h1
                            h1 = j
                    score = 1E8 + i*2000 + h1*200 + h2*20 + h1
                        
        # high card
        if score == 0:
            h1 = 0
            h2 = 0
            h3 = 0
            h4 = 0
            h5 = 0
            for i in range(len(Points)):
                if len(Points[i]) == 1:
                    h5 = h4
                    h4 = h3
                    h3 = h2
                    h2 = h1
                    h1 = i
            score = h1*20000 + h2*2000 + h3*200 + h4*20 + h5
            
        # straight flush
        if flush and straight:
            s_f = True
            for i in ns:
                if len(i) == 1:
                    if i[0] not in nf:
                        s_f = False
                else:
                    n = 0
                    for j in i:
                        if j not in nf:
                            n += 1
                    if n == len(i):
                        s_f = False
            if s_f:
                for i in range(11):
                    if len(Points[i]) > 0:
                        n = 0
                        while True:
                            n += 1
                            if i+n <= 13:
                                if len(Points[i+n]) == 0:
                                    break
                            if i+n > 13:
                                break
                        if n == 5:
                            score = 8E8 + i + n
        
        if score < 1E8:
            Types = 'High Card'
        if score >= 1E8 and score < 2E8:
            Types = 'One Pair'
        if score >= 2E8 and score < 3E8:
            Types = 'Two Pair'
        if score >= 3E8 and score < 4E8:
            Types = 'Three of a Kind'
        if score >= 4E8 and score < 5E8:
            Types = 'Straight'
        if score >= 5E8 and score < 6E8:
            Types = 'Flush'
        if score >= 6E8 and score < 7E8:
            Types = 'Full House'
        if score >= 7E8 and score < 8E8:
            Types = 'Four of a Kind'
        if score >= 8E8:
            Types = 'Straight Flush'
        if score == 8E8 + 14:
            Types = 'Royal Straight Flush'
        
        return [score, Types]
    


    def settle(self): 
        if len(self.notfold()) == 1:
            self.players[self.notfold()[0]].chips += self.pod
            self.pod = 0
            self.stage = "begin"
        else:
            #score list(order by player no.)
            s = [] 

            # no. of player who did all in 
            a = 0 

            # no. of player who share prize pool
            e = 0 
            for i in self.players:
                if i.allin:
                    a += 1
            
            for i in range(len(self.players)): 
                if not self.players[i].fold:
                    # score, card type
                    s_t = self.judge(self.players[i].hands)
                    self.players[i].w_st(s_t)
                    s.append(s_t[0])
                else:
                    s.append(0)

            # prioritize all in player
            while a > 0: 
                for i in range(len(self.players)):

                    # if all in player win, gain double prizes
                    if self.players[i].allin: 
                        if s[i] < max(s):
                            a -= 1
                        else:
                            if self.pod >= self.players[i].bet * 2:
                                self.players[i].chips = self.players[i].bet * 2
                                self.pod -= self.players[i].chips
                                s[i] = 0
                                a -= 1
                            else:
                                self.players[i].chips += self.pod
                                self.pod = 0
                                a = 0

            # if prize pool not empty, goes to all in player with highest score
            if self.pod > 0:
                for i in self.players:
                    if i.score == max(s):
                        e += 1

                bonus = round(self.pod / e)
                for i in self.players:
                    if i.score == max(s):
                        i.chips += bonus
                        self.winner = i.name

                self.pod = 0

        self.stage = 'begin'
        


          
    def begin(self): 
        # initialize parameters
        P.__init__()
        self.w_init()
        for i in self.players:
            i.w_init()
        
        # if human player not alive, end game
        if not self.players[0].alive: 
            self.end()
            self.stage = None
            
        else: 
            if len(self.left()) == 1:
                self.players = [self.players[0]]
                self.win()
                self.stage = None
                
            # if game not ended, remove all players from list, change SB/BB
            else: 
                l = self.left()
                s = []
                r = True
                for i in range(len(self.players)):
                    if self.players[i].seat == 'SB':
                        s.append(i)
                t = []
                for i in l:
                    t.append(self.players[i])
                if len(s) == 0:
                    self.players = t
                    self.players[0].seat = 'S'
                    self.players[1].seat = 'B'
                else:
                    for i in l:
                        if i > s[0]:
                            self.players[i].seat = 'S'
                            r = False
                            break
                    if r:
                        self.players[l[0]].seat = 'S'
                    self.players = t
                    if self.players[-1].seat == 'S':
                        self.players[0].seat = 'B'
                    else:
                        for i in range(len(self.players)):
                            if self.players[i].seat == 'S':
                                self.players[i+1].seat = 'B'
                                break
                for i in self.players:
                    if i.seat != 'S' and i.seat != 'B':
                        i.seat = None
                    elif i.seat == 'S':
                        i.seat = 'SB'
                    elif i.seat == 'B':
                        i.seat = 'BB'
                for i in range(len(self.players)):
                    if self.players[i].seat == 'SB':
                        n = i
                        self.order.clear()
                        while len(self.order) < len(self.players):
                            self.order.append(n)
                            if n == len(self.players) - 1:
                                n = 0
                            else:
                                n += 1
                self.stage = 'preflop'

              
    # players draw cards
    def preflop(self):
        for i in self.players:
            i.r_hands()
        self.done = 0
        self.actionable = len(self.players)
        B = False
        while self.actionable > 1:
            print("test",self.players[0].bet_amount)
            for i in self.order:
                if (not self.players[i].fold) and (not self.players[i].allin):
                    result = self.players[i].decision('preflop', self.pod, self.highbet, self.board)
                    self.pod += result[0]
                    if result[1] > self.highbet:
                        self.highbet = result[1]
                        self.done = 0
                    self.done += 1
                    if result[2] or result[3]:
                        self.actionable -= 1
                        self.done -= 1
                    if self.done >= self.actionable:
                        B = True
                        break
            if B:
                break

        # check if only one player not fold, settle account
        if len(self.notfold()) == 1: 
            self.settle()
        self.stage = 'flop'

            
    
    # flop round, flop first 3 cards from dealer
    def flop(self):
        print("test", self.players[0].bet_amount)
        self.board = [P.draw(), P.draw(), P.draw()]
        self.done = 0
        B = False
        while self.actionable > 1:
            for i in self.order:
                if (not self.players[i].fold) and (not self.players[i].allin):
                    result = self.players[i].decision('flop', self.pod, self.highbet, self.board)
                    self.pod += result[0]
                    if result[1] > self.highbet:
                        self.highbet = result[1]
                        self.done = 0
                    self.done += 1
                    if result[2] or result[3]:
                        self.actionable -= 1
                        self.done -= 1
                    if self.done >= self.actionable:
                        B = True
                        break
            if B:
                break
        if len(self.notfold()) == 1:
            self.settle()
        self.stage = 'turn'
    
    
    # turn card round (second last public card)
    def turn(self):
        print("test", self.players[0].bet_amount)
        self.done = 0
        self.board.append(P.draw())
        B = False
        while self.actionable > 1:
            for i in self.order:
                if (not self.players[i].fold) and (not self.players[i].allin):
                    result = self.players[i].decision('turn', self.pod, self.highbet, self.board)
                    self.pod += result[0]
                    if result[1] > self.highbet:
                        self.highbet = result[1]
                        self.done = 0
                    self.done += 1
                    if result[2] or result[3]:
                        self.actionable -= 1
                        self.done -= 1
                    if self.done >= self.actionable:
                        B = True
                        print('AAAAAAAAAA')
                        break
            if B:
                break
        if len(self.notfold()) == 1: 
            self.settle()
        self.stage = 'river'
     
        
     #river card round (last public card)
    def river(self): 
        self.done = 0
        self.board.append(P.draw())
        B = False
        while self.actionable > 1:
            for i in self.order:
                if (not self.players[i].fold) and (not self.players[i].allin):
                    result = self.players[i].decision('river', self.pod, self.highbet, self.board)
                    self.pod += result[0]
                    if result[1] > self.highbet:
                        self.highbet = result[1]
                        self.done = 0
                    self.done += 1
                    if result[2] or result[3]:
                        self.actionable -= 1
                        self.done -= 1
                    if self.done >= self.actionable:
                        B = True
                        break
            if B:
                break
        self.settle() 
        
        
    # loop until end of the game, save action and card record in csv file
    def flow(self):
        Round = 0
        Index = []
        C_L = []
        j = 0
        for i in self.players:
            j += 1
            C_L.append('name_' + str(j))
            C_L.append('seat_' + str(j))
            C_L.append('fold_' + str(j))
            C_L.append('all_in_' + str(j))
            C_L.append('chips_' + str(j))
            C_L.append('bet_' + str(j))
            C_L.append('hands_' + str(j))
            C_L.append('type_' + str(j))
            C_L.append('score_' + str(j))
        A = [[], [], [], []]
        for i in self.players:
            for k in range(9):
                A.append([])

        while self.players[0].alive and len(self.players) > 1:
            if self.stage == 'begin':
                Round += 1
                self.begin()
            elif self.stage == 'preflop':
                self.preflop()
            elif self.stage == 'flop':
                self.flop()
            elif self.stage == 'turn':
                self.turn()
            elif self.stage == 'river':
                self.river()

            Index.append(Round)
            A[0].append(self.stage)
            A[1].append(self.pod)
            A[2].append(self.highbet)
            A[3].append(self.board)

            for i in range(len(self.players)):
                A[i*9+4].append(self.players[i].name)
                A[i*9+5].append(self.players[i].seat)
                A[i*9+6].append(self.players[i].fold)
                A[i*9+7].append(self.players[i].allin)
                A[i*9+8].append(self.players[i].chips)
                A[i*9+9].append(self.players[i].bet)
                A[i*9+10].append(self.players[i].hands)
                A[i*9+11].append(self.players[i].type)
                A[i*9+12].append(self.players[i].score)

            self.get()

        for i in A:
            while len(i) < len(A[0]):
                i.append('')


        R = pd.DataFrame({'next_stage': A[0]
                          ,'pod': A[1]
                          ,'high_bet': A[2]
                          ,'board': A[3]
                          })
        for i in range(len(C_L)):
            R[C_L[i]] = A[i+4]
        R.index = Index
        R.to_csv('Record.csv', encoding="utf_8_sig")


    # run game
    def get(self):
        print('#######################')
        print('nextstage:', self.stage)
        print('board:', self.board)
        print('highbet:', self.highbet)
        print('pod:', self.pod)
        ALL = 0
        for i in self.players:
            print(i.name, i.seat, 'F:', i.fold, 'C:', i.chips, i.hands,  i.type, i.score)
            ALL += i.chips
        print('***', ALL + self.pod, '***')
           
        
        
            
#start game with 5 players 
# D = Dealer(7)
# D.flow()
#





