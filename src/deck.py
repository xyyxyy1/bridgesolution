import copy
from src.util import *
from src.hand import Hand
import numpy.random as npr
from src.alpha_beta_minimax import *

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
    total_turns = 13

    def __init__(self, table, deck_num, hands=None):
        self.table = table
        self.deck_num = deck_num
        self.auction = []
        self._trump = None
        self.init_direction()
        self.init_minimax()
        self.current_result = {direct: 0 for direct in self.table.player_directions}
        self.current_direct = self.lead_direct
        self.current_color = None
        self.hands = {direct: Hand(self) for direct in self.table.player_directions}
        self.redeal(hands)
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
    def lead_direct(self):
        return self._lead_direct

    @lead_direct.setter
    def lead_direct(self, direct):
        if not direct or direct not in self.table.player_directions:
            self._lead_direct = self.table.player_directions[-1]
        else:
            self._lead_direct = direct

    @property
    def vulnerability(self):
        return self.table.vulnerability_table[(self.deck_num - 1) % len(self.table.vulnerability_table)]

    @property
    def open_bidder(self):
        return self.table.player_directions[(self.deck_num - 1) % len(self.table.player_directions)]

    @property
    def viable_cards(self):
        cards = [card for card in self.hands[self.current_direct].cards if card.color == self.current_color]
        if not cards:
            cards = self.hands[self.current_direct].cards
        # todo: compute equal cards to get simpler card format
        return cards

    def redeal(self, hands):
        if not hands:
            full_deck = complete_deck()
            while full_deck:
                card = full_deck.pop()
                direct = self.table.player_directions[npr.randint(4)]
                if self.hands[direct].card_n < Hand.max_card_n:
                    self.hands[direct].undo_card(card)
                else:
                    full_deck.add(card)
        else:
            for direct, hand in hands.items():
                for color, nums in hand.items():
                    for num in nums:
                        self.hands[direct].undo_card(Card(color, num))



    def init_direction(self, lead_direct=None):
        self.lead_direct = lead_direct
        if lead_direct in ["North", "South"]:
            self.declare_direct = ["East", "West"]
            self.defence_direct = ["North", "South"]
        else:
            self.declare_direct = ["North", "South"]
            self.defence_direct = ["East", "West"]

    def init_minimax(self):
        self.max_winners = Deck.total_turns
        self.min_winners = 0

    def update_minimax(self):
        self.max_winners = min(self.max_winners,
                               Deck.total_turns - sum([self.current_result[direct] for direct in self.declare_direct]))
        self.min_winners = max(self.min_winners,
                               sum([self.current_result[direct] for direct in self.defence_direct]))

    def next_bid(self):
        # todo: method to add bidding process
        pass

    def play_card(self, card):
        # if this is the first card for a new turn, change the color
        if not len(self.played_card) % 4:
            self.current_color = card.color
        self.hands[self.current_direct].play_card(card)
        self.played_card.append(card)
        # if this is the last card for a new turn, compute for result and new direct
        self.current_direct = next_direc(self.current_direct)
        if not len(self.played_card) % 4:
            self.close_turn()

    def undo_card(self, card):
        # if this is the last card for a new turn, compute for result and new direct
        if not len(self.played_card) % 4:
            self.reverse_close_turn()
        self.current_direct = previous_direc(self.current_direct)
        self.hands[self.current_direct].undo_card(card)
        self.played_card.pop()
        # if this now is the first card for a new turn, change the color
        if not len(self.played_card) % 4:
            self.current_color = None

    # compute the new direction based on last four cards
    def close_turn(self):
        winner_index = winner(self.played_card[-4:], self.trump)
        self.current_direct = self.table.player_directions[
            (self.table.player_directions.index(self.current_direct) + winner_index) % len(self.table.player_directions)]
        self.current_result[self.current_direct] += 1
        self.current_color = None
        self.update_minimax()

    def reverse_close_turn(self):
        winner_index = winner(self.played_card[-4:], self.trump)
        self.current_direct = self.table.player_directions[
            (self.table.player_directions.index(self.current_direct) - winner_index) % len(
                self.table.player_directions)]
        self.current_result[self.current_direct] -= 1
        self.current_color = self.played_card[-4].color
        self.update_minimax()

    # randomly play the hand
    def random_play(self):
        while len(self.played_card) < self.total_card_number:
            card = self.hands[self.current_direct].random_card()
            self.play_card(card)
            # card.display()

    def minimax(self):
        alpha_beta_minimax(self)

    # todo: display the following function in a more elegant way
    def display_played_cards(self):
        print("trump: ", self.trump)
        for n in range(len(self.played_card)):
            direct = [direct for direct, hand in self.original_hands.items() if self.played_card[n] in hand.cards][0]
            self.played_card[n].display(direct)
            if n % 4 == 3:
                print("\n")
