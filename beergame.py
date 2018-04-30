# Copyright (c) Mikaël Swawola. All rights reserved.

# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

import os, sys
import random
from argparse import ArgumentParser
import json

import pandas as pd

from stage import Stage

    
def createAgents(args, data):
    """
    """
    
    il=data['inventory']
    ch=data['holding_cost']
    cp=data['shortage_cost']
    bs=data['base_stock']
    
    # Instantiate agents/stages
    retailer = Stage("Retailer", inventory=il, holding_cost=ch, shortage_cost=cp, base_stock=bs)
    wholesaler = Stage("Wholesaler", inventory=il, holding_cost=ch, shortage_cost=cp, base_stock=bs)
    distributor = Stage("Distributor", inventory=il, holding_cost=ch, shortage_cost=cp, base_stock=bs)
    factory = Stage("Factory", inventory=il, holding_cost=ch, shortage_cost=cp, base_stock=bs)
    
    if args['agent'] == 'retailer':
        retailer.set_strategy('human')
    elif args['agent'] == 'wholesaler':
        wholesaler.set_strategy('human')
    elif args['agent'] == 'distributor':
        distributor.set_strategy('human')
    elif args['agent'] == 'distributor':
        factory.set_strategy('human')
    else:
        print('Error in argument')
        sys.exit(1)
    
    return retailer, wholesaler, distributor, factory


def saveHistory(costs, ILs):
    """
    """
    df_retailer = pd.DataFrame(data={'costs': costs['retailer'],'inventory':ILs['retailer']})
    df_wholesaler = pd.DataFrame(data={'costs': costs['wholesaler'],'inventory':ILs['wholesaler']})
    df_distributor = pd.DataFrame(data={'costs': costs['distributor'],'inventory':ILs['distributor']})
    df_factory = pd.DataFrame(data={'costs': costs['factory'],'inventory':ILs['factory']})

    df_retailer.to_csv('retailer.csv')
    df_wholesaler.to_csv('wholesaler.csv')           
    df_distributor.to_csv('distributor.csv')
    df_factory.to_csv('factory.csv')
    
    print('Saved results !')


def playGame(args):
    """
    """
    
    with open(args['param']) as data_file:    
        data = json.load(data_file)
    
    # Instantiate agents / stages
    retailer, wholesaler, distributor, factory = createAgents(args, data)
    
    # Initializations
    customer_demand = [5,5,5,5,5,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9]
    customer_demand = customer_demand[:random.randint(30,50)] # End the game after a random number of weeks
    
    # Order out-and-inboxes
    r_out = 0 # retailer outbox
    w_out = 0 # wholesaler outbox
    d_out = 0 # distributor outbox
    f_out = 0 # factory outbox
    w_in = 0 # wholesaler inbox 
    d_in = 0 # distributor inbox 
    f_in = 0 # factory inbox 
    
    # Transportation lead times
    r_w_delay = [0,0] # delay buffer between retailer and wholesaler
    w_d_delay = [0,0] # delay buffer between wholesaler and distributor
    d_f_delay = [0,0] # delay buffer between distributor and factory
    f_delay = [0,0] # delay buffer for factory production

    # Dictionnaries for storing costs and inventory levels (ILs) history
    costs = {'retailer' : [0],
             'wholesaler' : [0],
             'distributor' : [0],
             'factory' : [0],
            }

    ILs = {'retailer' : [0],
           'wholesaler' : [0],
           'distributor' : [0],
           'factory' : [0],
           }


    i = 0

    try:
        for cd in customer_demand:
            i += 1
            _ = os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"\n+----- WEEK #{i} -----+") 
            deliv, r_out, il, cost = retailer.play(incoming = r_w_delay[0], order = cd)
            r_w_delay[0] = r_w_delay[1]
            costs['retailer'].append(cost)
            ILs['retailer'].append(il)

            r_w_delay[1], w_out, il, cost = wholesaler.play(incoming = w_d_delay[0], order = w_in)
            w_d_delay[0] = w_d_delay[1]
            costs['wholesaler'].append(cost)
            ILs['wholesaler'].append(il)

            w_d_delay[1], d_out, il, cost = distributor.play(incoming = d_f_delay[0], order = d_in)
            d_f_delay[0] = d_f_delay[1]
            costs['distributor'].append(cost)
            ILs['distributor'].append(il)

            d_f_delay[1], f_out, il, cost = factory.play(incoming = f_delay[0], order = f_in)
            f_delay[0] = f_delay[1]
            f_delay[1] = f_out
            costs['factory'].append(cost)
            ILs['factory'].append(il)

            w_in = r_out
            d_in = w_out
            f_in = d_out

    except KeyboardInterrupt:
        pass

    saveHistory(costs, ILs)
    
    print('Game Over !')

    
def main():
    """
    """
    parser = ArgumentParser(description='Beer Game')
    parser.add_argument('-a','--agent', help='retailer / wholesaler / distributor / factory', required=True)
    parser.add_argument('-p','--param', help='parameters file', required=False)
    args = vars(parser.parse_args())
    playGame(args)


if __name__ == "__main__":
    """
    Entry point, execute only if run as a script
    """
    main()
   
            
        
        
    