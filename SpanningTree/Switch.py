
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm -
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks
#           Based on prior work by Sean Donovan, 2015, updated for new VM by Jared Scott and James Lohse

from Message import *
from StpSwitch import *


class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)

        # TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.
        self.root = self.switchID
        self.distance = 0
        self.active_links = dict.fromkeys(neighbors, True)
        self.switch_through = self.switchID

    def send_initial_messages(self):
        # TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
        #      Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)
        for neighbour in self.links:
            msg = Message(self.root, self.distance, self.switchID, neighbour, False)  # Doesn't go through the initial sending Nodes
            self.send_message(msg)
        return

    def process_message(self, message):
        # TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.
        # If a switch gets a message with a paththrough of true, the sending switch goes through the receiving switch in order to access the root        
        if message.root < self.root:
            self.root = message.root
            self.distance = message.distance + 1
            self.active_links[message.origin] = True
            self.switch_through = message.origin
            self.helper()

        elif message.root == self.root:
            if message.distance + 1 > self.distance:
                if message.pathThrough is True:
                    self.active_links[message.origin] = True
                else:
                    self.active_links[message.origin] = False
                return
            
            if message.distance + 1 < self.distance:
                self.distance = message.distance + 1
                self.active_links[message.origin] = True
                self.switch_through = message.origin
                self.helper()
                
            elif message.distance + 1 == self.distance:  # (Tie Breaker)
                if message.origin < self.switch_through:
                    self.active_links[self.switch_through] = False
                    self.switch_through = message.origin
                    self.helper()
                    
                elif message.origin > self.switch_through:
                    self.active_links[message.origin] = False
                    self.helper()
                    
    def helper(self):
        for neighbour in self.links:
            this_path_through = False
            if neighbour == self.switch_through:
                this_path_through = True
            msg = Message(self.root, self.distance,
                            self.switchID, neighbour, this_path_through)
            self.send_message(msg)

    def generate_logstring(self):
        # TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked
        #      only after the simulaton is complete.  Output the links included in the
        #      spanning tree by increasing destination switch ID on a single line.
        #      Print links as '(source switch id) - (destination switch id)', separating links
        #      with a comma - ','.
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        to_return = ""
        sorted_links = sorted(self.active_links.items())
        for key, value  in sorted_links:
            if value is True:
                to_return+="%d - %d, " %(self.switchID, key)
        to_return = to_return[:-2]
        return to_return

