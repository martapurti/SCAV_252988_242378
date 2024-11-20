# -*- coding: utf-8 -*-
"""first_seminar2.py"""

import numpy as np
from PIL import Image
import os
import cv2
import pywt
from scipy.fft import dct, idct

# TASK 1
# !apt-get install ffmpeg

# TASK 2: RGB <-> YUV Conversion
# Using the functions that convert RGB -> YUV and viceversa. In the unit test we can see that the functions work correctly since the output of RGB is the same as c.
def rgb2yuv(r, g, b):
    y = 0.257 * r + 0.504 * g + 0.098 * b + 16
    u = -0.148 * r - 0.291 * g + 0.439 * b + 128
    v = 0.439 * r - 0.368 * g - 0.071 * b + 128
    return y, u, v

def yuv2rgb(y, u, v):
    b = 1.164 * (y - 16) + 2.018 * (u - 128)
    g = 1.164 * (y - 16) - 0.813 * (v - 128) - 0.391 * (u - 128)
    r = 1.164 * (y - 16) + 1.596 * (v - 128)
    return r, g, b

# TASK 3: Image Resize and Quality Reduction
#To change the size: {width} {height}. To change the quality: {quality}
def resize_and_reduce_quality(input_image, output_image, width, height, quality):
    ffmpeg_command = f'ffmpeg -i {input_image} -vf "scale={width}:{height}" -q:v {quality} {output_image}'
    os.system(ffmpeg_command)

def get_image_dimensions(image_path):
    img = Image.open(image_path)
    width, height = img.size
    return width, height

# TASK 4: Serpentine Reading of JPEG File
def serpentine(file_path):
    image = Image.open(file_path).convert("L") # "L" mode converts to grayscale
    pixels = np.array(image)
    height, width = pixels.shape
#--------------------------------------------------------------------------------------------------------------------
  # Init output
    output = []
    i = j = 0
    output.append(pixels[i][j]) # Afegim el primer pixel
    j += 1
    output.append(pixels[i][j]) # Afegim el segon
 
    right, left, half = False, True, False
# Primera meitat -------------------------------------------------------------------
    while j <= width - 1 and not half:
        while j - 1 >= 0 and i + 1 <= height - 1 and not right:
            j -= 1
            i += 1
            output.append(pixels[i][j])
            if (j - 1) < 0 and (i + 1) <= height - 1: # Prevision para el siguiente paso
                j = 0
                i += 1
                output.append(pixels[i][j])  # Pas a baix
                right, left = True, False
            elif (i + 1) > height - 1:
                i = height - 1
                j += 1
                output.append(pixels[i][j]) # Hemos llegado a una punta
                right, left, half = True, False, True
        # Per a les pujades
        while j + 1 <= width - 1 and i - 1 >= 0 and not left:
            j += 1
            i -= 1
            output.append(pixels[i][j]) # Pas a la dreta
            if i - 1 < 0 and j + 1 <= width - 1:
                i = 0
                j += 1
                output.append(pixels[i][j]) 
                left, right = True, False
            elif j + 1 > width - 1: # Hemos llegado a una punta
                j = width - 1
                i += 1
                output.append(pixels[i][j]) # Pas a baix
                left, right, half = True, False, True

# Segona meitat ---------------------------
    right, left = False, True
    while j <= width - 1 and half:
        while j - 1 >= 0 and i + 1 <= height - 1 and not right:
            j -= 1
            i += 1
            output.append(pixels[i][j])
            if (i + 1) > height - 1: # Prevision para el siguiente paso
                j += 1
                i = height - 1
                output.append(pixels[i][j]) # Pas a la dreta
                right, left = True, False
                if i == height - 1 and j == width - 1:
                    half = False
         # Per a les pujades
        while j + 1 <= width - 1 and i - 1 >= 0 and not left:
            j += 1
            i -= 1
            output.append(pixels[i][j])
            if j + 1 > width - 1:
                i += 1
                j = width - 1
                output.append(pixels[i][j]) # Pas a la dreta
                left, right = True, False
                if i == height - 1 and j == width - 1:
                    half = False
    return output

# TASK 5: Convert Image to Black & White with Compression
#Comments: The resulting image will be in Black and White, with the highest compression (quality = 1)
def compress2bw(input_image, output_image, width, height, quality):
    ffmpeg_command = f'ffmpeg -i {input_image} -vf "format=gray" -q:v {quality} {output_image}'
    os.system(ffmpeg_command)

# TASK 6: Run-Length Encoding
# We will create a function that if it finds a 0, it includes 0 + #zeros.
def run_length(data_stream):
    count, output = 0, []
    for i in range(len(data_stream)):
        if data_stream[i] == 0:
            count += 1
            if i == len(data_stream) - 1:
                output.append(0)
                output.append(count)
        elif data_stream[i] != 0 and data_stream[i - 1] == 0:
            output.append(0)
            output.append(count)
            output.append(data_stream[i])
            count = 0
        else:
            output.append(data_stream[i])
    return output

# TASK 7: DCT Class
# For this task we tried to create the DCT function by ourselves. Without using the imports.
class DCTConversion:
# MANUAL ONE
    @staticmethod
    def alpha(pixel, N):
        return np.sqrt(1/N) if pixel == 0 else np.sqrt(2/N)
    
    @staticmethod
    def dct_array(image_path):
        image = Image.open(image_path).convert("L")
        image = np.array(image)
        N, M = image.shape
        dct_matrix = np.zeros((N, M))
        for u in range(N):
            for v in range(M):
                alpha_u = DCTConversion.alpha(u, N)
                alpha_v = DCTConversion.alpha(v, M)
                sum_val = 0.0
                for i in range(N):
                    for j in range(M):
                        gxy = image[i][j]
                        sum_val += gxy * np.cos(np.pi / N * (i + 0.5) * u) * np.cos(np.pi / N * (j + 0.5) * v)
                dct_matrix[u][v] = alpha_u * alpha_v * sum_val
        return dct_matrix

#2D DCT, defined in: https://stackoverflow.com/questions/7110899/how-do-i-apply-a-dct-to-an-image-in-python
#IMPORTED ONES
    @staticmethod
    def dct2(a):
        return dct(dct(a.T, norm='ortho').T, norm='ortho')

    @staticmethod
    def idct2(a):
        return idct(idct(a.T, norm='ortho').T, norm='ortho')

# TASK 8: DWT Class
# To do the DWT, we will import pywt
class DWTConversion:
    @staticmethod
    def dwt(image_path):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        coeficientes = pywt.dwt2(image, 'haar', mode='symmetric', axes=(-2, -1))
        return coeficientes

    @staticmethod
    def idwt(cA, cH, cV, cD):
        return pywt.idwt2((cA, (cH, cV, cD)), 'haar', mode='symmetric', axes=(-2, -1))
