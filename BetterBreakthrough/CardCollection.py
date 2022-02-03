import random


class CardCollection:
    def __init__(self, N):
        self._Name = N
        self._Cards = []
        self._Stats = []
        self._NumKeys = 0
        self._NumFiles = 0
        self._NumPicks = 0

    def GetName(self):
        return self._Name

    def GetCards(self):
        return self._Cards

    def GetCardNumberAt(self, X):
        return self._Cards[X].GetCardNumber()

    def GetCardDescriptionAt(self, X):
        return self._Cards[X].GetDescription()

    def AddCard(self, C):
        CardString = C.GetDescription()
        CardType = CardString[0]

        if CardType == "K":
            self._NumKeys += 1
        elif CardType == "F":
            self._NumFiles += 1
        elif CardType == "P":
            self._NumPicks += 1

        self._Cards.append(C)

    def GetNumberOfCards(self):
        return len(self._Cards)

    def Shuffle(self):
        for Count in range(10000):
            RNo1 = random.randint(0, len(self._Cards) - 1)
            RNo2 = random.randint(0, len(self._Cards) - 1)
            TempCard = self._Cards[RNo1]
            self._Cards[RNo1] = self._Cards[RNo2]
            self._Cards[RNo2] = TempCard

    def RemoveCard(self, CardNumber):
        CardFound = False
        Pos = 0
        while Pos < len(self._Cards) and not CardFound:
            if self._Cards[Pos].GetCardNumber() == CardNumber:
                CardToGet = self._Cards[Pos]
                CardFound = True
                self._Cards.pop(Pos)
            Pos += 1

        CardString = CardToGet.GetDescription()
        CardType = CardString[0]
        if CardType == "K":
            self._NumKeys -= 1
        elif CardType == "F":
            self._NumFiles -= 1
        elif CardType == "P":
            self._NumPicks -= 1

        self._Stats.append(CardString)
        return CardToGet

    def DisplayStats(self):
        NumOfCards = self.GetNumberOfCards()
        PercentageKeys = (self._NumKeys / NumOfCards) * 100
        PercentageFiles = (self._NumFiles / NumOfCards) * 100
        PercentagePics = (self._NumPicks / NumOfCards) * 100
        Msg = f"There is a {PercentageKeys:.2f}% chance that the next card will be a key, a {PercentageFiles:.2f}% " \
            f"chance that it will be a file and a {PercentagePics:.2f}% chance that it will be a pick. "

        return Msg

    def __CreateLineOfDashes(self, Size):
        LineOfDashes = ""
        for Count in range(Size):
            LineOfDashes += "------"
        return LineOfDashes

    def GetCardDisplay(self):
        CardDisplay = "\n" + self._Name + ":"
        if len(self._Cards) == 0:
            return CardDisplay + " empty" + "\n" + "\n"
        else:
            CardDisplay += "\n" + "\n"
        LineOfDashes = ""
        CARDS_PER_LINE = 10
        if len(self._Cards) > CARDS_PER_LINE:
            LineOfDashes = self.__CreateLineOfDashes(CARDS_PER_LINE)
        else:
            LineOfDashes = self.__CreateLineOfDashes(len(self._Cards))
        CardDisplay += LineOfDashes + "\n"
        Complete = False
        Pos = 0
        while not Complete:
            CardDisplay += "| " + self._Cards[Pos].GetDescription() + " "
            Pos += 1
            if Pos % CARDS_PER_LINE == 0:
                CardDisplay += "|" + "\n" + LineOfDashes + "\n"
            if Pos == len(self._Cards):
                Complete = True
        if len(self._Cards) % CARDS_PER_LINE > 0:
            CardDisplay += "|" + "\n"
            if len(self._Cards) > CARDS_PER_LINE:
                LineOfDashes = self.__CreateLineOfDashes(len(self._Cards) % CARDS_PER_LINE)
            CardDisplay += LineOfDashes + "\n"
        return CardDisplay
