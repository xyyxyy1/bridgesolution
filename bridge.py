# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 10:04:00 2017

@author: xuyiyao
"""
import time
#import os
def completeSuit(suit):
    #13张牌
    suitcards = set()
    for num in range(2,15):
        suitcards.add((suit,num))
    return suitcards

def completeDeck():
    #52张牌
    deck = set()
    for suit in ['S','H','D','C']:
        for num in range(2,15):
            deck.add((suit,num))
    return deck
                
def nextDirec(direc):
    #下家关系
    if direc=='N':
        return "E"
    if direc=='E':
        return "S"
    if direc=='S':
        return "W"
    if direc=='W':
        return "N"    
    
def partner(direc):
    #同伴关系
    if direc=='N':
        return "S"
    if direc=='E':
        return "W"
    if direc=='S':
        return "N"
    if direc=='W':
        return "E" 

def winner(cards,trump,suit):
    #判断每轮赢家，赢张
    trumps = []
    orisuits = []
    for card in cards:
        if card[0] == trump :
            trumps.append(card)
        elif card[0] == suit :
            orisuits.append(card)
    num = 0
    if trumps:
        for card in trumps:
            if card[1]> num:
                num = card[1]
                winner = card[2]
        return (trump,num,winner)
    else:
        for card in orisuits:
            if card[1]> num:
                num = card[1]
                winner = card[2]
        return (suit,num,winner)

class playerCards(object):
    #单手牌类
    def __init__(self,S,H,D,C,direc):
        self.cardList = {}
        self.cardList["S"] = S
        self.cardList["H"] = H
        self.cardList["D"] = D
        self.cardList["C"] = C
        self.playedList = []
        self.direc = direc
        self.num = len(S)+len(H)+len(D)+len(C)

    def allCards(self):
        #剩余的所有牌
        opts = []
        for suit in self.cardList:
            for num in self.cardList[suit]:
                #单张牌，用duple形式，包含花色，大小，是哪家出的三部分信息
                opts.append((suit,num,self.direc))
        return opts

    def options(self,suit):
        #出某花色时所有可选择的牌
        opts = []
        if self.cardList[suit]:
            for num in self.cardList[suit]:
                
                opts.append((suit,num,self.direc))
        else:
            for othersuit in self.cardList:
                for num in self.cardList[othersuit]:
                    opts.append((othersuit,num,self.direc))
        return opts

    def printDeck(self):
        #打印剩余牌，用于调试
        for suit in self.cardList:
            print(suit,self.cardList[suit])
                

class deck(object):
    #整桌牌类
    def __init__(self,players,num):
        #根据初始牌，排除重复牌、多牌少牌，求出已打出的牌
        self.cardList = {}        
        cards = set()
        for player in players:            
            #player是playerCards类
            cardNum = 0
            for card in player.allCards():
                cardNum += 1
                if card[:2] in cards:
                    print("repeated card",card)
                cards.add(card[:2])
            if cardNum != num:
                print("wrong number of card %s" %(player.direc))
            direc = player.direc           
            self.cardList[direc] = player

        completedeck = completeDeck()
        if cards - completedeck:
            print("not bridge card")
        #初始化参数，依次为：已出过的牌（是集合，该集合中的牌没有记录是哪家的），当轮桌上的牌（是链表），单家初始张数（不随出牌改变），目前轮次
        self.turnedOver = completedeck - cards
        self.onTable = []
        self.num = num
        self.turn = 0
        
    def play(self,card):
        #某方打出一张牌
        if card[1] in self.cardList[card[2]].cardList[card[0]]:
            self.cardList[card[2]].cardList[card[0]].remove(card[1])
            self.cardList[card[2]].num -= 1
            self.cardList[card[2]].playedList.append(card)
            self.onTable.append(card)
            return card
        else:
            print("no card %s%d in player %s's hand" %card)
    
    def withdraw(self,direc):
        if self.cardList[direc].playedList:
        #撤回一张牌
            card = self.cardList[direc].playedList[-1]
            self.cardList[direc].num += 1
            self.cardList[direc].cardList[card[0]].append(card[1])
            self.cardList[direc].playedList = self.cardList[direc].playedList[:-1]
            self.onTable = self.onTable[:-1]
            
    def nextTurn(self):
        #每轮结束时，更新已出牌堆
        for card in self.onTable:
            self.turnedOver.add(card[:2])
        self.onTable = []
        self.turn += 1
        
    def previousTurn(self,direc):
        #回退已出牌堆
        self.onTable = []
        self.turn -= 1
        for num in range(4):
            direc = nextDirec(direc)
            card = self.cardList[direc].playedList[-1]
            self.turnedOver.remove(card[:2])
            self.onTable.append(card)  
        
    def big(self,direc):
        #找一张该方可出的能赢墩的大牌
        for card in self.cardList[direc].allCards():
            big = 1
            for num in range(card[1]+1,15):
                if (card[0],num) in self.turnedOver:
                    big = 0
                    break
            if big:
                return card
        return False
            
        
    def small(self,direc):
        #没有大牌时，找一张该方可出的小牌
        pass
    
    def equal(self,card1,card2,trump):
        #判断两张牌大小是否等价: 比较啰嗦，倒数第二轮禁掉        
        if card1[0] == card2[0]:
            #同花色，目前标准：两张之间的卡均在之前轮次已打出或在自己手中
            big = max(card1[1],card2[1])
            small = min(card1[1],card2[1])
            for num in range(small+1,big):
                if (card1[0],num) not in self.turnedOver and num not in self.cardList[card1[2]].cardList[card1[0]]:
                    #若某张卡既不在手中也未在之前打出，当它已在桌上且并不大时仍忽略它
                    if not self.onTable:
                        return False
                    find = 0
                    for card in self.onTable:
                        if card[:2] == (card1[0],num):
                            if card == winner(self.onTable,trump,self.onTable[0][0]):
                                return False  
                            else:
                                find = 1
                                break
                    if not find:
                        return False
            
            return True
        if card1[0] != card2[0]:
            #不同花色，目前标准：两门花色均非将牌，且均只有该家有
            if card1[0] == trump or card2[0] == trump:
                return False            
            for direc in self.cardList:
                if direc!= card1[2]:
                    if self.cardList[direc].cardList[card1[0]] or self.cardList[direc].cardList[card2[0]]:
                        return False
            return True 

    def allCardsDif(self,direc,trump):
        #某方剩余的所有不等价牌
        #if self.cardList[direc].num < 3:
            #return self.cardList[direc].allCards()
        opts = []
        #bigcard = self.big(direc)
        #if bigcard:
            #opts.append(bigcard)
        for newcard in self.cardList[direc].allCards():
            #if newcard != bigcard:
                equal = 0
                for card in opts:
                    if self.equal(card,newcard,trump):
                        equal = 1
                        break
                if not equal:
                    opts.append(newcard)
        return opts
                 
    def optionsDif(self,direc,suit,trump):
        #某方出某花色时可选择的不等价的牌
        #if self.cardList[direc].num < 3:
            #return self.cardList[direc].options(suit)
        opts = []
        if self.cardList[direc].cardList[suit]:            
            for num in self.cardList[direc].cardList[suit]:
                newcard = (suit,num,direc)
                equal = 0
                for card in opts:
                    if self.equal(card,newcard,trump):
                        equal = 1
                        break
                if not equal:
                    opts.append(newcard)
        else:
            for othersuit in self.cardList[direc].cardList:
                for num in self.cardList[direc].cardList[othersuit]:
                    newcard = (othersuit,num,direc)
                    equal = 0
                    for card in opts:
                        if self.equal(card,newcard,trump):
                            equal = 1
                            break
                    if not equal:
                        opts.append(newcard)
        return opts

    def printDeck(self):
        #格式化打印牌库，用于调试
        for key in self.cardList:            
            print(key)
            self.cardList[key].printDeck()
        print(self.onTable,self.turn)    

        
i = 0
j = 0  
# 用于计数递归调用次数
def playCard(deck,trump,direc,wintrumps,deal):
    #参量依次为：整桌牌库，将牌花色，当前出牌方，本方目前已赢墩，本方需要完成的墩
    total = deck.num  
    #双方总墩数    
    if deck.cardList[direc].num == 1:
        global i 
        i += 1
        if i % 100000 == 0:
            print('i',i)
        #结束条件1：出牌方只剩一张
        card = deck.cardList[direc].allCards()[0]
        suit = card[0]
        cards = [card]
        direc = nextDirec(direc)
        for num in range(3):
            card = deck.cardList[direc].allCards()[0]          
            cards.append(card)
            direc = nextDirec(direc)
        windirec = winner(cards,trump,suit)[2]
        #得到末轮赢家
        if windirec == direc or windirec == partner(direc):
           wintrumps += 1
        return wintrumps
        #返回分支南北，东西总赢张及末轮出牌
    
    #以下为结束条件2：AlphaBeta剪枝
    
    if wintrumps >= deal:
        global j 
        j += 1
        if j % 100000 == 0:
            print('j',j)
        #双方最佳结果出牌的一种可能性，剪枝时直接返回空
        return wintrumps
    
    #以下部分为一般情况  
        
    if not deck.onTable:
        #情况一：该轮出牌方，可以出手里任意牌
        cardlist = deck.allCardsDif(direc,trump)
        
    else:
        #情况二：该轮跟牌方
        suit = deck.onTable[0][0]
        cardlist = deck.optionsDif(direc,suit,trump)
        
    if len(deck.onTable)<3:
        #非末轮，此时出牌方一定转换                 
        for card in cardlist:             
            #遍历所有可能出牌，对于每种出牌，更新牌库，给出下一步各种参数             
            card = deck.play(card)
            newdirec = nextDirec(direc)
            newwintrumps = deck.turn - wintrumps            
            newdeal = total - deal + 1      
            newwintrumps = playCard(deck,trump,newdirec,newwintrumps,newdeal)            
                    
            #从子分支返回，先还原套牌，然后判断是否完成了定约
            deck.withdraw(direc)
            tempwintrumps = total - newwintrumps
            if tempwintrumps >= deal:
                return tempwintrumps
            
        return deal - 1
    
    else:
        #该轮已到末家，结算该轮赢家并清空桌面
        for card in cardlist:
            #遍历所有可能出牌
            card = deck.play(card)
            newdirec = winner(deck.onTable,trump,suit)[2]
            deck.nextTurn()
            #若不转换牌权
            if newdirec == direc or newdirec == partner(direc):
                newwintrumps = wintrumps + 1
                newdeal = deal
            #若转换牌权
            else:
                newwintrumps = deck.turn - wintrumps
                newdeal = total - deal + 1
            newwintrumps = playCard(deck,trump,newdirec,newwintrumps,newdeal)            
            #从子分支返回，先还原套牌，然后判断是否完成了定约
            deck.previousTurn(direc)
            deck.withdraw(direc)
            if newdirec == direc or newdirec == partner(direc):
                tempwintrumps = newwintrumps
            else:
                tempwintrumps = total - newwintrumps
            if tempwintrumps >= deal:
                return tempwintrumps
        
        #返回分支最佳策略本方总赢张及出牌
        return deal - 1
'''
cardN = playerCards([14,9,7],[8,7],[14,6,4,3,2],[13,5,2],"N")
cardE = playerCards([13,12,11],[12,11,10,6],[12,11,8,7],[9,4],"E")
cardS = playerCards([10,2],[14,13,5,4,3],[13,10],[14,8,6,3],"S")
cardW = playerCards([8,6,5,4,3],[9,2],[9,5],[12,11,10,7],"W")

cardN = playerCards([10,7],[2],[3,8],[7,6,11,4],"N")
cardE = playerCards([3,2],[11,10,8],[11,12],[12,8],"E")
cardS = playerCards([14],[14,13,5],[7,13],[9,13,14],"S")
cardW = playerCards([13,12],[12,9,6],[14],[10,5,3],"W")

cardN = playerCards([10,7],[2],[4,13],[4],"N")
cardE = playerCards([9],[11,10,8],[14,11],[],"E")
cardS = playerCards([14],[14,13,5],[7,10],[],"S")
cardW = playerCards([13,12],[12,9,6],[12],[],"W")

cardN = playerCards([2,3],[7],[],[],"N")
cardE = playerCards([5],[8,4],[],[],"E")
cardS = playerCards([],[],[3,4,6],[],"S")
cardW = playerCards([],[],[],[3,4,7],"W")
'''
cardN = playerCards([10,7],[2],[3,8],[7,6,11,4],"N")
cardE = playerCards([3,2],[14,10,8],[11,12],[14,8],"E")
cardS = playerCards([14],[11,13,5],[7,13],[9,13,12],"S")
cardW = playerCards([13,12],[12,9,6,4],[14],[10,5],"W")

cards = [cardN,cardE,cardS,cardW]
num = 9
deal = 5
deck = deck(cards,num)

time1 = time.time()
NSwintrumps = playCard(deck,"NT","N",0,deal)
time2 = time.time()
print(NSwintrumps,time2-time1)
print(i,j)   
