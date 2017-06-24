import copy
from src.util import *
from src.hand import Hand
import numpy.random as npr


class Deck(object):
    """
    deck includes:
    1. table that this deck belongs to
    2. original hands of four players
    3. Auction (叫牌过程)
    4. trump
    5. played card
    6. current result
    7. current hands of four players
    8. current vulnerability(局况)
    9. current open bidder
    """

    # static variables
    trumps = ["Club", "Diamond", "Heart", "Spade", "No trump"]

    def __init__(self, table, deck_num):
        self.table = table
        self.deck_num = deck_num
        self._trump = None
        self.auction = []
        self.current_result = {"NS": 0, "EW": 0}
        self.current_direct = self.open_bidder
        self.current_color = None
        self.hands = {direct: Hand(self) for direct in self.table.player_directions}
        self.redeal()
        self.original_hands = copy.deepcopy(self.hands)
        self.played_card = []

    @property
    def total_card_number(self):
        return sum([hand.card_n for hand in self.original_hands.values()])

    @property
    def trump(self):
        return self._trump

    @trump.setter
    def trump(self, bid_trump):
        if not bid_trump or bid_trump not in Deck.trumps:
            self._trump = self.trumps[-1]
        else:
            self._trump = bid_trump

    @property
    def vulnerability(self):
        return self.table.vulnerability_table[(self.deck_num - 1) % len(self.table.vulnerability_table)]

    @property
    def open_bidder(self):
        return self.table.player_directions[(self.deck_num - 1) % len(self.table.player_directions)]

    def redeal(self):
        full_deck = complete_deck()
        while full_deck:
            card = full_deck.pop()
            direct = self.table.player_directions[npr.randint(4)]
            if self.hands[direct].card_n < Hand.max_card_n:
                self.hands[direct].undo_card(card)
            else:
                full_deck.add(card)

    def next_bid(self):
        # todo: method to add bidding process
        pass

    def play_next_card(self, card):
        self.hands[self.current_direct].play_card(card)
        # if this is the first card for a new turn, change the color
        if not len(self.played_card) % 4:
            self.current_color = card.color
        self.played_card.append(card)
        # if this is the last card for a new turn, compute for result and new direct
        self.current_direct = next_direc(self.current_direct)
        if not len(self.played_card) % 4:
            self.close_turn()

    # compute the new direction based on last four cards
    def close_turn(self):
        # todo: implement this function using winner function
        # include: decide who is the winner
        # change current result
        # change new direction
        self.current_color = None

    # randomly play the hand
    def random_play(self):
        while len(self.played_card) < self.total_card_number:
            card = self.hands[self.current_direct].random_card()
            self.play_next_card(card)
            # card.display()

    # todo: display the following function in a more elegant way
    def display_played_cards(self):
        for n in range(len(self.played_card)):
            self.played_card[n].display()
            if n % 4 == 3:
                print("\n")
