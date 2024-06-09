from itertools import combinations


def is_set(card1, card2, card3):
    """Check if three cards form a Set."""
    for feature in zip(card1, card2, card3):
        if not (
            all(f == feature[0] for f in feature)
            or all(f != feature[0] for f in feature)
        ):
            return False
    return True


def find_sets(cards):
    """Find all Sets in the list of cards."""
    sets_found = []
    for combo in combinations(cards, 3):
        if is_set(*combo):
            sets_found.append(combo)
    return sets_found


# Example usage:
# Each card is represented as a tuple of features (number, shape, shading, color)
cards = [
    (1, "oval", "solid", "red"),
    (2, "diamond", "striped", "green"),
    (3, "squiggle", "open", "purple"),
    # ... include all identified cards
]

sets = find_sets(cards)
print(f"Sets found: {len(sets)}")
for s in sets:
    print(s)


class SetCard:
    def __init__(self, number, shape, shading, color):
        self.number = number
        self.shape = shape
        self.shading = shading
        self.color = color

    def __repr__(self):
        return f"SetCard(number={self.number}, shape='{self.shape}', shading='{self.shading}', color='{self.color}')"
