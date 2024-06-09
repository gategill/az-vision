from set_card import SetCard


class SetCardCollection:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        if isinstance(card, SetCard):
            self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f"SetCardCollection with {len(self.cards)} cards: {self.cards}"


# Example usage:
# Create some Set cards
card1 = SetCard(1, "oval", "solid", "red")
card2 = SetCard(2, "squiggle", "striped", "green")
card3 = SetCard(3, "diamond", "open", "purple")

# Create a Set card collection and add cards to it
collection = SetCardCollection()
collection.add_card(card1)
collection.add_card(card2)
collection.add_card(card3)

# Print the collection
print(collection)
