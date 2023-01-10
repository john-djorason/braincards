"""
A module for associative cards managing.

Author: Anton Dmytrenko
Version: 1.0
"""

import enum


class MemorizeStatuses(enum.Enum):
    """
    A class to represent different types of a word memorizing process.

    Values
    -------
    Default - the word is new
    Day - the word has correct match a day before
    Week - the word has correct match a week before
    Month - the word has correct match a month before
    Year - the word has correct match a year before
    BrainCarded - the word is successfully learned
    """

    Default = 0
    Day = 1
    Week = 2
    Month = 3
    Year = 4
    BrainCarded = 5


class CardBox:
    """
    A class to represent a box to put associative cards in.

    Attributes
    ----------
    cards : list
        The associative cards that was put in the box

    Methods
    -------
    get_get_front_side()
        Returns a front side of the card
    """

    _cards = []

    def __init__(self, card):
        self.cards = card

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, card):
        self.cards.append(card)


class Card:
    """
    A class to represent an associative card with a translation on the front side
    and a association sentence and a learning word on the front side and  of the card.

    Attributes
    ----------
    word : str
        The word to learn

    Methods
    -------
    heads() : str
        Returns a front side of the card

    tails() : str
        Returns a back side of the card

    brain(check_word : str) : None
        Updates the status of the word memorizing process

    Example
    -------
        'ИМБИРЬ'
        ===============================================>
        'Заказывая суши, я никогда не ем красный GINGER'
    """

    _word = ''
    _translation = ''
    _association = ''
    _status = None

    def __init__(self, word, translation, association):
        self.word = word
        self.translation = translation
        self.association = association
        self.status = MemorizeStatuses.Default

    def __eq__(self, other):
        return self.word == other.word

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, word):
        self._word = word

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, success):
        iterator = 1 if success else -1
        new_status = self.status.value + iterator
        if MemorizeStatuses.Default.value <= new_status <= MemorizeStatuses.BrainCarded.value:
            self._status = MemorizeStatuses(new_status)

    def heads(self):
        """
        Returns the front side of the card that contains the translation of the learning word.

        Returns
        -------
        str
            The translation of the learning word
        """

        return self._translation

    def tails(self):
        """
        Returns the back side of the card that contains the association with the learning word.

        Returns
        -------
        str
            The association with the learning word
        """

        return self._association

    def brain(self, check_word):
        """
        Checks if the word equals the check_word.

        Attributes
        -------
        check_word : str
            The origin language word to check

        Returns
        -------
        None
        """

        self.status = self.word == check_word
