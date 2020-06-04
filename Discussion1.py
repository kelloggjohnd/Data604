# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 22:01:52 2020

@author: x
"""
import random
from modsim import *

def roll_dice(n, s):
    
# define the counting varibles
    count1 = 0
    count2 = 0
    count3 = 0
# sides will define how many sides the dice has
    sides = s
    
    for i in range(n):
        # Random rolls defined by the sides varible in the function (s)
        player1 = random.randint(1,sides)
        player2 = random.randint(1,sides)
        # if player 1 wins
        player1_win = player1 > player2
        # if player 2 wins
        player2_win = player1 < player2
        # if it's a draw
        draw = player1 == player2
        
        #defining the if statements for each count seperately
        if player1_win == True:
            count1 += 1
        if player2_win == True:
            count2 += 1
        if draw == True:
            count3 += 1    
    #return count
    print('The amount of games Player 1 won is: ' + str(count1))
    print('The amount of games Player 2 won is: ' + str(count2))
    print('The amount of games as a draw is: ' + str(count3))
           
roll_dice(10000,6)