def alpha_beta_minimax(deck):
    """
    Returns best score for the player associated with the given node.
    Also sets the variable bestMove to the move associated with the
    best score at the root node.
    """

    # check if there is no card to play
    cards = deck.viable_cards
    if len(cards) == 0:
        assert(sum([deck.current_result[direct] for direct in deck.table.player_directions]) == deck.total_turns)
        if deck.current_direct in deck.declare_direct:
            return deck.total_turns - sum([deck.current_result[direct] for direct in deck.declare_direct])
        elif deck.current_direct in deck.defence_direct:
            return sum([deck.current_result[direct] for direct in deck.defence_direct])

    # if declare is playing in turn
    if deck.current_direct in deck.declare_direct:
        for card in cards:
            deck.play_card(card)
            new_max_winners = alpha_beta_minimax(deck)
            deck.undo_card(card)
            if new_max_winners < deck.max_winners:
                deck.max_winners = new_max_winners
            if deck.max_winners <= deck.min_winners:
                return deck.max_winners
        return deck.max_winners

    # if defence is playing in turn
    if deck.current_direct in deck.defence_direct:
        for card in cards:
            deck.play_card(card)
            new_min_winners = alpha_beta_minimax(deck)
            deck.undo_card(card)
            if new_min_winners > deck.min_winners:
                deck.min_winners = new_min_winners
            if deck.min_winners >= deck.max_winners:
                return deck.min_winners
        return deck.min_winners
