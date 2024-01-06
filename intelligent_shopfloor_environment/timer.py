"""
the class of time controller
"""


class TimeController:
    def __init__(self):
        """"Initializes a TimeController"""
        self.time = 0
        self._observers = set()

    def attach(self, observer):
        """add observer to observers"""
        self._observers.add(observer)

    def detach(self, observer):
        """remove observer from observers"""
        self._observers.remove(observer)

    def notify(self, message):
        """notify all observers"""
        for observer in self._observers:
            observer.notify(message)
