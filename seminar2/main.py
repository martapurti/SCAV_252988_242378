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
#Allows to modify the resolution (ffpeg)
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





# ENDPOINTS ------------------------------------------------------------------------

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

#TASK 1
@app.post("/modify_resolution")
async def reduce(input_video: str, output_video: str, width: int, height: int, quality:int):
    await modify_res(input_video, output_video, width, height, quality)
    return {"message": f"Video {input_video} modified and saved as {output_video}"}