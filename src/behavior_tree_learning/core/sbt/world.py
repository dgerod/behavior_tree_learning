from interface import Interface


class World(Interface):

    def startup(self, verbose):
        pass

    def is_alive(self):
        pass

    def shutdown(self):
        pass
