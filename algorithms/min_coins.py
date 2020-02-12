# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 10:55:56 2018

@author: kasprark
"""

def change_coin(amount, coins):
    coins.sort(reverse=True)

    def find_coin(amount, coins):
        
        for k in range(len(coins)):
            if coins[k] <= amount:
                coin = coins[k]
                amount -= coin
                if amount == 0:
                    coins = coins[(k+1):]
                else:
                    coins = coins[k:]
                return amount, coins, coin
                break
            else:
                if k == len(coins) - 1:
                    coin = coins[k]
                    amount -= coin    # will be negative
                    return amount, coins, coin
                else:
                    pass

    result = []
    
    while amount > 0:
        amount, coins, coin = find_coin(amount, coins)
        if amount < 0:
            result.append(amount)
        else:
            result.append(coin)
        
    return result


#%%                

change_coin(5, [5])    
change_coin(5, [1])    
change_coin(5, [2, 1])    
change_coin(8, [5, 2, 1])    
change_coin(8, [5, 2])    
change_coin(8, [3, 2])    

       

    
#%%
lst = [3, 5, 2]

lst[:]
lst[0:]
lst[1:]
lst[2:]
lst[3:]

lst.sort()    
lst

lst.pop(0)
lst

lst.pop()

a = 1 if lst[0] == 2 else 2
a
