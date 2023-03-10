"""
A module for associative cards managing.

Author: Anton Dmytrenko
Version: 1.0
"""

import enum
import configparser
import json
import random
from datetime import datetime as dt


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


class BrainSettings:
    """A class to represent a Telegram-bot settings."""

    _parser = None

    def __init__(self, path='config.ini'):
        parser = configparser.ConfigParser()
        parser.read(path, 'utf-8')
        self._parser = parser

    def cards_path(self):
        return self._read_setting('DATABASE', 'CARDS_PATH')

    def _read_setting(self, section, name):
        return self._parser[section][name]


class CardBox:
    """
    A class to represent a box to put associative cards in.

    Methods
    -------
    add_card(card : Card) : bool
        Adds a card to the card-box

    learn_cards() : list
        Returns the cards to learn

    save_cards() : None
        Saves the cards' data in to the file
    """

    _settings = None
    _cards = []

    def __init__(self):
        self._settings = BrainSettings()
        self._load_cards()

    def add_card(self, card):
        """
        Adds a card to the card-box

        Attributes
        -------
        card : Card
            The card to add

        Returns
        -------
        True - if the card is added, and False - there is a card with the same word
        """

        if card in self._cards:
            return False

        self._cards.append(card)
        self.save_cards()

        return True

    def learn_cards(self):
        cards = []
        for card in self._cards:
            if card.status in (MemorizeStatuses.Default, MemorizeStatuses.Day):
                cards.append(card)
            elif card.status == MemorizeStatuses.Week and dt.now().weekday() <= 2:
                cards.append(card)
            elif card.status == MemorizeStatuses.Month and dt.now().day <= 2:
                cards.append(card)
            elif card.status == MemorizeStatuses.Year and dt.now().month == 1 and dt.now().day <= 2:
                cards.append(card)

        random.shuffle(cards)

        return cards

    def save_cards(self):
        """
        Saves the cards' data to the file

        Returns
        -------
        None
        """

        path = self._settings.cards_path()
        with open(path, 'w', encoding='utf-8') as f:
            for card in self._cards:
                data = {
                    'word': card.word,
                    'translation': card.translation,
                    'association': card.association,
                    'status': card.status.value
                }
                line = json.dumps(data) + '\n'
                f.write(line)

    def _load_cards(self):
        """
        Reads the cards' data from the file to initiate a card-box

        Returns
        -------
        None
        """

        path = self._settings.cards_path()
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                data = json.loads(line.replace('\n', ''))
                card = Card(data['word'], data['translation'], data['association'], data['status'])
                self.add_card(card)


class Card:
    """
    A class to represent an associative card with a translation on the front side
    and a association sentence and a learning word on the front side and  of the card.

    Attributes
    ----------
    word : str
        The word to learn itself

    association : str
        The association with the learning word

    translation : str
        The translation of the learning word

    status : MemorizeStatuses
        The memorizing status of the card

    Methods
    -------
    get_heads() : str
        Returns a front side of the card

    get_tails() : str
        Returns a back side of the card

    check_word(word : str) : bool
        Updates the status of the word memorizing process and returns the correctness

    Example
    -------
        'Z??ZVOR'
        ===============================================>
        'I don't eat pink-coloured Z??ZVOR with sushi'
    """

    _word = ''
    _translation = ''
    _association = ''
    _status = None

    def __init__(self, word, translation, association, status=0):
        new_word = word.strip().lower()
        new_translation = translation.strip().lower()
        new_association = association.strip().lower()

        if not new_word or not new_translation or not new_association:
            return
        if new_word not in new_association:
            return

        self.word = new_word
        self.translation = new_translation
        self.association = new_association
        self.status = status

    def __eq__(self, other):
        return self.word == other.word or self.translation == other.translation

    def __bool__(self):
        if self.word and self.translation:
            return True
        else:
            return False

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, word):
        self._word = word

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, translation):
        self._translation = translation

    @property
    def association(self):
        return self._association

    @association.setter
    def association(self, association):
        self._association = association

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if MemorizeStatuses.Default.value <= status <= MemorizeStatuses.BrainCarded.value:
            self._status = MemorizeStatuses(status)

    def get_heads(self):
        """
        Returns the front side of the card that contains the translation of the learning word.

        Returns
        -------
        str
            The translation of the learning word
        """

        return self._translation

    def get_tails(self):
        """
        Returns the back side of the card that contains the association with the learning word.

        Returns
        -------
        str
            The association with the learning word
        """

        return self._association

    def check_word(self, word):
        """
        Checks if the word equals the check word and updates the status.

        Attributes
        -------
        word : str
            The origin language word to check

        Returns
        -------
        True - if the word suggestion is correct, False - otherwise
        """

        correct = self.word == word
        self._update_status(correct)

        return correct

    def _update_status(self, success):
        iterator = 1 if success else -1
        new_status = self.status.value + iterator
        self.status = new_status
