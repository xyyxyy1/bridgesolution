from src.deck import Deck


class Table(object):
    """
    table includes
    1. name for table
    1. names of four players in the table
    2. scoring method: ex. IMP
    3. conventional card for players
    4. table states

    Table states include:
    1. current score
    2. decks played (including current deck)
    """

    # static variable
    # we have four states for vulnerability: "NS", "EW", "-" as both nonvulnerable, "B" as both vulnerable
    vulnerability_table = ["-", "NS", "EW", "B", "NS", "EW", "B", "-", "EW", "B", "-", "NS", "B", "-", "NS", "EW"]
    player_directions = ["North", "East", "South", "West"]

    def __init__(self, table_name=None, player_name=None):
        self.table_name = table_name
        self._players = {}
        self.players = player_name
        self.scoring_method = "IMP"
        self.NS_conventional_card = None
        self.WE_conventional_card = None
        self.deck = {}
        self.deck_num = 0
        self.score = 0
        pass

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, player_name):
        for s in Table.player_directions:
            if player_name and s in player_name:
                self._players[s] = player_name[s]
            elif s not in self._players:
                self._players[s] = s

    def next_deck(self):
        new_deck = Deck(self, self.deck_num)
        self.deck_num += 1
        self.deck[self.deck_num] = new_deck
        return new_deck
