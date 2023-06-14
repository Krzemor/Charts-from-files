from abc import abstractmethod


class Builder:

    def __init__(self, path, is_title):
        self.path = path
        self.content = ''
        self.title = ''
        self.is_title = is_title

    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def open_file(self) -> None:
        pass

    @abstractmethod
    def prepare_chart(self) -> None:
        pass

    @abstractmethod
    def create_chart(self) -> None:
        pass
