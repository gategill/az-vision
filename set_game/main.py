from random import randint

from PIL import Image, ImageDraw

# Define the properties of the Set card
card_width, card_height = 200, 300


symbol_shape = "oval"  # 'diamond', 'squiggle', or 'oval'
symbol_count = 1  # 1, 2, or 3
symbol_color = "red"  # 'red', 'green', or 'purple'
symbol_shading = "solid"  # 'solid', 'striped', or 'open'

# Create a new image with white background
card = Image.new("RGB", (card_width, card_height), "white")
draw = ImageDraw.Draw(card)


# Function to draw an oval (replace this function to draw other shapes)
def draw_oval(draw, bounding_box, color, shading):
    if shading == "solid":
        draw.ellipse(bounding_box, fill=color)
    elif shading == "striped":
        # Draw striped shading
        for i in range(bounding_box[0], bounding_box[2], 4):
            draw.line([(i, bounding_box[1]), (i, bounding_box[3])], fill=color)
    else:
        # Draw open (outline only)
        draw.ellipse(bounding_box, outline=color)


# Calculate the position and size of the symbol(s)
symbol_width = card_width // 4
symbol_height = card_height // 4
symbol_x_spacing = (card_width - symbol_width) // 2
symbol_y_start = (card_height - (symbol_count * symbol_height)) // 2

# Draw the symbol(s) on the card
for i in range(symbol_count):
    symbol_y_position = symbol_y_start + (i * symbol_height)
    bounding_box = [
        symbol_x_spacing,
        symbol_y_position,
        symbol_x_spacing + symbol_width,
        symbol_y_position + symbol_height,
    ]

    # Draw the symbol based on its shape
    if symbol_shape == "oval":
        draw_oval(draw, bounding_box, symbol_color, symbol_shading)
    # Add more conditions to draw other shapes
r = randint(1, 99999)
# Save the image
card.save(f"data/set_card_{r}.png")

# Display the image
# card.show()


# Define the properties of the Set cards
numbers = [1, 2, 3]
shapes = ["diamond", "squiggle", "oval"]
shadings = ["solid", "striped", "open"]
colors = ["red", "green", "purple"]


# Function to draw the shapes on the card
def draw_shape(draw, shape, bounding_box, color, shading):
    # Add your shape drawing logic here

    if shape == "oval":

        pass


# Create a new image for each combination
for number in numbers:
    for shape in shapes:
        for shading in shadings:
            for color in colors:
                # Create a new image with white background
                card = Image.new("RGB", (200, 300), "white")
                draw = ImageDraw.Draw(card)

                # Add your logic to place and draw the shapes on the card
                # ...

                # Save the image with a unique filename
                filename = f"set_card_{number}_{shape}_{shading}_{color}.png"
                card.save(filename)
