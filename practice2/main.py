# app/main.py
import json
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

    except Exception as e:
        print(f"An error occurred: {e}")


# TASK 2
async def encoding_ladder(input_video, codec):
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
            output_video = f"{input_video.split('.')[0]}_{profile['resolution']}_{codec}.mp4"
            
            # Build FFmpeg command for each profile
            ffmpeg_cmd = [
                "docker", "exec", "ffmpeg_container_s2",
                "ffmpeg", "-y",
                "-i", f"/app/content/{input_video}",
                "-vf", f"scale={profile['resolution']}",  # Scale to the desired resolution
                "-b:v", profile["bitrate"],  # Set the target bitrate
            ]
            
            # Append codec-specific arguments
            if codec == "vp8":
                ffmpeg_cmd += ["-c:v", "libvpx"]
            elif codec == "vp9":
                ffmpeg_cmd += ["-c:v", "libvpx-vp9"]
            elif codec == "h265":
                ffmpeg_cmd += ["-c:v", "libx265", "-preset", "medium", "-crf", "28"]
            elif codec == "av1":
                ffmpeg_cmd += ["-c:v", "libaom-av1", "-crf", "30", "-b:v", "0"]
            else:
                raise ValueError(f"Unsupported codec '{codec}'")

            # Output command
            ffmpeg_cmd += [f"/app/content/{output_video}"]
            
            # Schedule the process execution as a coroutine task
            tasks.append(asyncio.create_subprocess_exec(
                *ffmpeg_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ))

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Check for errors in each task
        for idx, process in enumerate(results):
            if isinstance(process, Exception):
                print(f"Error in profile {encoding_params[idx]}: {process}")
            else:
                stdout, stderr = await process.communicate()
                if process.returncode != 0:
                    print(f"Error in profile {encoding_params[idx]}: {stderr.decode()}")
                else:
                    print(f"Successfully encoded: {encoding_params[idx]['resolution']} at {encoding_params[idx]['bitrate']}")

    except Exception as e:
        print(f"An error occurred: {e}")


# ENDPOINTS ------------------------------------------

# TASK 1
@app.post("/convert")
async def convert(input_video: str, output_video: str, codec: str):
    await convert_video(input_video, output_video, codec)
    return {"message": f"Video {input_video} modified and saved as {output_video}"}

# TASK 2
@app.post("/encodingLadder")
async def encodingLeader(input_video: str, output_video: str):
    await encoding_ladder(input_video, output_video)
    return {"message": f"Video {input_video} modified and saved as {output_video}"}

