from PythonFile.Breakthrough.BetterBreakthrough.Challenge import Challenge


class Lock():
    def __init__(self):
        self._Challenges = []

    def AddChallenge(self, Condition):
        C = Challenge()
        C.SetCondition(Condition)
        self._Challenges.append(C)

    def IsPartial(self, Sequence):
        PreviousAddedCard = Sequence.GetCards()[-2] if Sequence.GetNumberOfCards() >= 2 else None
        NewAddedCard = Sequence.GetCards()[-1]

        for C in self._Challenges:
            Condition = C.GetCondition()
            if len(Condition) == 1:
                if NewAddedCard.GetDescription() in Condition:
                    return True
            CardsPlayedConsecutive = NewAddedCard.GetDescription() in Condition and PreviousAddedCard in Condition
            if CardsPlayedConsecutive:
                return True

        return False

    def __ConvertConditionToString(self, C):
        ConditionAsString = ""
        for Pos in range(0, len(C) - 1):
            ConditionAsString += C[Pos] + ", "
        ConditionAsString += C[len(C) - 1]
        return ConditionAsString

    def GetLockDetails(self):
        LockDetails = "\n" + "CURRENT LOCK" + "\n" + "------------" + "\n"
        for C in self._Challenges:
            if C.GetMet():
                LockDetails += "Challenge met: "
            else:
                LockDetails += "Not met:       "
            LockDetails += self.__ConvertConditionToString(C.GetCondition()) + "\n"
        LockDetails += "\n"
        return LockDetails

    def GetLockSolved(self):
        for C in self._Challenges:
            if not C.GetMet():
                return False
        return True

    def CheckIfConditionMet(self, Sequence):
        for C in self._Challenges:
            if not C.GetMet() and Sequence == self.__ConvertConditionToString(C.GetCondition()):
                C.SetMet(True)
                return True
        return False

    def SetChallengeMet(self, Pos, Value):
        self._Challenges[Pos].SetMet(Value)

    def GetChallengeMet(self, Pos):
        return self._Challenges[Pos].GetMet()

    def GetNumberOfChallenges(self):
        return len(self._Challenges)

