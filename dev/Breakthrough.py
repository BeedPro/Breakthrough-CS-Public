"""
Skeleton Program code for the AQA A Level Paper 1 Summer 2022 examination
this code should be used in conjunction with the Preliminary Material
written by the AQA Programmer Team
developed in the Python 3.9 programming environment
"""

"""
Importing the libraries
"""

"""
Main function
"""

import random
import os
def Main():
	ThisGame = Breakthrough()
	ThisGame.PlayGame()


"""
Classes
"""


class Breakthrough():
	def __init__(self):
		"""
		Initialisation of the Breakthrough class by initilaising the defualt values to the resprective fields
		"""
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
	
	def Test(self):
		"""
		Test Function
		"""
		d = DifficultyCard()
		self.__SetupGame()
		print(self.__CheckIfKeyInHand())
			



	def __SaveFile(self):
		with open(f"dev/{input('What is the name of file:> ')}.txt", "w+") as saveFile:
			### Writes Score to the save file
			saveFile.write(f"{self.__Score}\n")

			### Iterates through the challenges and then saves each challenge and its condition
			temp = ''
			for C in self.__CurrentLock._Challenges:
				for Con in C._Condition:
					temp += Con + ","
				temp = temp[:-1] + ";"
			saveFile.write(f"{temp[:-1]}\n")

			### Checks if the challenge has been met
			temp = ''
			for C in self.__CurrentLock._Challenges:
				if C._Met:
					temp += "Y;"
				else:
					temp += "N;"
			saveFile.write(f"{temp[:-1]}\n")

			### Iterates over to get the cards of your hand
			temp = ''
			for card in range(5):
				temp += f"{self.__Hand.GetCardDescriptionAt(card)} {self.__Hand.GetCardNumberAt(card)},"
			saveFile.write(f"{temp[:-1]}\n")

			### Iterates over to get the cards of your sequence
			temp = ''
			for card in range(self.__Sequence.GetNumberOfCards()):
				temp += f"{self.__Sequence.GetCardDescriptionAt(card)} {self.__Sequence.GetCardNumberAt(card)},"
			saveFile.write(f"{temp[:-1]}\n")		

			### Iterates over to get the cards of your discard
			temp = ''
			for card in range(self.__Discard.GetNumberOfCards()):
				temp += f"{self.__Discard.GetCardDescriptionAt(card)} {self.__Discard.GetCardNumberAt(card)},"
			saveFile.write(f"{temp[:-1]}\n")

			### Iterates over to get the cards of your Deck
			temp = ''
			for card in range(self.__Deck.GetNumberOfCards()):
				temp += f"{self.__Deck.GetCardDescriptionAt(card)} {self.__Deck.GetCardNumberAt(card)},"
			saveFile.write(f"{temp[:-1]}")

	def __ProcessLockSolved(self):
		'''
		handles the lock change after its has been solved
		'''
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

	def __ProcessLockSolved(self):
		'''
		handles the lock change after its has been solved
		'''
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

	def PlayGame(self):
		"""
		Main game loop in which the logic of the game on how it is played is within this method the score gets displayed 
		Along with the Lock details, card display of the users hand and the sequence, and handles the MenuChoice of the game.
		"""
		if len(self.__Locks) > 0:
			self.__SetupGame()
			while not self.__GameOver:
				self.__LockSolved = False
				while not self.__LockSolved and not self.__GameOver:
					print()
					print("Current score:", self.__Score)
					print(f"Cards remaining in deck: {self.__Deck.GetNumberOfCards()}")
					print(self.__CurrentLock.GetLockDetails())
					print(self.__Sequence.GetCardDisplay())
					print(self.__Hand.GetCardDisplay())
					MenuChoice = self.__GetChoice()
					ValidMenuChoices = ["D", "U", "S"]
					while MenuChoice.upper() not in ValidMenuChoices:
						print("Not a valid choice")
						MenuChoice = self.__GetChoice()
					if MenuChoice == "D":
						print(self.__Discard.GetCardDisplay())
					elif MenuChoice == "U":
						CardChoice = self.__GetCardChoice()
						DiscardOrPlay = self.__GetDiscardOrPlayChoice()
						ValidDiscardOrPlayChoice = ["D", "P"]
						while DiscardOrPlay.upper() not in ValidDiscardOrPlayChoice:
							print("Not valid choice")
							DiscardOrPlay = self.__GetDiscardOrPlayChoice()
						if DiscardOrPlay == "D":
							self.__MoveCard(
								self.__Hand, self.__Discard, self.__Hand.GetCardNumberAt(CardChoice - 1))
							self.__GetCardFromDeck(CardChoice)
						elif DiscardOrPlay == "P":
							self.__PlayCardToSequence(CardChoice)
					elif MenuChoice.upper() == "S":
						self.__SaveFile()
					if self.__CurrentLock.GetLockSolved():
						self.__LockSolved = True
						self.__ProcessLockSolved()
				self.__GameOver = self.__CheckIfPlayerHasLost()
		else:
			print("No locks in file.")


	def __ProcessLockSolved(self):
		"""
		Checks if the lock has been solved and adds +10 score to the total score and then gets another lock
		randomly in order to get the next lock.
		"""
		self.__Score += 10
		print("Lock has been solved.  Your score is now:", self.__Score)
		while self.__Discard.GetNumberOfCards() > 0:
			self.__MoveCard(self.__Discard, self.__Deck,
							self.__Discard.GetCardNumberAt(0))
		self.__Deck.Shuffle()
		self.__CurrentLock = self.__GetRandomLock()

	def __CheckIfPlayerHasLost(self):
		"""
		Checks if player has lost when the cards in the deck has run out
		"""
		if self.__Deck.GetNumberOfCards() == 0:
			print(
				"You have run out of cards in your deck.  Your final score is:", self.__Score)
			return True
		else:
			return False

	def __SetupGame(self):
		""" 
		Method in order to initialise the setup of the game of game1.txt
		"""
		Choice = input(
			"Enter L to load a game from a file, anything else to play a new game:> ").upper()
		if Choice == "L":
			if not self.__LoadGame("game1.txt"):
				self.__GameOver = True
		else:
			self.__CreateStandardDeck()
			self.__Deck.Shuffle()
			for Count in range(5):
				self.__MoveCard(self.__Deck, self.__Hand,
								self.__Deck.GetCardNumberAt(0))
			self.__AddDifficultyCardsToDeck()
			self.__Deck.Shuffle()
			self.__CurrentLock = self.__GetRandomLock()

	def __PlayCardToSequence(self, CardChoice):
		"""
		Handles if the adding of cards to the sequence and checking if a challenge is on its way to be completed.
		"""
		if self.__Sequence.GetNumberOfCards() > 0:
			if self.__Hand.GetCardDescriptionAt(CardChoice - 1)[0] != self.__Sequence.GetCardDescriptionAt(self.__Sequence.GetNumberOfCards() - 1)[0]:
				self.__Score += self.__MoveCard(
					self.__Hand, self.__Sequence, self.__Hand.GetCardNumberAt(CardChoice - 1))
				self.__GetCardFromDeck(CardChoice)
			else:
				print(
					f"You cannot play the {self.__Hand.GetCardDescriptionAt(CardChoice - 1)[0]} as its the same as the most recently added card to the lock sequence")
		else:
			self.__Score += self.__MoveCard(self.__Hand, self.__Sequence,
											self.__Hand.GetCardNumberAt(CardChoice - 1))
			self.__GetCardFromDeck(CardChoice)
		if self.__CheckIfLockChallengeMet():
			print()
			print("A challenge on the lock has been met.")
			print()
			self.__Score += 5

	def __CheckIfLockChallengeMet(self):
		"""
		Checks in the sequence that if the lock challenges have been met within the sequence of the  cards
		"""
		SequenceAsString = ""
		for Count in range(self.__Sequence.GetNumberOfCards() - 1, max(0, self.__Sequence.GetNumberOfCards() - 3) - 1, -1):
			if len(SequenceAsString) > 0:
				SequenceAsString = ", " + SequenceAsString
			SequenceAsString = self.__Sequence.GetCardDescriptionAt(
				Count) + SequenceAsString
			if self.__CurrentLock.CheckIfConditionMet(SequenceAsString):
				return True
		return False

	def __SetupCardCollectionFromGameFile(self, LineFromFile, CardCol):
		"""
		Get the card sequences from the game file and puts it in a card collection at the start of the game in order to be able to be used in a deck
		"""
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
		"""
		It is used to set up the lock challenges
		"""
		SplitLine = Line1.split(";")
		for Item in SplitLine:
			Conditions = Item.split(",")
			self.__CurrentLock.AddChallenge(Conditions)
		SplitLine = Line2.split(";")
		for Count in range(0, len(SplitLine)):
			if SplitLine[Count] == "Y":
				self.__CurrentLock.SetChallengeMet(Count, True)

	def __LoadGame(self, FileName):
		"""
		This is the initisial class to load in the game1.txt file into memeory in order to be be able to play game
		"""
		try:
			with open(f"dev/{FileName}") as f:
				LineFromFile = f.readline().rstrip()
				self.__Score = int(LineFromFile)
				LineFromFile = f.readline().rstrip()
				LineFromFile2 = f.readline().rstrip()
				self.__SetupLock(LineFromFile, LineFromFile2)
				LineFromFile = f.readline().rstrip()
				self.__SetupCardCollectionFromGameFile(
					LineFromFile, self.__Hand)
				LineFromFile = f.readline().rstrip()
				self.__SetupCardCollectionFromGameFile(
					LineFromFile, self.__Sequence)
				LineFromFile = f.readline().rstrip()
				self.__SetupCardCollectionFromGameFile(
					LineFromFile, self.__Discard)
				LineFromFile = f.readline().rstrip()
				self.__SetupCardCollectionFromGameFile(
					LineFromFile, self.__Deck)
				return True
		except:
			print("File not loaded")
			return False

	def __LoadLocks(self):
		"""
		Getting the challanges from the locks.txt and putting in the __Locks array and to be used later in the game
		"""
		FileName = "dev/locks.txt"
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
		"""
		Return a random lock from the __Lock
		"""
		return self.__Locks[random.randint(0, len(self.__Locks) - 1)]

	def __CheckIfKeyInHand(self):
		for i in range(4):
			if self.__Hand.GetCardDescriptionAt(i)[0] == "K":
				return True 
		return False

	def __GetCardFromDeck(self, CardChoice):
		"""
		From the Deck get the Card if the Deck is not empty and handles Diff cards. Number of cards decrease as it is put on the hand and is 
		checked if the number of card does not go down 
		"""
		if self.__Deck.GetNumberOfCards() > 0:
			if self.__Deck.GetCardDescriptionAt(0) == "Dif":
				CurrentCard = self.__Deck.RemoveCard(
					self.__Deck.GetCardNumberAt(0))
				print()
				print("Difficulty encountered!")
				print(self.__Hand.GetCardDisplay())
				KeyInHand = self.__CheckIfKeyInHand()
				print("To deal with this you need to either lose a key ", end='')
				Choice = input(
					"(enter 1-5 to specify position of key) or if you don't have a key then (D)iscard five cards from the deck:> ")
				print()
				if KeyInHand:
					while not Choice.isdigit():
						Choice = input(
					"(enter 1-5 to specify position of key) or if you don't have a key then (D)iscard five cards from the deck:> ")
					while self.__Hand.GetCardDescriptionAt(int(Choice)-1)[0] != "K":
						print("That was not key")
						Choice = input(
					"(enter 1-5 to specify position of key) or if you don't have a key then (D)iscard five cards from the deck:> ")

				self.__Discard.AddCard(CurrentCard)
				CurrentCard.Process(self.__Deck, self.__Discard, self.__Hand,
									self.__Sequence, self.__CurrentLock, Choice, CardChoice)
		while self.__Hand.GetNumberOfCards() < 5 and self.__Deck.GetNumberOfCards() > 0:
			if self.__Deck.GetCardDescriptionAt(0) == "Dif":
				self.__MoveCard(self.__Deck, self.__Discard,
								self.__Deck.GetCardNumberAt(0))
				print(
					"A difficulty card was discarded from the deck when refilling the hand.")
			else:
				self.__MoveCard(self.__Deck, self.__Hand,
								self.__Deck.GetCardNumberAt(0))
		if self.__Deck.GetNumberOfCards() == 0 and self.__Hand.GetNumberOfCards() < 5:
			self.__GameOver = True

	def __GetCardChoice(self):
		"""
		Handles the card choice from a UserInput based on the index of the hand
		"""
		Choice = None
		while Choice is None:
			try:
				Choice = int(
					input("Enter a number between 1 and 5 to specify card to use:> "))
				if Choice > 5 or Choice < 1:
					raise Exception
			except:
				print("Not a valid number")
				Choice = None
		return Choice

	def __GetDiscardOrPlayChoice(self):
		"""
		Handles the choice of playing or discarding a card
		"""
		Choice = input("(D)iscard or (P)lay?:> ").upper()

		return Choice

	def __GetChoice(self):
		"""
		Handles the choice of what to do
		"""
		print()
		Choice = input("(D)iscard inspect, (U)se card, (S)ave game:> ").upper()
		return Choice

	def __AddDifficultyCardsToDeck(self):
		"""
		Adding Difficulty cards within the Deck
		"""
		for Count in range(5):
			self.__Deck.AddCard(DifficultyCard())

	def __CreateStandardDeck(self):
		"""
		Handeling of creating the normal standard deck
		"""
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
		"""
		Moving cards from one Collection to another Card collection
		"""
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


class Challenge():
	def __init__(self):
		"""
		Init of Challenge
		"""
		self._Met = False
		self._Condition = []

	def GetMet(self):
		"""
		Getter to get Met
		"""
		return self._Met

	def GetCondition(self):
		"""
		Getter to get 
		"""
		return self._Condition

	def SetMet(self, NewValue):
		"""
		Setter to set the new value to Met
		"""
		self._Met = NewValue

	def SetCondition(self, NewCondition):
		"""
		Setter to set the new condition to Condition
		"""
		self._Condition = NewCondition


class Lock():
	def __init__(self):
		"""
		Init of Lock class
		"""
		self._Challenges = []

	def AddChallenge(self, Condition):
		"""
		Adds the Challenge and Sets challenge condition and then appends to _Challenges
		"""
		C = Challenge()
		C.SetCondition(Condition)
		self._Challenges.append(C)

	def __ConvertConditionToString(self, C):
		"""
		Takes the conditions of lock and converts into a string type so it can be outputed
		"""
		ConditionAsString = ""
		for Pos in range(0, len(C) - 1):
			ConditionAsString += C[Pos] + ", "
		ConditionAsString += C[len(C) - 1]
		return ConditionAsString

	def GetLockDetails(self):
		"""
		Getter to get Lock details
		"""
		LockDetails = "\n" + "CURRENT LOCK" + "\n" + "------------" + "\n"
		for C in self._Challenges:
			if C.GetMet():
				LockDetails += "Challenge met: "
			else:
				LockDetails += "Not met:	   "
			LockDetails += self.__ConvertConditionToString(
				C.GetCondition()) + "\n"
		LockDetails += "\n"
		return LockDetails

	def GetLockSolved(self):
		"""
		Getter if Lock is solved
		"""
		for C in self._Challenges:
			if not C.GetMet():
				return False
		return True

	def CheckIfConditionMet(self, Sequence):
		"""
		Checks if the conditions of the challenges of unlocking a lock has been made
		"""
		for C in self._Challenges:
			if not C.GetMet() and Sequence == self.__ConvertConditionToString(C.GetCondition()):
				C.SetMet(True)
				return True
		return False

	def SetChallengeMet(self, Pos, Value):
		"""
		Set if the challenge has been met
		"""
		self._Challenges[Pos].SetMet(Value)

	def GetChallengeMet(self, Pos):
		"""
		Getter to get ChallengeMet
		"""
		return self._Challenges[Pos].GetMet()

	def GetNumberOfChallenges(self):
		"""
		Getter to get how many challenges
		"""
		return len(self._Challenges)


class Card():
	_NextCardNumber = 0

	def __init__(self):
		"""
		Init of Card
		"""
		self._CardNumber = Card._NextCardNumber
		Card._NextCardNumber += 1
		self._Score = 0

	def GetScore(self):
		"""
		Getter for returning score
		"""
		return self._Score

	def Process(self, Deck, Discard, Hand, Sequence, CurrentLock, Choice, CardChoice):
		"""
		Empty
		"""
		pass

	def GetCardNumber(self):
		"""
		Getter for returning Card Number
		"""
		return self._CardNumber

	def GetDescription(self):
		"""
		Getter for returning the description
		"""
		if self._CardNumber < 10:
			return " " + str(self._CardNumber)
		else:
			return str(self._CardNumber)


class ToolCard(Card):
	def __init__(self, *args):
		"""
		Init Tool Card Class
		"""
		self._ToolType = args[0]
		self._Kit = args[1]
		if len(args) == 2:
			super(ToolCard, self).__init__()
		elif len(args) == 3:
			self._CardNumber = args[2]
		self.__SetScore()

	def __SetScore(self):
		"""
		Sets the Score of each tool card
		"""
		if self._ToolType == "K":
			self._Score = 3
		elif self._ToolType == "F":
			self._Score = 2
		elif self._ToolType == "P":
			self._Score = 1

	def GetDescription(self):
		""" 
		Getter for getting the description
		"""
		return self._ToolType + " " + self._Kit


class DifficultyCard(Card):
	def __init__(self, *args):
		"""
		Init of DifficultyCard Inheriting from Card class
		"""
		self._CardType = "Dif"
		if len(args) == 0:
			super(DifficultyCard, self).__init__()
		elif len(args) == 1:
			self._CardNumber = args[0]

	def GetDescription(self):
		""" 
		Getter for getting the description
		"""
		return self._CardType
			

	def Process(self, Deck, Discard, Hand, Sequence, CurrentLock, Choice, CardChoice):
		"""
		It checks the Diff card process, so it checks which card is of Key tool and will discard that if that was inputed by the user
		If the whole hand has to be replaced then it will remove all the 5 cards from hand and replace them
		"""
		ChoiceAsInteger = None
		try:
			ChoiceAsInteger = int(Choice)
		except:
			pass
		
		if ChoiceAsInteger is not None:
			if ChoiceAsInteger >= 1 and ChoiceAsInteger <= 5:
				if ChoiceAsInteger >= CardChoice:
					ChoiceAsInteger -= 1
				elif ChoiceAsInteger > 0:
					ChoiceAsInteger -= 1
				if Hand.GetCardDescriptionAt(ChoiceAsInteger)[0] == "K":
					CardToMove = Hand.RemoveCard(
						Hand.GetCardNumberAt(ChoiceAsInteger))
					Discard.AddCard(CardToMove)
					return None
		Count = 0
		while Count < 5 and Deck.GetNumberOfCards() > 0:
			CardToMove = Deck.RemoveCard(Deck.GetCardNumberAt(0))
			Discard.AddCard(CardToMove)
			Count += 1


class CardCollection():
	def __init__(self, N):
		"""
		Init CardCollection
		"""
		self._Name = N
		self._Cards = []

	def GetName(self):
		"""
		Getter for name
		"""
		return self._Name

	def GetCardNumberAt(self, X):
		"""
		Getter for Card number at a postion of X
		"""
		return self._Cards[X].GetCardNumber()

	def GetCardDescriptionAt(self, X):
		"""
		Getter of CardDescription at position of X
		"""
		return self._Cards[X].GetDescription()

	def AddCard(self, C):
		"""
		Appending a Card to _Cards
		"""
		self._Cards.append(C)

	def GetNumberOfCards(self):
		"""
		Getter for the number of cards in a deck
		"""
		return len(self._Cards)

	def Shuffle(self):
		"""
		Shuffles the Deck
		"""
		for Count in range(10000):
			RNo1 = random.randint(0, len(self._Cards) - 1)
			RNo2 = random.randint(0, len(self._Cards) - 1)
			TempCard = self._Cards[RNo1]
			self._Cards[RNo1] = self._Cards[RNo2]
			self._Cards[RNo2] = TempCard

	def RemoveCard(self, CardNumber):
		"""
		Removes a card from the deck
		"""
		CardFound = False
		Pos = 0
		while Pos < len(self._Cards) and not CardFound:
			if self._Cards[Pos].GetCardNumber() == CardNumber:
				CardToGet = self._Cards[Pos]
				CardFound = True
				self._Cards.pop(Pos)
			Pos += 1
		return CardToGet

	def __CreateLineOfDashes(self, Size):
		"""
		Creates Lines of Dashes for the output
		"""
		LineOfDashes = ""
		for Count in range(Size):
			LineOfDashes += "------"
		return LineOfDashes

	def GetCardDisplay(self):
		"""
		Gets the card display in the game
		"""
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
				LineOfDashes = self.__CreateLineOfDashes(
					len(self._Cards) % CARDS_PER_LINE)
			CardDisplay += LineOfDashes + "\n"
		return CardDisplay


"""
Main loop
"""
if __name__ == "__main__":
	Main()