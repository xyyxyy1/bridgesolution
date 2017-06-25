class Card(object):
    """
    card includes a suit and a number
    """

    # static variables
    colors = ["Club", "Diamond", "Heart", "Spade"]
    nums = list(range(2, 15))
    card_nums = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self, color, num):
        assert isinstance(color, str)
        assert color in Card.colors
        assert isinstance(num, int)
        assert num in Card.nums
        self.color = color
        self.num = num

    def __key(self):
        return self.color, self.num

    def __eq__(self, y):
        return self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    # def __gt__(self, other):
    #     if Card.colors.index(self.color) > Card.colors.index(other.color):
    #         return True
    #     elif self.num > other.num:
    #         return True
    #     else:
    #         return False

    # print out card
    # todo: graphics interface to display hand
    def display(self, direct=""):
        print(direct, self.color, " ", Card.card_nums[Card.nums.index(self.num)])

    @staticmethod
    def get_key(card):
        return card.color, card.num

    # @staticmethod
    # def compare(card1, card2):
    #     if Card.colors.index(card1.color) < Card.colors.index(card2.color):
    #         return -1
    #     elif Card.colors.index(card1.color) > Card.colors.index(card2.color):
    #         return 1
    #     elif card1.num < card2.num:
    #         return -1
    #     elif card1.num > card2.num:
    #         return 1
    #     else:
    #         return 0
