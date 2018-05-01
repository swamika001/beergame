# Copyright (c) Mikaël Swawola. All rights reserved.

# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

import re

class Stage:

    def __init__(self, name, m=3, inventory=15, holding_cost=0.5, shortage_cost=1.0, base_stock=15, strategy='base-stock-policy'):
        """
        Args:
        name (str): name of the stage
        
        holding_cost (float): cost for holding one item per week
        
        shortage_cost (float): cost for one backordered item per week
        """
        
        self._name = name
        
        self._inventory = inventory # Inventory on-hand
        self._backorder = 0
        self._OO = 0 # On-order items
        self._demand = 0
        self._incoming = 0
        self._history = [] # Historcial observations
        
        self.m = m # Only the last m periods are captured in state
        self.ch = holding_cost
        self.cp = shortage_cost
        
        self.available = 0
        
        self.to_ship = 0
        self.delivery = 0
        self.new_order = 0

        self.strategy = strategy
        self.base_stock = base_stock
        
        
    
    def new_delivery(self, incoming):
        """
        """
        
        assert(incoming >= 0)
        self._incoming = incoming
        self.available = self._inventory + incoming
        self._OO -= incoming
        
    
    def new_incoming_order(self, order):
        """
        """
        assert(order >= 0)
        self._demand = order
        self.to_ship = self._backorder + order
        
    def prepare_delivery(self):
        """
        """
        if self.to_ship >= self.available:
            self.delivery = self.available
        else:
            self.delivery = self.to_ship
    
    def calculate_backorder(self):
        """
        """
        if self.to_ship > self.available:
            self._backorder = self.to_ship - self.available
        else:
            self._backorder = 0    
    
    def calculate_inventory(self):
        """
        """
        if self.to_ship > self.available:
            self._inventory = 0
        else:
            self._inventory = self.available - self.to_ship
    
    def place_new_order(self, order):
        """
        """
        if self.strategy == 'human':
            print(" ")
            print(self._name)
            print("---------------")
            print("Incoming:" + str(self._incoming))
            print('Available: ' + str(self.available))
            print('New Order: ' + str(order))
            print('Demand/to_ship: ' + str(self.to_ship))
            print('Delivery: ' + str(self.delivery))
            print('Backorder: ' + str(self._backorder))
            print('Inventory: ' + str(self._inventory))
            print('On-order items: ' + str(self._OO))
            #print('Week cost: ' + str(self.costs_history[-1]))
            #print('Cumulative costs: ' + str(sum(self.costs_history)))

            ok = False
            while not ok: 
                try:
                    self.new_order = input("Your order? ")
                    self._OO += int(self.new_order)
                    ok = True
                except ValueError:
                    print('INPUT ERROR')
                    ok = False
        else:
            self.new_order = self.base_stock - self._inventory + self._backorder - self._OO
            if self.new_order > 0:
                self._OO += self.new_order
            
        
        
    @property        
    def get_state_variable_OO(self):
        """
        On-order items (State variable)
        
        Items that have been ordered from agent i+1 but not received yet
        """
        return self._OO
    
    @property
    def get_state_variable_d(self):
        """
        demand / order (State variable)
        
        Demand / order recevie from agent i-1
        """
        return self._demand

    @property
    def get_state_variable_RS(self):
        """
        Received Shipment (State variable)
        
        Size of the shipment recevied from agent i+1
        """
        return self._incoming

    @property
    def get_state_variable_IL(self):
        """
        Inventory Level (State variable)
        
        Inventory on hand or backorder
        """
        return self._inventory - self._backorder
    
    @property
    def get_environment(self):
        """
        Environment
        
        All state variables: IL, OO, d and RS
        """
        return {
            'IL': self.get_state_variable_IL,
            'OO': self.get_state_variable_OO,
            'd': self.get_state_variable_d,
            'RS': self.get_state_variable_RS
        }
    
    @property
    def get_state_variable(self):
        """
        State Variable for DQN
        
        All the state variables in the last m periods
        """
        if len(self._history) >= self.m:
            return self._history[-self.m:]
        
        return None
    
    def set_strategy(self, strategy):
        """
        Strategy setter
        """
        if re.match(r"human|base-stock-policy|sterman|DQN", strategy) is not None:
            self.strategy = strategy
        else:
            raise Exception('Unknown strategy')

            
    def compute_costs(self):
        """
        Compute holding and stockout costs
        """
        assert(self._backorder == 0 or self._inventory == 0)

        return self.ch * self._inventory + self.cp * self._backorder
                
    
    def play(self, incoming, order):
        """
        """
        self.new_delivery(incoming)
        self.new_incoming_order(order)
        self.prepare_delivery()
        self.calculate_backorder()
        self.calculate_inventory()
        self.place_new_order(order)
        
        assert(self._backorder == 0 or self._inventory == 0)
    
        # Add new observation to history
        self._history.append(self.get_environment)
    
        return (self.delivery,
                int(self.new_order),
                self.compute_costs()
               )      