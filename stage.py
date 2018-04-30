# Copyright (c) Mikaël Swawola. All rights reserved.

# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

class Stage:

    def __init__(self, name, inventory = 15, holding_cost=0.5 , shortage_cost=1.0, base_stock=15, strategy='human'):
        """
        
        Args:
        name (str): name of the stage
        
        holding_cost (float): cost for holding one item per week
        
        shortage_cost (float): cost for one backordered item per week
        """
        
        self.name = name
        
        self.ch = holding_cost
        self.cp = shortage_cost
        
        self.inventory = inventory
        self.available = 0
        self.backorder = 0
        self.to_ship = 0
        self.delivery = 0
        self.new_order = 0
        
        self.strategy = strategy
        self.base_stock = base_stock
        
        
        self.OO = 0 # On-order items
    
    def new_delivery(self, incoming):
        self.available = self.inventory + incoming
        self.OO -= incoming
    
    def new_incoming_order(self, order):
        self.to_ship = self.backorder + order
        
    def prepare_delivery(self):
        if self.to_ship >= self.available:
            self.delivery = self.available
        else:
            self.delivery = self.to_ship
    
    def calculate_backorder(self):
        if self.to_ship > self.available:
            self.backorder = self.to_ship - self.available
        else:
            self.backorder = 0    
    
    def calculate_inventory(self):
        if self.to_ship > self.available:
            self.inventory = 0
        else:
            self.inventory = self.available - self.to_ship
    
    def place_new_order(self, incoming, order):
        
        if self.strategy == 'human':
            print(" ")
            print(self.name)
            print("---------------")
            print("Incoming:" + str(incoming))
            print('Available: ' + str(self.available))
            print('New Order: ' + str(order))
            print('Demand/to_ship: ' + str(self.to_ship))
            print('Delivery: ' + str(self.delivery))
            print('Backorder: ' + str(self.backorder))
            print('Inventory: ' + str(self.inventory))
            print('On-order items: ' + str(self.OO))
            #print('Week cost: ' + str(self.costs_history[-1]))
            #print('Cumulative costs: ' + str(sum(self.costs_history)))

            ok = False
            while not ok: 
                try:
                    self.new_order = input("Your order? ")
                    self.OO += int(self.new_order)
                    ok = True
                except ValueError:
                    print('INPUT ERROR')
                    ok = False
        else:
            self.new_order = self.base_stock - self.inventory + self.backorder - self.OO
            if self.new_order > 0:
                self.OO += self.new_order
            
        
        
            
    def get_OO(self):
        return self.OO
    
    def compute_costs(self):
        if self.inventory > 0:
            cost = self.ch * self.inventory
        elif self.backorder > 0:
            cost = self.cp * self.backorder
        else:
            cost = 0
        
        return cost
        
        
    
    def play(self, incoming, order):

        self.new_delivery(incoming)
        self.new_incoming_order(order)
        self.prepare_delivery()
        self.calculate_backorder()
        self.calculate_inventory()
        self.place_new_order(incoming, order)
        
        assert(self.backorder == 0 or self.inventory == 0)
       
        if self.inventory > 0:
            il = self.inventory
        else:
            il = -self.backorder
    
        return (self.delivery,
                int(self.new_order),
                il,
                self.compute_costs()
               )      