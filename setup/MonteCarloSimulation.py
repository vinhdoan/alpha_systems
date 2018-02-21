import math
import numpy as np
from time import time
import random
import matplotlib.pyplot as plt
broke = 0
def rollDice():
    roll = random.randint(1,100)
    if roll>52:
        #print(roll, 'roll was 100. You lose')
        return True
    elif roll <= 48:
        return False

def simple_bettor(funds,inital_wager,wager_count):
    value = funds
    wager = inital_wager
    currentWager = 1
    wX = []
    vY = []
    while currentWager<=wager_count:
        if rollDice():
            value += 2.7*wager
            wX.append(currentWager)
            vY.append(value)
        else:
            value -= wager
            wX.append(currentWager)
            vY.append(value)
        currentWager += 1
        plt.plot(wX,vY)

def simple_bettor(funds,inital_wager,wager_count):
    value = funds
    wager = inital_wager
    currentWager = 1
    wX = []
    vY = []
    while currentWager<=wager_count:
        if rollDice():
            value += 2.7*wager
            wX.append(currentWager)
            vY.append(value)
        else:
            value -= wager
            wX.append(currentWager)
            vY.append(value)
        currentWager += 1
        plt.plot(wX,vY)

# trading algorithm: each time bet percent % of current equity (ex. 2%)
def exponential_bettor(funds, percent, wager_count):
    value = funds
    currentWager = 1
    global broke_account
    wX = []
    vY = []
    while currentWager <= wager_count:
        if rollDice():
            wager = percent * value
            value += 2.7 * wager
            wX.append(currentWager)
            vY.append(value)
        else:
            wager = percent * value
            value -= wager
            wX.append(currentWager)
            vY.append(value)
        currentWager += 1
        plt.plot(wX, vY)
    if value<3*funds:
        broke_account+=1

def doubler_bettor(funds, inital_wager, wager_count):
    value = funds
    wager = inital_wager
    global broke_count
    wX = []
    vY = []
    currentWager = 1
    previousWager = 'win'
    previousWagerAmount = inital_wager
    while currentWager < wager_count:
        if previousWager == 'win':
            #print('we won last wager, great')
            if rollDice():
                value += 2.7*wager
                #print(value)
                wX.append(currentWager)
                vY.append(value)
            else:
                value -= wager
                #print(value)
                previousWager = 'loss'
                previousWagerAmount = wager
                wX.append(currentWager)
                vY.append(value)
                if value<0:
                    #print('we went broke after',currentWager,'bets')
                    broke_count += 1
                    break
        elif previousWager=='loss':
            #print('we lost the last one, so double now')
            if rollDice():
                wager = previousWagerAmount * 2
                #print('we won', wager)
                value += 2.7*wager
                #print(value)
                wager = inital_wager
                previousWager = 'win'
                wX.append(currentWager)
                vY.append(value)
            else:
                wager = previousWagerAmount * 2
                #print('we loss', wager)
                value -= wager
                if value<0:
                    #print('we go broke ater',currentWager,'bets')
                    broke_count += 1
                    break
                #print(value)
                previousWagerAmount = wager
                wX.append(currentWager)
                vY.append(value)
        currentWager += 1
    #print(value)
    plt.plot(wX,vY)

# xx = 0
# broke_count = 0
# while xx<100:
#     doubler_bettor(10000,100,100)
#     xx+=1
#
# print('death rate:', (broke_count/float(xx))*100)
# print('survival rate', 100 - (broke_count/float(xx))*100)
#
# plt.axhline(0,color='r')
# plt.ylabel("Account Value")
# plt.xlabel("wager count")
# plt.show()

broke_account = 0
x = 0
while x < 30:
    #simple_bettor(10000,100,100)
    print(x)
    exponential_bettor(10000,0.025,100)
    x+=1
print('broke_account:',broke_account,'times')
print("death rate:", broke_account/float(200)*100)
print("survival rate:", 100 - broke_account/float(200)*100)
plt.ylabel("Account Value")
plt.xlabel("wager count")
plt.show()

