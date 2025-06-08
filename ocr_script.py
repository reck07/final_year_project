import pytesseract
from PIL import Image
import os

def extract_text_from_image(image_path):
    """
    Extract text from an image using OCR.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Extracted text from the image
    """
    try:
        # Open the image using PIL
        image = Image.open(image_path)
        
        # Extract text from the image
        text = pytesseract.image_to_string(image)
        
        return text.strip()
    except Exception as e:
        return f"Error processing image: {str(e)}"

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create an 'images' directory if it doesn't exist
    images_dir = os.path.join(current_dir, 'images')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"Created 'images' directory at: {images_dir}")
    
    # Get list of image files in the images directory
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    if not image_files:
        print("No image files found in the 'images' directory.")
        print("Please place your image files in the 'images' directory.")
        return
    
    # Process each image
    for image_file in image_files:
        image_path = os.path.join(images_dir, image_file)
        print(f"\nProcessing: {image_file}")
        print("-" * 50)
        
        # Extract text from the image
        extracted_text = extract_text_from_image(image_path)
        
        # Print the extracted text
        print("Extracted Text:")
        print(extracted_text)
        
        # Save the extracted text to a file
        output_file = os.path.join(current_dir, f"{os.path.splitext(image_file)[0]}_text.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        print(f"\nText saved to: {output_file}")

if __name__ == "__main__":
    main() 