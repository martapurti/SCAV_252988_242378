# app/main.py
import json
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
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
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse




app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.).
    allow_headers=["*"],  # Permite todos los encabezados.
)


# FUNCTIONS PRACTICE 2 ----------------------------------------------------

# TASK 1
# codec = {vp8, vp9, h265, av1}
async def convert_video(input_video, output_video, codec):
    try:
        # Define codec-specific FFmpeg parameters
        codec_params = {
            "vp8": ["-c:v", "libvpx", "-b:v", "1M"],
            "vp9": ["-c:v", "libvpx-vp9", "-b:v", "1M"],
            "h265": ["-c:v", "libx265", "-preset", "medium", "-crf", "28"],
            "av1": ["-c:v", "libaom-av1", "-crf", "30", "-b:v", "0"]
        }

        if codec not in codec_params:
            raise ValueError(f"Unsupported codec '{codec}'. Supported codecs are: {list(codec_params.keys())}")
        
        # Adjust output container for VP8 and VP9
        if codec in ["vp8", "vp9"]:
            if not output_video.endswith(".webm"):
                output_video = f"{output_video.split('.')[0]}.webm"
        else:
            if not output_video.endswith(".mp4"):
                output_video = f"{output_video.split('.')[0]}.mp4"


        ffmpeg_cmd = [
            "docker", "exec", "ffmpeg_container_s2",
            "ffmpeg", "-y",
            "-i", f"/app/content/{input_video}",
            *codec_params[codec],
            f"/app/content/{output_video}"
        ]


        process = await asyncio.create_subprocess_exec(
            *ffmpeg_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(f"Error in ffmpeg: {stderr.decode()}")

        print(f"Output video saved as {output_video}")
        return output_video
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Video conversion failed: {e}")

# TASK 2
async def encoding_ladder(input_video, output_video, codec):
    try:
        # Define resolutions and corresponding bitrates for the encoding ladder
        encoding_params = [
            {"resolution": "426x240", "bitrate": "300k"},
            {"resolution": "640x360", "bitrate": "800k"},
            {"resolution": "1280x720", "bitrate": "2M"},
            {"resolution": "1920x1080", "bitrate": "4M"}
        ]
        
        # List to store asyncio tasks
        tasks = []
        
        for profile in encoding_params:
            output_video2 = f"{output_video.split('.')[0]}_{profile['resolution']}_{codec}.mp4"
            
            # Call convert_video for each profile
            tasks.append(convert_video(
                input_video,
                output_video2,
                codec
            ))

        # Execute all tasks in parallel
        await asyncio.gather(*tasks)

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

    except Exception as e:
        print(f"An error occurred: {e}")


# ENDPOINTS ------------------------------------------

# app.mount("/content", StaticFiles(directory="content"), name="content")
# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     with open("index_marta.html", "r") as f:
#         return f.read()

# TASK 1
@app.post("/convert")
async def convert(input_video: UploadFile = File(...), output_video: str = Form(...), codec: str = Form(...)):
    input_video_filename = input_video.filename
    codec_type = codec
    await convert_video(input_video_filename, output_video, codec_type)
    return {"message": f"Video {input_video} modified and saved as {output_video}"}

# TASK 2
@app.post("/encodingLadder")
async def encodingLadder(input_video: UploadFile = File(...), output_video: str = Form(...), codec: str = Form(...)):
    input_video_filename = input_video.filename
    await encoding_ladder(input_video_filename, output_video, codec)
    return {"message": f"Video {input_video} modified and saved as {output_video}"}

