from abc import ABC, abstractmethod


class BaseWebFile(ABC):
    """
    Abstract class that dectates to implement required methods
    """

    @abstractmethod
    def get_path(self):
        return NotImplemented("Please Implement this method")
