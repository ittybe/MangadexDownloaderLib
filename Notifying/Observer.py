from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, **kwargs):
        '''
        get info from Event notify
        '''
        pass