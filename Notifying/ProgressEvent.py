from Notifying.Observer import Observer
from Notifying.Event import Event

class ProgressEvent(Event):
    
    def __init__(self):
        self._observers = []

    def notify(self, **kwargs):
        '''
        notify all subscribers and send info about event
        '''
        # notify all observers about progress event with args
        for observer in self._observers:
            observer.update(**kwargs)

    def detach(self, observer :Observer):
        '''
        unsubscribe observer from event
        '''
        # check type
        if (not isinstance(observer, Observer)):
            raise TypeError(f"observer arg is {type(observer)}, observer have to be {Observer}")
        self._observers.remove(observer)

    def attach(self, observer :Observer):
        '''
        subscribe observer to event
        '''
        # check type
        if (not isinstance(observer, Observer)):
            raise TypeError(f"observer arg is {type(observer)}, observer have to be {Observer}")
        self._observers.append(observer)