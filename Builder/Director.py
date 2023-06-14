class Director:

    def __init__(self):
        self._builder = None

    @property
    def builder(self):
        return self._builder

    @builder.setter
    def builder(self, builder):
        self._builder = builder

    def build_graph(self):
        self.builder.open_file()
        self.builder.prepare_chart()
        self.builder.create_chart()
