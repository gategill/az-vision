from PIL import Image
import os

def compress_image(input_path, output_path, quality=20):
    """
    Compress an image by reducing its quality to save space.
    
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the compressed image.
        quality (int): Quality of the output image (1-100). Lower means more compression.
        
    Returns:
        None
    """
    # Open the image file
    with Image.open(input_path) as img:
        # Save the image with the specified quality
        img.save(output_path, "JPEG", quality=quality)
        print(f"Compressed image saved at {output_path} with quality={quality}")

def compress_images_in_directory(input_directory, output_directory, quality=20):
    """
    Compress all images in the input directory and save them to the output directory.
    
    Args:
        input_directory (str): Path to the directory containing input images.
        output_directory (str): Path to the directory to save compressed images.
        quality (int): Quality of the output images (1-100). Lower means more compression.
        
    Returns:
        None
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file_name in os.listdir(input_directory):
        # Check if the file is an image
        if not (file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png")):
            continue
        
        input_path = os.path.join(input_directory, file_name)
        output_path = os.path.join(output_directory, file_name)
        
        try:
            compress_image(input_path, output_path, quality)
        except Exception as e:
            print(f"Failed to compress {file_name}: {e}")

# Example usage
if __name__ == "__main__":
    input_dir = f"./data/original"  # Replace with your input directory path
    output_dir = f"./data/original_compressed"  # Replace with your output directory path
    compress_images_in_directory(input_dir, output_dir, quality=10)

# # Example usage
# if __name__ == "__main__":
#     name = '1RED'
#     input_image_path = f"./data/original/{name}.jpg"  
#     output_image_path = f"./data/original_compressed/{name}.jpg"
#     compress_image(input_image_path, output_image_path, quality=20)
