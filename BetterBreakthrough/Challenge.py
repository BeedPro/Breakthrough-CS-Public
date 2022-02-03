
class Challenge():
    def __init__(self):
        self._Met = False
        self._Condition = []

    def GetMet(self):
        return self._Met

    def GetCondition(self):
        return self._Condition

    def SetMet(self, NewValue):
        self._Met = NewValue

    def SetCondition(self, NewCondition):
        self._Condition = NewCondition
