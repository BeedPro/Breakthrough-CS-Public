from PythonFile.Breakthrough.BetterBreakthrough.Card import Card


class ToolCard(Card):
    def __init__(self, *args):
        self._ToolType = args[0]
        self._Kit = args[1]
        if len(args) == 2:
            super(ToolCard, self).__init__()
        elif len(args) == 3:
            self._CardNumber = args[2]
        self.__SetScore()

    def __SetScore(self):
        if self._ToolType == "K":
            self._Score = 3
        elif self._ToolType == "F":
            self._Score = 2
        elif self._ToolType == "P":
            self._Score = 1

    def GetDescription(self):
        return self._ToolType + " " + self._Kit

