def gen1():
    # Define the properties of the Set cards
    numbers = [1, 2, 3]
    shapes = ["diamond", "squiggle", "oval"]
    shadings = ["solid", "striped", "open"]
    colors = ["red", "green", "purple"]

    # Generate all unique cards and assign an ID to each
    cards = []
    card_ids = []
    for number in numbers:
        for shape in shapes:
            for shading in shadings:
                for color in colors:
                    # cards.append({'id': card_id, 'number': number, 'shape': shape, 'shading': shading, 'color': color})
                    card_id = f"{number}-{color}-{shading}-{shape}"
                    card_ids.append(card_id)

    # Print the list of all cards
    for card_id in card_ids:
        print(card_id)


def gen2():
    # Define the properties of the Set cards
    numbers = ["1", "2", "3"]  # numbers
    shapes = ["D", "S", "O"]  # diamond, squiggle, oval
    shadings = ["S", "O", "E"]  # solid, opaque, empty
    colors = ["R", "G", "P"]  # red, green, purple

    # Generate all unique cards and assign an ID to each
    cards = []
    card_ids = []
    for number in numbers:
        for shape in shapes:
            for shading in shadings:
                for color in colors:
                    card_id = f"{number}{color}{shading}{shape}"
                    card_ids.append(card_id)

    # Print the list of all cards
    for card_id in card_ids:
        print(card_id)


gen2()
