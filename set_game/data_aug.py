import os
import uuid
import logging

import numpy as np
import imgaug.augmenters as iaa
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def augment_image_directory(input_directory, output_directory, num_images_per_file=10, target_char=None):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Define the augmentations
    seq = iaa.Sequential(
        [
            iaa.Affine(rotate=(-25, 25)),  # rotate image
            iaa.AdditiveGaussianNoise(scale=(10, 60)),  # add noise
            iaa.Crop(percent=(0, 0.2)),  # crop image
            iaa.LinearContrast((0.5, 2.0)),  # change contrast
            iaa.Multiply((0.8, 1.2)),  # change brightness
            iaa.Affine(scale={"x": (0.8, 1.2), "y": (0.8, 1.2)}),  # scale image
        ]
    )
    # Process each image in the input directory
    for i, file_name in enumerate(os.listdir(input_directory), start=1):
        # Check if the file matches the target character
        if target_char and len(file_name) > 3 and file_name[3].upper() != target_char.upper():
            continue
        
        image_path = os.path.join(input_directory, file_name)

        logger.info(f"Processing file {i} - {file_name}")

        # Check if the file is an image
        if not (
            file_name.endswith(".jpg")
            or file_name.endswith(".png")
            or file_name.endswith(".jpeg")
        ):
            continue

        # Open the image file
        img = Image.open(image_path)
        img_np = np.array(img)
        base_name = os.path.splitext(file_name)[0]

        # Generate augmented images
        for i in range(num_images_per_file):
            tag = str(uuid.uuid4())
            aug_img_np = seq(image=img_np)
            aug_img = Image.fromarray(aug_img_np)
            new_file_name = f"{base_name}_{tag}.jpg"
            logger.info(f"Saving {new_file_name}")
            aug_img.save(os.path.join(output_directory, new_file_name))


def augment_image(image_path, output_directory, num_images_per_file=10):
    # Define the augmentations
    seq = iaa.Sequential(
        [
            iaa.Affine(rotate=(-25, 25)),  # rotate image
            iaa.AdditiveGaussianNoise(scale=(10, 60)),  # add noise
            iaa.Crop(percent=(0, 0.2)),  # crop image
            iaa.LinearContrast((0.5, 2.0)),  # change contrast
            iaa.Multiply((0.8, 1.2)),  # change brightness
            iaa.Affine(scale={"x": (0.8, 1.2), "y": (0.8, 1.2)}),  # scale image
        ]
    )
    file_name = image_path.split("/")[-1]
    logger.info(f"Processing file {file_name}")

    # Check if the file is an image
    if not (
        file_name.endswith(".jpg")
        or file_name.endswith(".png")
        or file_name.endswith(".jpeg")
    ):
        raise TypeError

    # Open the image file
    img = Image.open(image_path)
    img_np = np.array(img)
    base_name = os.path.splitext(file_name)[0]

    # Generate augmented images
    for i in range(num_images_per_file):
        tag = str(uuid.uuid4())
        aug_img_np = seq(image=img_np)
        aug_img = Image.fromarray(aug_img_np)
        new_file_name = f"{base_name}_{tag}.jpg"
        logger.info(f"Saving {new_file_name}")
        aug_img.save(os.path.join(output_directory, new_file_name))


cards = [
    (1, "oval", "solid", "red"),
    (2, "diamond", "striped", "green"),
    (3, "squiggle", "open", "purple"),
    # ... include all identified cards
]

# Dictionary to map shorthand codes to their full names
feature_map = {
    "R": "Red",
    "E": "Empty",  # Assuming 'E' stands for 'Empty'
    "S": "Squiggle",
    "D": "Diamond",
    "O": "Oval"
}

def translate_card_id(card_id):
    # Extract the individual components from the card ID
    number = int(card_id[0])
    color_code = card_id[1]
    shading_code = card_id[2]
    shape_code = card_id[3]

    # Find the corresponding card in the cards list
    for card in cards:
        if card[0] == number:
            shape = card[1]
            shading = card[2]
            color = card[3]
            break
    else:
        return "Card not found"

    # Construct the full name using the feature map and the card features
    color_full = feature_map.get(color_code.upper(), color)
    shading_full = feature_map.get(shading_code.upper(), shading)
    shape_full = feature_map.get(shape_code.upper(), shape)

    return f"{number}{color_full}{shading_full}{shape_full}"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    input_directory = f"./data/original_compressed"


    outputs = ['dataset_shape'] #, 'dataset_number', 'dataset_filling']
    for output_dir in outputs:
        shapes = ['S', 'D', 'O']
        for shape in shapes:
            target_char = shape
            dic_shape = {"S":"squiggle", "O":"oval", "D":"diamond" }
            target_name = dic_shape[target_char] # -> squiggle

            s = [('test', 3), ('valid', 3), ('train', 10)]

            for dir_name, num_images in s:
                output_directory = f"./{output_dir}/{dir_name}/{target_name}"
                logger.info(f"Saving to {output_directory}")
                augment_image_directory(input_directory, output_directory, num_images_per_file=num_images, target_char=target_char)


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     set_id = "1RES"
#     input_directory = f"./data/here"
#     set_full = translate_card_id(set_id)
#     # set_full = "1RedEmptySquiggle"
#     output_directory = f"./dataset/valid/{set_full}"
#     logging.info(f"Saving to {output_directory}")
#     image_path = f"./data/original/{set_id}.jpg"
#     augment_image_directory(input_directory, output_directory, num_images_per_file=10)
#     augment_image(image_path, output_directory, num_images_per_file=10)
