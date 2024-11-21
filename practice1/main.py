# app/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import cv2
import pywt
import numpy as np
from scipy.fft import dct, idct
from io import BytesIO
from PIL import Image
import subprocess
import io

app = FastAPI()

# Funciones seminar 1

# TASK 2
def rgb2yuv(r, g, b):
  y =  0.257 * r + 0.504 * g + 0.098 * b +  16
  u = -0.148 * r - 0.291 * g + 0.439 * b + 128
  v =  0.439 * r - 0.368 * g - 0.071 * b + 128
  return y, u, v

def yuv2rgb(y, u, v):
  b = 1.164 * (y - 16) + 2.018 * (u - 128)
  g = 1.164 * (y - 16) - 0.813 *(v -128) - 0.391 * (u - 128)
  r = 1.164 * (y - 16) + 1.596 * (v - 128)
  return r, g, b

# TASK 3
#def resize_and_reduce_quality(input_image, output_image, width, height, quality):
  ffmpeg_command = f'ffmpeg -i {input_image} -vf "scale={width}:{height}" -q:v {quality} {output_image}'
  subprocess.run(ffmpeg_command, shell=True, check=True)


def resize_and_reduce_quality(input_image, output_image, width, height, quality):
    ffmpeg_command = [
        "ffmpeg", 
        "-i", f"/app/content/{input_image}",
        "-vf", f"scale={width}:{height}",
        "-q:v", str(quality),
        f"/app/content/{output_image}"
    ]
    subprocess.run(ffmpeg_command, check=True)


def get_image_dimensions(image_path): # Just in case
  img = Image.open(image_path)
  width, height = img.size

  return width, height

# TASK 4
def serpentine(file_path):

  image = Image.open(file_path).convert("L")  # Converts to grayscale
  pixels = np.array(image)

  height, width = pixels.shape


  # Init output
  output = []
  i = 0
  j = 0

  output.append(pixels[i][j]) # Afegim el primer pixel
  i += 0
  j += 1
  output.append(pixels[i][j]) # Afegim el segon

  right = False
  left = True
  half = False

  # Primera meitat -------------------------------------------------
  while(j <= width - 1 and half == False):
    # Per a les baixades
    while(j - 1>= 0 and i + 1 <= height - 1 and right == False):
      j -= 1
      i += 1
      output.append(pixels[i][j])
      if((j - 1) < 0 and (i + 1) <= height - 1):
        j = 0
        i += 1
        output.append(pixels[i][j]) # Pas a baix
        right = True
        left = False

      elif((i + 1) > height - 1):  # Hemos llegado a una punta
        i = height - 1
        j += 1
        output.append(pixels[i][j]) # Pas a la dreta
        right = True
        left = False
        half = True

    # Per a les pujades
    while(j + 1 <= width - 1 and i - 1 >= 0 and left == False):
      j += 1
      i -= 1
      output.append(pixels[i][j])
      if(i - 1 < 0 and j + 1 <= width - 1):
        i = 0
        j += 1
        output.append(pixels[i][j]) # Pas a la dreta
        left = True
        right = False
      elif(j + 1 > width - 1):  # Hemos llegado a una punta
        j = width - 1
        i += 1
        output.append(pixels[i][j]) # Pas a baix
        left = True
        right = False
        half = True

  # Segona meitat -------------------------------------------------
  right =  False
  left = True
  while(j <= width - 1 and half == True):
    # Per a les baixades
    while(j - 1>= 0 and i + 1 <= height - 1 and right == False):
      j -= 1
      i += 1
      output.append(pixels[i][j])
      if((i + 1) > height - 1): # Prevision para el siguiente paso
        j +=1
        i = height - 1
        output.append(pixels[i][j]) # Pas a la dreta
        right = True
        left = False
        if(i == height - 1 and j == width - 1):
          half = False

    # Per a les pujades
    while(j + 1 <= width - 1 and i - 1 >= 0 and left == False):
      j += 1
      i -= 1
      output.append(pixels[i][j])
      if(j + 1 > width - 1):
        i += 1
        j = width -1
        output.append(pixels[i][j]) # Pas a la dreta
        left = True
        right = False
        if(i == height - 1 and j == width - 1):
          half = False

  return output

# TASK 5
#def compress2bw(input_image, output_image, quality=1):
  ffmpeg_command = f'ffmpeg -i {input_image} -vf "format=gray" -q:v {quality} {output_image}'
  subprocess.run(ffmpeg_command, shell=True, check=True)

def compress_to_bw(input_image, output_image, quality=1):
    ffmpeg_command = [
        "ffmpeg",
        "-i", f"/app/content/{input_image}",
        "-vf", "format=gray",  
        "-q:v", str(quality),
        f"/app/content/{output_image}"
    ]
    subprocess.run(ffmpeg_command, check=True)



# TASK 6
def run_length(data_stream):
  count = 0
  output = []
  for i in range(len(data_stream)):
    if(data_stream[i] == 0):
      count += 1
      if(i == len(data_stream) - 1):
        output.append(0)
        output.append(count)
    elif(data_stream[i] != 0 and data_stream[i - 1] == 0):
      output.append(0)
      output.append(count)
      output.append(data_stream[i])
      count = 0
    else:
      output.append(data_stream[i])

  return output

# TASK 7
# ENCODER CLASS ONLY
class dct_conversion:
  def alpha(pixel, N):
    if(pixel == 0):
      return np.sqrt(1/N)
    else:
      return np.sqrt(2/N)

  def dct_array(image_path):

    image = Image.open(image_path).convert("L")  # "L" mode converts to grayscale
    image = np.array(image)
    #image = cv2.imread(image_path, cv2.COLOR_BGR2GRAY)
    N, M = get_image_dimensions(image_path)
    dct_matrix = np.zeros((N, N))

    for u in range(N):
      for v in range(N):
        alpha_u = dct_conversion.alpha(u, N)
        alpha_v = dct_conversion.alpha(v, N)
        sum = 0.0
        for i in range(N):
          for j in range(N):
            gxy = image[i][j]
            sum += gxy*np.cos(np.pi/N*(i + 0.5)*u) * np.cos(np.pi/N*(j + 0.5)*v)
        dct_matrix[u][v] = alpha_u * alpha_v * sum

    return dct_matrix

  def dct2(a):
      return dct(dct(a.T, norm='ortho').T, norm='ortho')

  def idct2(a):
      return idct(idct(a.T, norm='ortho').T, norm='ortho')

# TAKS 8
class dwt_conversion:
  # Code
  def dwt(image_path):

      image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
      # Apply DWT
      coeficientes = pywt.dwt2(image, 'haar', mode = 'symmetric', axes =(-2,-1)) # Wavelet haar
      return coeficientes       #retorna: cH - horizontal detail, cV - vertical detail, cD - diagonal detail, cA - approximation

  # Decode
  def idwt(cA, cH, cV, cD):
    image = pywt.idwt2((cA, (cH, cV, cD)), 'haar', mode = 'symmetric', axes =(-2,-1))
    return image


# ENDPOINTS ------------------------------------------------------------------------

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

#TASK 2
@app.post("/convert-rgb2yuv")
async def convert_rgb2yuv(r: float, g: float, b: float):
    y, u, v = rgb2yuv(r, g, b)
    return {"y": y, "u": u, "v": v}

#TASK 2
@app.post("/convert-yuv2rgb")
async def convert_yuv2rgb(y: float, u: float, v: float):
    r, g, b = yuv2rgb(y, u, v)
    return {"r": r, "g": g, "b": b}

# TASK 3
@app.post("/resize")
async def resize(input_image: str, output_image: str, width: int, height: int, quality: int):
  resize_and_reduce_quality(input_image, output_image,
                                    width, height, quality)
