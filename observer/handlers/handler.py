from abc import ABC,abstractmethod


class Handler(ABC):
    @abstractmethod
    def can_handle(self, message:dict) -> bool:
        """return can it handle this message or not"""
        pass

    @abstractmethod
    def handle(self, message:dict) -> bool:
        """returns continue - go next or not"""
        pass