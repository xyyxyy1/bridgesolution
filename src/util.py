from src.card import Card


def complete_deck():
    #13张牌
    full_deck = set()
    for color in Card.colors:
        for num in Card.nums:
            full_deck.add(Card(color, num))
    return full_deck


def next_direc(direc):
    # 下家关系
    if direc == 'North':
        return "East"
    if direc == 'East':
        return "South"
    if direc == 'South':
        return "West"
    if direc == 'West':
        return "North"


def partner(direc):
    # 同伴关系
    if direc == 'Norht':
        return "South"
    if direc == 'East':
        return "West"
    if direc == 'South':
        return "North"
    if direc == 'West':
        return "East"


def winer(a, b, c, d):
    # todo: implement method to compare winner of the turn
    return "N"
