
class Card:
    _NextCardNumber = 0

    def __init__(self):
        self._CardNumber = Card._NextCardNumber
        Card._NextCardNumber += 1
        self._Score = 0

    def GetScore(self):
        return self._Score

    def Process(self, Deck, Discard, Hand, Sequence, CurrentLock, Choice, CardChoice):
        pass

    def GetCardNumber(self):
        return self._CardNumber

    def GetDescription(self):
        if self._CardNumber < 10:
            return " " + str(self._CardNumber)
        else:
            return str(self._CardNumber)
