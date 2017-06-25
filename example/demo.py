from src.table import Table

table = Table()

print(table.players["North"])

new_deck = table.next_deck()
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
