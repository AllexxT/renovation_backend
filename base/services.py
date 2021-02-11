from abc import ABCMeta, abstractmethod


class Service:
    metaclass = ABCMeta

    @abstractmethod
    def execute(self):
        raise NotImplementedError("Not implemented method execute")