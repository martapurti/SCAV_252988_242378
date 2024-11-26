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
import asyncio



app = FastAPI()

# New functions

#TASK 1---------------------------------------------------------------------

#Create a new endpoint / feature which will let you to modify the resolution
async def modify_res(input_video, output_video, width, height, quality):
    try:
        ffmpeg_command = [
            "docker", "exec", "ffmpeg_container_s2",
            "ffmpeg", "-y",
            "-i", f"/app/content/{input_video}",  
            "-vf", f"scale={width}:{height}", 
            "-q:v", str(quality),
            f"/app/content/{output_video}"
        ]
        process = await asyncio.create_subprocess_exec(
            *ffmpeg_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
         
        if process.returncode != 0:
            raise Exception(f"Error in ffmpeg: {stderr.decode()}")
        print(f"Video saved as {output_video}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
#-----------------------------------------------------------------------------

#TASK 2---------------------------------------------------------------------
#2) Create a new endpoint / feature which will let you to modify the chroma subsampling
#Practice of encoding images by implementing less resolution for Chroma / Luma
#Subsampling a:x:y (chroma resolution) / ax2 block of luma pixels
#a: horizontal sampling reference (4)
#x: num of chroma samples 1st row of pixels
#y: num of changes of chroma samples bw 1st and 2nd rows of a pixel

def chroma_subsampling(input_video, output_video, subsampling_3ratio):
# - subsampling_3ratio has to be without : (ex: 422)
    try:
        ffmpeg_cmd = [
            "docker", "exec", "ffmpeg_container_s2",
            "ffmpeg", "-y",
            "-i", f"/app/content/{input_video}",  
            "-vf", f"format=yuv{subsampling_3ratio}p", #Chroma subsampling ratio = 4:2:2
            "-c:v", "libx264",  #Video codec
            "-b:v", "2M",  #Video bitrate
            "-c:a", "aac",  #Audio codec
            f"/app/content/{output_video}"
        ]

        # Run the ffmpeg command
        subprocess.run(ffmpeg_cmd, check=True)

        print(f"Output video saved as {output_video}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")




# ENDPOINTS ------------------------------------------------------------------------

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

#TASK 1
@app.post("/modify_resolution")
async def reduce(input_video: str, output_video: str, width: int, height: int, quality:int):
    await modify_res(input_video, output_video, width, height, quality)
    return {"message": f"Video {input_video} modified and saved as {output_video}"}

@app.post("/chromass")
def chromass(input_video:str, output_video:str, subsampling_3ratio:int):
    chroma_subsampling(input_video, output_video, subsampling_3ratio)
    return {"message": f"Video {input_video} modified and saved as {output_video}"}