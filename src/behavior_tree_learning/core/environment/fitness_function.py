from interface import Interface


class FitnessFunction(Interface):
    
    def compute(self, world, behavior_tree):
        """ Retrieve values and compute cost """
        pass
