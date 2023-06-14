from Builder.Builder import Builder
import matplotlib.pyplot as plt
import os


class PieGraph(Builder):

    def __init__(self, path, is_title):
        super().__init__(path, is_title)
        self.x = []
        self.y = []

    def open_file(self) -> None:
        with open(self.path, mode="r") as file:
            if self.is_title:
                self.title = file.readline().split(",")
                self.title[1].replace("\n", "")
            while True:
                line = file.readline()
                if not line:
                    break
                self.x.append(line.split(",")[0])
                self.y.append(line.split(",")[1].replace("\n", ""))

        self.x = [int(element) for element in self.x]
        self.y = [int(element) for element in self.y]

    def prepare_chart(self) -> None:
        plt.title(f"Wykres z pliku {os.path.basename(self.path)}")

    def create_chart(self) -> None:
        plt.pie(self.y, labels=self.x)
        plt.show()

    @property
    def product(self) -> None:
        pass
