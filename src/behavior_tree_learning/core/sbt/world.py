from interface import Interface


class World(Interface):

    def startup(self):
        pass

    def is_alive(self):
        pass

    def shutdown(self):
        pass
