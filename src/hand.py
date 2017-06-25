from src.card import Card
import random

class Hand(object):
    """
    hand includes:
    1. deck that this hand belongs to
    2. direction of this hand
    3. cards have in hand
    4. expected result for playing each card
    """

    # static variables
    max_card_n = 13

    def __init__(self, deck):
        self.cards = set()
        self.deck = deck

    @property
    def card_n(self):
        return len(self.cards)

    def undo_card(self, card):
        assert isinstance(card, Card)
        self.cards.add(card)

    def play_card(self, card):
        if card not in self.cards:
            return False
        self.cards.remove(card)

    def get_color_card(self, color):
        return [card for card in self.cards if card.color == color]

    def best_card(self):
        # todo: implement, this should implement most utilities in function "playCard" in original code
        pass

    def random_card(self):
        color = self.deck.current_color
        viable_card = self.get_color_card(color)
        # do not have card in required color
        if not viable_card:
            card, = random.sample(self.cards, 1)
            return card
        while True:
            card, = random.sample(viable_card, 1)
            if not color or card.color == color:
                break
        return card

    def sorted_hand(self):
        return sorted(self.cards, key=Card.get_key)


    # print out the hand.
    # todo: graphics interface to display hand
    def display(self, direct=""):
        for card in self.sorted_hand():
            print(direct, card.color, Card.card_nums[Card.nums.index(card.num)])
