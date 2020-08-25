from abc import ABC, abstractmethod

from MangadexDownloaderLib.Observer import Observer

class Event(ABC):
    @abstractmethod
    def notify(self, **kwargs):
        '''
        notify all subscribers and send info about event
        '''
        pass
    
    @abstractmethod
    def detach(self, observer :Observer) -> None:
        '''
        unsubscribe observer from event
        '''
        pass

    @abstractmethod
    def attach(self, observer :Observer) -> None:
        '''
        subscribe observer to event
        '''
        pass