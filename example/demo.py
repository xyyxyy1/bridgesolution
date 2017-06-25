from src.table import Table

table = Table()

print(table.players["North"])

## simulate a random hand
# new_deck = table.next_deck()

# hand are listed in following colors: club, diamond, heart, spade
hands = {}
hands["North"] = {}
hands["North"]["Club"] = [14,9,7]
hands["North"]["Diamond"] = [8,7]
hands["North"]["Heart"] = [14,6,4,3,2]
hands["North"]["Spade"] = [13,5,2]
hands["East"] = {}
hands["East"]["Club"] = [13,12,11]
hands["East"]["Diamond"] = [12,11,10,6]
hands["East"]["Heart"] = [12,11,8,7]
hands["East"]["Spade"] = [9,4]
hands["South"] = {}
hands["South"]["Club"] = [10,2]
hands["South"]["Diamond"] = [14,13,5,4,3]
hands["South"]["Heart"] = [13,10]
hands["South"]["Spade"] = [14,8,6,3]
hands["West"] = {}
hands["West"]["Club"] = [8,6,5,4,3]
hands["West"]["Diamond"] = [9,2]
hands["West"]["Heart"] = [9,5]
hands["West"]["Spade"] = [12,11,10,7]

new_deck = table.next_deck(hands)


for direct in Table.player_directions:
    hand = new_deck.hands[direct]
    print("\n hand of ", direct, "\n")
    hand.display()

# # test 1: random play
# new_deck.random_play()
# print("\nplayed hand: ")
# new_deck.display_played_cards()

# test 2: minimax
new_deck.minimax()
print("deck.max_winners: ", new_deck.max_winners)
print("deck.min_winners: ", new_deck.min_winners)
