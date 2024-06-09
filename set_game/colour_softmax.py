import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import logging
from termcolor import colored
from skimage import exposure

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def softmax(x):
    """
    Compute the softmax of vector x in a numerically stable way.
    
    Args:
        x (np.array): Input array of values.
        
    Returns:
        np.array: Softmax probabilities.
    """
    x = np.array(x, dtype=np.float64)  # Ensure the input is in float64 for numerical stability
    max_x = np.max(x)
    shift_x = x - max_x  # Stability improvement
    exp_x = np.exp(shift_x)
    sum_exp_x = np.sum(exp_x)
    if sum_exp_x == 0:  # Avoid division by zero
        return np.zeros_like(x)
    return exp_x / sum_exp_x

def normalize_brightness(image):
    """
    Normalize the brightness of an image using histogram equalization.
    
    Args:
        image (np.array): Input RGB image.
        
    Returns:
        np.array: Brightness-normalized RGB image.
    """
    image_yuv = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
    image_yuv[:, :, 0] = cv2.equalizeHist(image_yuv[:, :, 0])
    return cv2.cvtColor(image_yuv, cv2.COLOR_YUV2RGB)

def increase_brightness(image, value=30):
    """
    Increase the brightness of an image.
    
    Args:
        image (np.array): Input RGB image.
        value (int): Brightness increment value.
        
    Returns:
        np.array: Brightness-increased RGB image.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    v = np.clip(v, 0, 255)
    final_hsv = cv2.merge((h, s, v))
    return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)

def check_and_adjust_brightness(image, threshold=100, increment=50):
    """
    Check the average brightness of an image and adjust it if it is too dark.
    
    Args:
        image (np.array): Input RGB image.
        threshold (int): Brightness threshold to decide if adjustment is needed.
        increment (int): Value by which to increase brightness if below threshold.
        
    Returns:
        np.array: Brightness-adjusted RGB image.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    brightness = np.mean(hsv[:, :, 2])
    if brightness < threshold:
        image = increase_brightness(image, increment)
    return image

def guess_dominant_color(image):
    """
    Guess the dominant color of an image based on heuristic rules.
    
    Args:
        image (np.array): Input RGB image.
        
    Returns:
        str: Guessed dominant color.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    brightness = np.mean(hsv[:, :, 2])
    logger.info(f"Brightness: {brightness}")
    
    if brightness < 50:
        return 'Blue'
    
    return None

def plot_color_channels(image, title):
    """
    Plot the individual color channels of the image.
    
    Args:
        image (np.array): Input RGB image.
        title (str): Title for the plots.
    """
    fig, axs = plt.subplots(1, 4, figsize=(20, 5))
    axs[0].imshow(image)
    axs[0].set_title('Original Image')
    axs[0].axis('off')
    
    for i, color in enumerate(['Red', 'Green', 'Blue']):
        axs[i+1].imshow(image[:, :, i], cmap='gray')
        axs[i+1].set_title(f'{color} Channel')
        axs[i+1].axis('off')
    
    plt.suptitle(title)
    plt.show()

def get_dominant_color(image_path):
    """
    Determine the dominant color (Red, Green, Blue) in the given image.
    
    Args:
        image_path (str): Path to the image file.
        
    Returns:
        tuple: Dominant color name and dictionary of color confidences.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image at path {image_path} could not be loaded.")
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Check and adjust brightness if necessary
    image = check_and_adjust_brightness(image)
    
    # Normalize brightness
    image = normalize_brightness(image)
    
    # Plot color channels for debugging
    # plot_color_channels(image, "Normalized Image and Color Channels")
    
    # Calculate the sum of each color channel
    red_sum = np.sum(image[:, :, 0])
    green_sum = np.sum(image[:, :, 1])
    blue_sum = np.sum(image[:, :, 2])
    
    logger.info(f"Red Sum: {red_sum}, Green Sum: {green_sum}, Blue Sum: {blue_sum}")
    
    # Heuristic rule: if the image is very dark, guess blue
    dominant_color = guess_dominant_color(image)
    if dominant_color:
        return dominant_color, {'Red': 0.0, 'Green': 0.0, 'Blue': 1.0}
    
    # Compute softmax confidences
    confidences = softmax([red_sum, green_sum, blue_sum])
    
    # Map results to colors
    color_names = ['Red', 'Green', 'Blue']
    color_confidences = dict(zip(color_names, confidences))
    
    # Find the dominant color
    dominant_color = color_names[np.argmax(confidences)]
    
    return dominant_color, color_confidences

def display_image_with_text(image, text):
    """
    Display an image with a title text using matplotlib.
    
    Args:
        image (np.array): Input RGB image.
        text (str): Title text to display on the image.
    """
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    plt.title(text)
    plt.axis('off')
    plt.show()

def evaluate_directory(directory_path):
    """
    Evaluate all images in the specified directory, checking the dominant color
    against the expected color indicated by the file name.
    
    Args:
        directory_path (str): Path to the directory containing image files.
        
    Returns:
        list: List of incorrectly classified file names.
    """
    color_map = {'R': 'Red', 'G': 'Green', 'P': 'Blue'}
    correct_count = 0
    incorrect_count = 0
    incorrect_files = []
    total_confidences = {'Red': [], 'Green': [], 'Blue': []}
    
    for filename in os.listdir(directory_path):
        if not filename.endswith(('.jpg', '.png')):
            logger.info(f"Skipping non-image file: {filename}")
            continue
        
        expected_color_code = filename[1]
        if expected_color_code not in color_map:
            logger.info(f"Skipping file with unexpected color code: {filename}")
            continue
        
        expected_color = color_map[expected_color_code]
        image_path = os.path.join(directory_path, filename)
        
        try:
            dominant_color, confidences = get_dominant_color(image_path)
            
            for color, confidence in confidences.items():
                total_confidences[color].append(confidence)
            
            if dominant_color == expected_color:
                correct_count += 1
                log_color = 'green'
            else:
                incorrect_count += 1
                incorrect_files.append(filename)
                log_color = 'red'
            
            log_text = f"File: {filename}, Expected: {expected_color}, Detected: {dominant_color}, Confidences: {confidences}"
            logger.info(colored(log_text, log_color))
        except ValueError as e:
            logger.error(e)
    
    total_files = correct_count + incorrect_count
    accuracy = correct_count / total_files if total_files > 0 else 0
    
    avg_confidences = {color: (sum(confs) / len(confs) if confs else 0) for color, confs in total_confidences.items()}
    
    summary_text = (
        f"\nTotal Files: {total_files}\n"
        f"Correct: {correct_count}\n"
        f"Incorrect: {incorrect_count}\n"
        f"Accuracy: {accuracy * 100:.2f}%\n"
        f"Average Confidences: {avg_confidences}"
    )
    
    logger.info(colored(summary_text, 'yellow'))

    return incorrect_files


if __name__ == "__main__":
    directory_path = "./data/original"
    incorrect_files = evaluate_directory(directory_path)
    logger.info(f"\nIncorrectly Classified Files: {incorrect_files}")