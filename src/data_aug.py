import os
import uuid
import logging

import numpy as np
import imgaug.augmenters as iaa
from PIL import Image


def augment_image_directory(input_directory, output_directory, num_images_per_file=10):
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
    dir_len = count_jpeg_files(input_directory)
    # Process each image in the input directory
    for i, file_name in enumerate(os.listdir(input_directory), start=1):
        image_path = os.path.join(input_directory, file_name)

        logging.info(f"Processing file {i} of {dir_len} - {file_name}")
        break

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
            aug_img.save(os.path.join(output_directory, new_file_name))


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    input_directory = "./data/original"
    output_directory = "./data/aug"
    augment_image_directory(input_directory, output_directory, num_images_per_file=10)
