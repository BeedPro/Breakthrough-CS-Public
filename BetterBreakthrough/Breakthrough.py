# Skeleton Program code for the AQA A Level Paper 1 Summer 2022 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed in the Python 3.9 programming environment

import random
import os

from PythonFile.Breakthrough.BetterBreakthrough.CardCollection import CardCollection
from PythonFile.Breakthrough.BetterBreakthrough.DifficultyCard import DifficultyCard
from PythonFile.Breakthrough.BetterBreakthrough.Lock import Lock
from PythonFile.Breakthrough.BetterBreakthrough.ToolCard import ToolCard


def Main():
    ThisGame = Breakthrough()
    ThisGame.PlayGame()


class Breakthrough:
    def __init__(self):
        self.__Deck = CardCollection("DECK")
        self.__Hand = CardCollection("HAND")
        self.__Sequence = CardCollection("SEQUENCE")
        self.__Discard = CardCollection("DISCARD")
        self.__Score = 0
        self.__Locks = []
        self.__GameOver = False
        self.__CurrentLock = Lock()
        self.__LockSolved = False
        self.__LoadLocks()
        self.__BonusPool = 0

    def PlayGame(self):
        if len(self.__Locks) > 0:
            self.__SetupGame()
            while not self.__GameOver:
                self.__LockSolved = False
                while not self.__LockSolved and not self.__GameOver:
                    print()
                    print("Current score:", self.__Score)
                    print(self.__CurrentLock.GetLockDetails())
                    print(self.__Sequence.GetCardDisplay())
                    print(self.__Hand.GetCardDisplay())

                    MenuChoice = self.__GetChoice()
                    if MenuChoice == "D":
                        print(self.__Discard.GetCardDisplay())
                    elif MenuChoice == "U":
                        CardChoice = self.__GetCardChoice()
                        DiscardOrPlay = self.__GetDiscardOrPlayChoice()
                        if DiscardOrPlay == "D":
                            self.__MoveCard(self.__Hand, self.__Discard, self.__Hand.GetCardNumberAt(CardChoice - 1))
                            self.__GetCardFromDeck(CardChoice)
                        elif DiscardOrPlay == "P":
                            self.__PlayCardToSequence(CardChoice)
                    elif MenuChoice == "Q":
                        self.__Score += self.__Deck.GetNumberOfCards()
                        print(f"Final Score: {self.__Score}")
                        self.__GameOver = True

                    if self.__CurrentLock.GetLockSolved():
                        self.__LockSolved = True
                        self.__ProcessLockSolved()
                if self.__GameOver:
                    break
                self.__GameOver = self.__CheckIfPlayerHasLost()
        else:
            print("No locks in file.")

    def __ProcessLockSolved(self):
        self.__Score += 10
        print("Lock has been solved.  Your score is now:", self.__Score)
        while self.__Discard.GetNumberOfCards() > 0:
            self.__MoveCard(self.__Discard, self.__Deck, self.__Discard.GetCardNumberAt(0))
        self.__Deck.Shuffle()
        self.__CurrentLock = self.__GetRandomLock()

    def __CheckIfPlayerHasLost(self):
        if self.__Deck.GetNumberOfCards() == 0:
            print("You have run out of cards in your deck.  Your final score is:", self.__Score)
            return True
        else:
            return False

    def __SetupGame(self):
        Choice = input("Enter L to load a game from a file, anything else to play a new game:> ").upper()
        if Choice == "L":
            FileName = input("Enter the filename :> ")
            if not self.__LoadGame(f"{FileName}.txt"):
                self.__GameOver = True
        else:
            self.__CreateStandardDeck()
            self.__Deck.Shuffle()
            for Count in range(5):
                self.__MoveCard(self.__Deck, self.__Hand, self.__Deck.GetCardNumberAt(0))
            self.__AddDifficultyCardsToDeck()
            self.__Deck.Shuffle()
            self.__CurrentLock = self.__GetRandomLock()

    def __PlayCardToSequence(self, CardChoice):
        if self.__Sequence.GetNumberOfCards() > 0:
            if self.__Hand.GetCardDescriptionAt(CardChoice - 1)[0] != \
                    self.__Sequence.GetCardDescriptionAt(self.__Sequence.GetNumberOfCards() - 1)[0]:
                self.__Score += self.__MoveCard(self.__Hand, self.__Sequence,
                                                self.__Hand.GetCardNumberAt(CardChoice - 1))
                self.__GetCardFromDeck(CardChoice)
        else:
            self.__Score += self.__MoveCard(self.__Hand, self.__Sequence, self.__Hand.GetCardNumberAt(CardChoice - 1))
            self.__GetCardFromDeck(CardChoice)
        if self.__CheckIfLockChallengeMet():
            print()
            print("A challenge on the lock has been met.")
            print()
            self.__Score += 5
        if self.__CurrentLock.IsPartial(self.__Sequence):
            self.__BonusPool += 5
            self.__Score += self.__BonusPool
        else:
            self.__BonusPool = 0

    def __CheckIfLockChallengeMet(self):
        SequenceAsString = ""
        for Count in range(self.__Sequence.GetNumberOfCards() - 1, max(0, self.__Sequence.GetNumberOfCards() - 3) - 1,
                           -1):
            if len(SequenceAsString) > 0:
                SequenceAsString = ", " + SequenceAsString
            SequenceAsString = self.__Sequence.GetCardDescriptionAt(Count) + SequenceAsString
            if self.__CurrentLock.CheckIfConditionMet(SequenceAsString):
                return True
        return False

    def __SetupCardCollectionFromGameFile(self, LineFromFile, CardCol):
        if len(LineFromFile) > 0:
            SplitLine = LineFromFile.split(",")
            for Item in SplitLine:
                if len(Item) == 5:
                    CardNumber = int(Item[4])
                else:
                    CardNumber = int(Item[4:6])
                if Item[0: 3] == "Dif":
                    CurrentCard = DifficultyCard(CardNumber)
                    CardCol.AddCard(CurrentCard)
                else:
                    CurrentCard = ToolCard(Item[0], Item[2], CardNumber)
                    CardCol.AddCard(CurrentCard)

    def __SetupLock(self, Line1, Line2):
        SplitLine = Line1.split(";")
        for Item in SplitLine:
            Conditions = Item.split(",")
            self.__CurrentLock.AddChallenge(Conditions)
        SplitLine = Line2.split(";")
        for Count in range(0, len(SplitLine)):
            if SplitLine[Count] == "Y":
                self.__CurrentLock.SetChallengeMet(Count, True)

    def __LoadGame(self, FileName):
        try:
            with open(FileName) as f:
                LineFromFile = f.readline().rstrip()
                self.__Score = int(LineFromFile)
                LineFromFile = f.readline().rstrip()
                LineFromFile2 = f.readline().rstrip()
                self.__SetupLock(LineFromFile, LineFromFile2)
                LineFromFile = f.readline().rstrip()
                self.__SetupCardCollectionFromGameFile(LineFromFile, self.__Hand)
                LineFromFile = f.readline().rstrip()
                self.__SetupCardCollectionFromGameFile(LineFromFile, self.__Sequence)
                LineFromFile = f.readline().rstrip()
                self.__SetupCardCollectionFromGameFile(LineFromFile, self.__Discard)
                LineFromFile = f.readline().rstrip()
                self.__SetupCardCollectionFromGameFile(LineFromFile, self.__Deck)
                return True
        except:
            print("File not loaded")
            return False

    def __LoadLocks(self):
        FileName = "locks.txt"
        self.__Locks = []
        try:
            with open(FileName) as f:
                LineFromFile = f.readline().rstrip()
                while LineFromFile != "":
                    Challenges = LineFromFile.split(";")
                    LockFromFile = Lock()
                    for C in Challenges:
                        Conditions = C.split(",")
                        LockFromFile.AddChallenge(Conditions)
                    self.__Locks.append(LockFromFile)
                    LineFromFile = f.readline().rstrip()
        except:
            print("File not loaded")

    def __GetRandomLock(self):
        return self.__Locks[random.randint(0, len(self.__Locks) - 1)]

    def __GetCardFromDeck(self, CardChoice):
        if self.__Deck.GetNumberOfCards() > 0:
            if self.__Deck.GetCardDescriptionAt(0) == "Dif":
                CurrentCard = self.__Deck.RemoveCard(self.__Deck.GetCardNumberAt(0))
                print()
                print("Difficulty encountered!")
                print(self.__Hand.GetCardDisplay())
                print(self.__Deck.DisplayStats())
                print("To deal with this you need to either lose a key ", end='')
                Choice = input("(enter 1-5 to specify position of key) or (D)iscard five cards from the deck:> ")
                print()
                self.__Discard.AddCard(CurrentCard)
                CurrentCard.Process(self.__Deck, self.__Discard, self.__Hand, self.__Sequence, self.__CurrentLock,
                                    Choice, CardChoice)
        while self.__Hand.GetNumberOfCards() < 5 and self.__Deck.GetNumberOfCards() > 0:
            if self.__Deck.GetCardDescriptionAt(0) == "Dif":
                self.__MoveCard(self.__Deck, self.__Discard, self.__Deck.GetCardNumberAt(0))
                print("A difficulty card was discarded from the deck when refilling the hand.")
            else:
                self.__MoveCard(self.__Deck, self.__Hand, self.__Deck.GetCardNumberAt(0))
        if self.__Deck.GetNumberOfCards() == 0 and self.__Hand.GetNumberOfCards() < 5:
            self.__GameOver = True

    def __GetCardChoice(self):
        Choice = None
        while Choice is None:
            try:
                Choice = int(input("Enter a number between 1 and 5 to specify card to use:> "))
            except:
                pass
        return Choice

    def __GetDiscardOrPlayChoice(self):
        Choice = input("(D)iscard or (P)lay?:> ").upper()
        return Choice

    def __GetChoice(self):
        print()
        Choice = input("(D)iscard inspect, (U)se card, (Q)uit:> ").upper()
        return Choice

    def __AddDifficultyCardsToDeck(self):
        for Count in range(5):
            self.__Deck.AddCard(DifficultyCard())

    def __CreateStandardDeck(self):
        for Count in range(5):
            NewCard = ToolCard("P", "a")
            self.__Deck.AddCard(NewCard)
            NewCard = ToolCard("P", "b")
            self.__Deck.AddCard(NewCard)
            NewCard = ToolCard("P", "c")
            self.__Deck.AddCard(NewCard)
        for Count in range(3):
            NewCard = ToolCard("F", "a")
            self.__Deck.AddCard(NewCard)
            NewCard = ToolCard("F", "b")
            self.__Deck.AddCard(NewCard)
            NewCard = ToolCard("F", "c")
            self.__Deck.AddCard(NewCard)
            NewCard = ToolCard("K", "a")
            self.__Deck.AddCard(NewCard)
            NewCard = ToolCard("K", "b")
            self.__Deck.AddCard(NewCard)
            NewCard = ToolCard("K", "c")
            self.__Deck.AddCard(NewCard)

    def __MoveCard(self, FromCollection, ToCollection, CardNumber):
        Score = 0
        if FromCollection.GetName() == "HAND" and ToCollection.GetName() == "SEQUENCE":
            CardToMove = FromCollection.RemoveCard(CardNumber)
            if CardToMove is not None:
                ToCollection.AddCard(CardToMove)
                Score = CardToMove.GetScore()
        else:
            CardToMove = FromCollection.RemoveCard(CardNumber)
            if CardToMove is not None:
                ToCollection.AddCard(CardToMove)
        return Score
