# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:59:17 2020

@author: skans
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 11:39:33 2020

@author: skans
"""
import json
from operator import itemgetter

class Node:
    def __init__(self,node_name,node_type,parent_name,cost,benefits, probability):
        self.node_type = node_type
        self.node_name = node_name
        self.parent_name = parent_name
        self.data = {'Cost': cost, 'Benefits': benefits, 'Probability': probability}
        self.branches = []

    def printJSON(self):
        print( json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4))
        
    def toJSON(self):
        json_string =  json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)
        return json.loads(json_string)
        
    def solve(self):
        if self.node_type == "Payoff":
            payoff = self.data['Benefits']-self.data['Cost']
            self.data['Payoff'] = payoff
            return payoff
        elif self.node_type == "Chance":
            sum = 0
            for child in self.branches:
                prob = child.data['Probability']
                value = child.solve()
                final_value = prob*(value - self.data['Cost'])
                sum = sum + final_value 
            self.data['EV'] = sum
            return sum
        else:
            maximization_list = []
            for child in self.branches:
                value = child.solve()
                node_recognition ={'name':child.node_name,'value':value}
                maximization_list.append(node_recognition)
            print(maximization_list)
            sorted_list = sorted(maximization_list, key=itemgetter('value'), reverse = True)
            return sorted_list[0]
            
        
    def insert(self,parent_name, child_node):
        if self.node_name == None:
            try:
                raise KeyboardInterrupt
            finally:
                print("There is no node")
        elif self.node_name != parent_name:
            for child in self.branches:
                if child.node_name == parent_name:
                    child.insert(child.node_name, child_node)
        else:
            self.branches.append(child_node)
            
    @staticmethod
    def read_json_formation_node(input_json_data):
        nodes_dict = {}
        for nodes in input_json_data: 
            if nodes['parent_node'] == "": ## Basically trying to access the root node andI think we can have a better condition
                node_type = nodes['node_type']
                node_name = nodes['node_name']
                cost = nodes['data']['Cost']
                benefits = nodes['data']['Benefits']
                probability = nodes['data']['Probability']
                parent_node = nodes['parent_node']
                new_node = Node(node_name,node_type,parent_node, cost,benefits,probability)
                nodes_dict[node_name] = new_node
            else:
                node_type = nodes['node_type']
                node_name = nodes['node_name']
                cost = nodes['data']['Cost']
                benefits = nodes['data']['Benefits']
                probability = nodes['data']['Probability']
                parent_node = nodes['parent_node']
                new_node = Node(node_name,node_type,parent_node,cost,benefits,probability)
                if node_type == "Chance":
                    node_data = new_node.data
                    node_data['probability_checker'] = []
                    nodes_dict[node_name] = new_node
                else:
                    nodes_dict[node_name] = new_node 
        for decision_tree_node in nodes_dict.keys():
            decision_tree_node_class = nodes_dict[decision_tree_node]
            if decision_tree_node_class.parent_name == "":
                root_node = decision_tree_node_class# It is a root node and that needs to be returned
                continue
            else:
                nodes_parent_name = decision_tree_node_class.parent_name
                parent_node_class = nodes_dict.get(nodes_parent_name) #The list includes parent_node, its parent_name
                if parent_node_class.node_type == "Chance": #Here we wil access the probability checker list
                    data_info = decision_tree_node.data # Accessing the data indicator of the node
                    probability_childnode = data_info['Probability'] # Data info is a dictionary and we will take the probability value
                    probability_checker_list = parent_node_class.data['probability_checker'] # Accessig the probability checker list of the parent node
                    if sum(probability_checker_list) > 1:
                        raise NameError("""The probability sum is greater than 1,
                                        thus cant add a new node anmore """)
                    else:
                        probability_checker_list.append(probability_childnode)
                        parent_node_class.branches.append(decision_tree_node_class)
                elif parent_node_class.node_type == "Payoff":
                    raise NameError("We cant add a child to the parent node")
                else:
                    parent_node_class.branches.append(childnode_with_node_parentnode[0])
        return root_node
                                 
# Question 1 

# final_decision = Node("Computer System", "Final Decision", 0 , 0 , 0)    
# advanced_computer_system = Node("Advanced Computer System", "Chance",20,0, 0)     
# current_computer_system = Node("Current Computer System", "Payoff", 20, 30, 0 )
# high_prob_adc = Node("High Probability", "Payoff", 0, 60 ,0.70)
# low_prob_adc = Node("Low Probability", "Payoff", 0,30,0.30)
# advanced_computer_system.insert("Advanced Computer System", high_prob_adc) 
# advanced_computer_system.insert("Advanced Computer System", low_prob_adc)
# final_decision.insert("Computer System",advanced_computer_system)
# final_decision.insert("Computer System", current_computer_system)
# print("The decision should be:",final_decision.solve())

# final_decision.printJSON()


input_json_data = [
   {
      "node_type":"Root|Choice",
      "node_name":"Computer System",
      "data":{
         "Cost":0,
         "Benefits":0,
         "Probability":0
      },
      "parent_node":""},
{
         "node_type":"Chance",
         "node_name":"Advanced Computer System",
         "data":{
            "Cost":20,
            "Benefits":0,
            "Probability":0
            },
         "parent_node":"Computer System"},
{
            "node_type":"Payoff",
            "node_name":"High Probability",
            "data":{
               "Cost":0,
               "Benefits":60,
               "Probability":0.7
            },
            "parent_node":"Advanced Computer System"},
{
               "node_type":"Payoff",
               "node_name":"Low Probability",
               "data":{
                  "Cost":0,
                  "Benefits":30,
                  "Probability":0.3
               },
               "parent_node":"Advanced Computer System"},
        {
            "node_type": "Payoff",
            "node_name": "Current Computer System",
            "data": {
                "Cost": 20,
                "Benefits": 30,
                "Probability": 0,
                "Payoff": 10
            },
            "parent_node":"Computer System"}
            ]

decision_tree = Node.read_json_formation_node(input_json_data)
decision_tree.printJSON()
print(decision_tree.solve())