# -*- coding: utf-8 -*-
"""test_first_seminar2.py"""

from io import BytesIO
import unittest
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import cv2
import pywt
from first_seminar2 import (
    rgb2yuv, yuv2rgb, resize_and_reduce_quality, get_image_dimensions,
    serpentine, compress2bw, run_length, DCTConversion, DWTConversion
)

class TestTask2(unittest.TestCase):
    def test_rgb2yuv_yuv2rgb_conversion(self):
        # Test values as per the user's request
        c = [0.2, 0.4, 0.6]
        # Perform RGB to YUV conversion
        (y, u, v) = rgb2yuv(c[0], c[1], c[2])
        print("(Y,U,V) =", y, u, v)
        # Perform YUV to RGB conversion
        (r, g, b) = yuv2rgb(y, u, v)
        print("(R,G,B) =", r, g, b)
        # Assert that the resulting RGB values are close to the original ones
        # Allow for minor floating-point precision errors
        self.assertAlmostEqual(r, c[0], places=2)
        self.assertAlmostEqual(g, c[1], places=2)
        self.assertAlmostEqual(b, c[2], places=2)
        
class TestTask3(unittest.TestCase):
    
    def test_resize_and_reduce_quality(self):
        # Input image path
        input_image = 'lab1\content\piplup.png'
        print("Input image dimensions: ", get_image_dimensions(input_image), "\n")

        # Output image path
        output_image = 'task3.png'  # Will have size 300x300, quality = 5 (we reduce the quality)
        new_width = 300  # size
        new_height = 300
        quality = 5  # quality

        # Resize and reduce quality
        resize_and_reduce_quality(input_image, output_image, new_width, new_height, quality)

        # Show the final image
        plt.title("Output Image of Task 3")
        plt.imshow(Image.open(output_image))
        plt.show()

        # Print the output image dimensions
        print("\nOutput image dimensions: ", get_image_dimensions(output_image))

class TestTask4(unittest.TestCase):
    def test_serpentine_with_in_memory_image(self):
        # Define a small 3x3 grayscale test image
        test_array = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ], dtype=np.uint8)

        # Expected output for serpentine traversal of this 3x3 array
        expected_output = [1, 2, 4, 7, 5, 3, 6, 8, 9]

        # Convert the array to an image and save it in an in-memory buffer
        test_image = Image.fromarray(test_array)
        image_buffer = BytesIO()
        test_image.save(image_buffer, format='PNG')
        image_buffer.seek(0)  # Restart buffer to beginning

        # Run the serpentine function using the in-memory buffer
        result = serpentine(image_buffer)

        # Assert that the result matches the expected output
        print("Result:", result)
        self.assertEqual(result, expected_output, "Serpentine traversal output does not match expected result")

class TestTask5(unittest.TestCase):
    def test_compress2bw(self):
        # Define input image path (adjust based on your test environment)
        input_image = 'lab1\content\piplup.png'

        # Get image dimensions
        w, h = get_image_dimensions(input_image)
        print(f"Input image dimensions: {w}x{h}")

        # Output image path (just for demonstration)
        output_image = 'gray_piplup.png'

        # Quality setting for compression
        quality = 1  # Low compression factor (lower means worse quality)

        # Compress to black and white (grayscale)
        compress2bw(input_image, output_image, w, h, quality)

        # Display the compressed grayscale image
        output_image = Image.open(output_image)  # Open the output image
        plt.imshow(output_image.convert("L"), cmap='gray')
        plt.title("Output Image of Task 5")
        plt.show()
        
class TestTask6(unittest.TestCase):
    def test_run_length(self):
        # Test input data stream
        data_stream = [0, 2, 3, 4, 0, 0, 0, 5, 6, 0, 0, 6, 0, 0, 0, 0, 0, 5, 0, 1, 0]
        
        # Expected output based on the RLE encoding of the input stream
        expected_output = [0, 1, 2, 3, 4, 0, 3, 5, 6, 0, 2, 6, 0, 5, 5, 0, 1, 1, 0, 1]
        
        # Run the function
        result = run_length(data_stream)
        
        # Print the result to check visually
        print("Run Length Encoding result:", result)
        
        # Assert that the result matches the expected output
        self.assertEqual(result, expected_output)
    
class TestTask7(unittest.TestCase):
    def test_dct_idct(self):
        # Load the input image as grayscale
        input_image = cv2.imread("lab1\content\piplup.png", cv2.IMREAD_GRAYSCALE)

        # Perform DCT on the input image
        dct_matrix = DCTConversion.dct2(input_image)

        # Perform IDCT to reconstruct the image
        idct_ = DCTConversion.idct2(dct_matrix)
        idct_image = Image.fromarray(np.clip(idct_, 0, 255).astype(np.uint8))
        
        # Plot the input and reconstructed image side by side
        plt.figure(figsize=(10, 5))

        # Plot original image
        plt.subplot(1, 2, 1)
        plt.imshow(input_image, cmap="gray")
        plt.title("Original Image")

        # Plot IDCT image
        plt.subplot(1, 2, 2)
        plt.imshow(idct_image, cmap="gray")
        plt.title("Reconstructed Image (IDCT)")
        
        plt.show()
        
class TestTask8(unittest.TestCase):
    def test_dwt_idwt(self):
        # Load the image in grayscale
        image_path = "lab1\content\color.jpg"
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        print("Original Image:")
        print(image)

        # Perform DWT on the image (wavelet transform)
        cA, (cH, cV, cD) = DWTConversion.dwt(image_path)

        print("\n\nDWT conversion:")
        print('cA (Approximation Coefficients):', cA)
        print('\ncH (Horizontal Detail Coefficients):', cH)
        print('\ncV (Vertical Detail Coefficients):', cV)
        print('\ncD (Diagonal Detail Coefficients):', cD)

        # Perform IDWT to reconstruct the image
        decoded_image = DWTConversion.idwt(cA, cH, cV, cD)

        print("\n\nDecoded Image (after IDWT):")
        print(decoded_image)

        # Plot the original image, the DWT coefficients, and the decoded image
        plt.figure(figsize=(15, 10))

        # Plot the original image
        plt.subplot(2, 3, 1)
        plt.imshow(image, cmap="gray")
        plt.title("Original Image")
        
        # Plot cA (Approximation Coefficients)
        plt.subplot(2, 3, 2)
        plt.imshow(cA, cmap="gray")
        plt.title("Approximation Coefficients (cA)")

        # Plot cH (Horizontal Coefficients)
        plt.subplot(2, 3, 3)
        plt.imshow(cH, cmap="gray")
        plt.title("Horizontal Coefficients (cH)")

        # Plot cV (Vertical Coefficients)
        plt.subplot(2, 3, 4)
        plt.imshow(cV, cmap="gray")
        plt.title("Vertical Coefficients (cV)")

        # Plot cD (Diagonal Coefficients)
        plt.subplot(2, 3, 5)
        plt.imshow(cD, cmap="gray")
        plt.title("Diagonal Coefficients (cD)")

        # Plot the reconstructed image
        plt.subplot(2, 3, 6)
        plt.imshow(decoded_image, cmap="gray")
        plt.title("Reconstructed Image (IDWT)")

        plt.show()

        
    
    
    
    
# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()
    
    