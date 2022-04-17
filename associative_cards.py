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


class Card:
    """
    A class to represent an associative card with a association sentence and a learning word on the front side
    and a translation on the back side of the card.

    Attributes
    ----------
    word : Word
        A learning word with a detailed information
    association : str
        An association sentence where the word is used
    translation : str
        A translation of the word for the current association context
    status : MemorizeStatuses
        A status of the word memorizing process

    Methods
    -------
    get_get_front_side() : str
        Returns a front side of the card

    get_get_back_side() : str
        Returns a back side of the card

    update_status(status : MemorizeStatuses) : bool
        Updates the status of the word memorizing process

    Example
    -------
        'Заказывая суши, я никогда не ем красный GINGER'
        ===============================================>
        'ИМБИРЬ'
    """

    _word = None
    _association = ''
    _translation = ''
    _status = MemorizeStatuses.Default

    def __init__(self, word, translation, association):
        self.word(word)
        self.translation(translation)
        self.association(association)

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
        self._status = status

    def get_front_side(self):
        """
        Returns a front side of the card that contains the association with the learning word.

        Returns
        -------
        str
            The association with the learning word
        """

        return self.association

    def get_back_side(self):
        """
        Returns a back side of the card that contains the translation of the learning word.

        Returns
        -------
        str
            The translation of the learning word
        """

        return self.translation

    def update_status(self, status):
        """
        Updates the status of the word memorizing process.

        Attributes
        -------
        status : MemorizeStatuses
            A new status of the word memorizing process

        Returns
        -------
        bool
            True - in case the status is successfully changed, and False - otherwise
        """

        success = False
        new_status = MemorizeStatuses.Default
        if self.status + 1 == status:
            new_status = status
            success = True

        self.status(new_status)

        return success


class Word:
    """
    A class to represent a learning Word with a detailed information.

    Attributes
    ----------
    word : str
        A learning word itself
    translations : tuple(str)
        Different translations of the word
    pronunciation : str
        A native pronunciation of the word
    transcription : str
        An original language transcription of the word

    Methods
    -------
    str_translation() : str
        Returns a translation string for the word

    add_translation(translation : str) : bool
        Adds a new translation to the current translations

    Example
    -------
        'word': 'ginger'
        'translations': ('имбирь', 'пикантность')
        'pronunciation': 'джинджер'
        'transcription': '[j i n j ə r]'
    """

    _word = ''
    _translations = set()
    _transcription = ''
    _pronunciation = ''

    def __init__(self, word, translation, pronunciation='', transcription=''):
        self.word(word)
        self.add_translation(translation)
        self.pronunciation(pronunciation)
        self.transcription(transcription)

    def __eq__(self, other):
        return self.word == other.word

    def __str__(self):
        """Override method returns a detailed information about the word."""

        details = 'Word: {}\nTranslations: {}\nPronunciation: {}\nTranscription: {}'.format(
            self.word,
            self.str_translation(),
            self.pronunciation,
            self.transcription
        )

        return details

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, word):
        self._word = word.strip().lower()

    @property
    def translations(self):
        return self._translations

    @property
    def transcription(self):
        return self._transcription

    @transcription.setter
    def transcription(self, transcription):
        self._transcription = transcription.strip().lower()

    @property
    def pronunciation(self):
        return self._pronunciation

    @pronunciation.setter
    def pronunciation(self, pronunciation):
        self._pronunciation = pronunciation.strip().lower()

    def str_translation(self):
        """
        Returns a translation string for the word.

        Returns
        -------
        str
            A translation string for the word
        """

        translation_str = ''
        for word in self.translations:
            translation_str = translation_str + ',' + word if translation_str else translation_str + word

        return translation_str

    def add_translation(self, translation):
        """
        Adds a new translation to the current translations.

        Attributes
        -------
        translation : str
            A new translation to be added

        Returns
        -------
        bool
            True - in case a new translation is unique, and False - otherwise
        """

        translations = self.translations
        new_translation = translation.strip().lower()
        if new_translation in translations:
            return False

        current_translations = list(translations)
        current_translations.append(new_translation)
        unique_translations = set(current_translations)

        self._translations = (x for x in unique_translations)

        return True
