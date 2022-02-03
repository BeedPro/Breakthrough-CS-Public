from PythonFile.Breakthrough.BetterBreakthrough.Card import Card

class DifficultyCard(Card):
    def __init__(self, *args):
        self._CardType = "Dif"
        if len(args) == 0:
            super(DifficultyCard, self).__init__()
        elif len(args) == 1:
            self._CardNumber = args[0]

    def GetDescription(self):
        return self._CardType

    def Process(self, Deck, Discard, Hand, Sequence, CurrentLock, Choice, CardChoice):
        ChoiceAsInteger = None
        try:
            ChoiceAsInteger = int(Choice)
        except:
            pass
        if ChoiceAsInteger is not None:
            if ChoiceAsInteger >= 1 and ChoiceAsInteger <= 5:
                if ChoiceAsInteger >= CardChoice:
                    ChoiceAsInteger -= 1
                if ChoiceAsInteger > 0:
                    ChoiceAsInteger -= 1
                if Hand.GetCardDescriptionAt(ChoiceAsInteger)[0] == "K":
                    CardToMove = Hand.RemoveCard(Hand.GetCardNumberAt(ChoiceAsInteger))
                    Discard.AddCard(CardToMove)
                    return
        Count = 0
        while Count < 5 and Deck.GetNumberOfCards() > 0:
            CardToMove = Deck.RemoveCard(Deck.GetCardNumberAt(0))
            Discard.AddCard(CardToMove)
            Count += 1


