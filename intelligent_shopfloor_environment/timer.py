"""
the class of time controller
"""
from intelligent_shopfloor_environment.machine import Machine, WareHouse
from intelligent_shopfloor_environment.shopfloor import ShopFloor


class TimeController:
    def __init__(self, shopfloor_environment: ShopFloor):
        """"Initializes a TimeController"""
        self._time = -1
        self._observers: set[Machine or WareHouse] = set()
        self.shopfloor = shopfloor_environment
        self.generate_warehouse = shopfloor_environment.generate_warehouse

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, new_time):
        self._time = new_time
        self.shopfloor.generate_warehouse.onTickTick(new_time)
        self.notifyFirst(new_time)
        self.notifySecond(new_time)

    def attach(self, observer):
        """add observer to observers"""
        self._observers.add(observer)

    def detach(self, observer):
        """remove observer from observers"""
        self._observers.remove(observer)

    def notifyFirst(self, new_time: int):
        """notify all observers"""
        for observer in self._observers:
            observer.onTickTick(new_time)

    def notifySecond(self, new_time: int):
        """notify all observers"""
        for observer in self._observers:
            observer.onTickTickSecond(new_time)

    def tickTick(self):
        """run time to the next tick"""
        self.time = self.getNextTimeStep()

    def start(self):
        """start the shopfloor"""
        self.time = 0

    def getNextTimeStep(self) -> int:
        return self.shopfloor.getNextTimeStep()

    def reset(self):
        self._time = 0
