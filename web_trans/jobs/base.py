from abc import ABC, abstractmethod


class BaseJob(ABC):
    """
    Abstract class that dectates to implement required methods
    """

    @abstractmethod
    def execute_job(self):
        return NotImplemented("Please Implement this method")
