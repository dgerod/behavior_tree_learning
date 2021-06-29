import re
import py_trees as pt
from find_action.parse_operation import parse_function, print_parsed_function


class Anchored(pt.behaviour.Behaviour):

    @staticmethod
    def make(text, world, verbose=False):

        print_parsed_function(text)   
        operation = parse_function(text)                  
        return Anchored(text, world, operation, verbose)

    def __init__(self, name, world, operation, verbose):
        
        super().__init__(name)        
        self._world = world
        self._operation = operation
        self._verbose = verbose

        print_parsed_function(name)   
        self._operation = parse_function(name)    

    def initialise(self):
        print("Anchored::initialise() [%s]" % self.name)
        text = self._operation[0] + " " + str(self._operation[1]) + " => " + str(self._operation[2])           
        print("operation: ", text)
        
    def update(self):
        print("Anchored::update() [%s]" % self.name)
        return pt.common.Status.FAILURE


class MoveArmTo(pt.behaviour.Behaviour):

    @staticmethod
    def make(text, world, verbose=False):
        
        print_parsed_function(text)   
        operation = parse_function(text)       
        return MoveArmTo(text, world, operation, verbose)

    def __init__(self, name, world, operation, verbose):
        
        super().__init__(name)        
        self._world = world
        self._operation = operation
        self._verbose = verbose

        print_parsed_function(name)   
        self._operation = parse_function(name)      

        #self._place = place        

    def initialise(self):
        print("MoveArmTo::initialise() [%s]" % self.name)
        
    def update(self):
        print("MoveArmTo::update() [%s]" % self.name)
        return pt.common.Status.SUCCESS

    def terminate(self, new_status):
        print("MoveArmTo::terminate() [%s]" % self.name)

class RetrieveObjects(pt.behaviour.Behaviour):

    @staticmethod
    def make(text, world, verbose=False):
        
        print_parsed_function(text)   
        operation = parse_function(text)       
        return RetrieveObjects(text, world, operation, verbose)

    def __init__(self, name, world, operation, verbose):
        
        super().__init__(name)        
        self._world = world
        self._operation = operation
        self._verbose = verbose

        print_parsed_function(name)   
        self._operation = parse_function(name)    

    def initialise(self):
        print("RetrieveObjects::initialise() [%s]" % self.name)
        
    def update(self):
        print("RetrieveObjects::update() [%s]" % self.name)
        return pt.common.Status.SUCCESS
