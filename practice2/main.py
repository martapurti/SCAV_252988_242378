
# app/main.py
import json
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from pydantic import BaseModel
import numpy as np
from scipy.fft import dct, idct
import asyncio
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import shutil
import subprocess

app = FastAPI()

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.).
    allow_headers=["*"],  # Permite todos los encabezados.
)

# FUNCTIONS PRACTICE 2 ----------------------------------------------------
#TASK 1
# Convert a video to a specific codec and resolution
async def convert_video(input_video, output_video_name, codec, new_resolution):
    codecs_disponible = {
        "VP8": "libvpx",
        "VP9": "libvpx-vp9",
        "h265": "libx265",
        "AV1": "libaom-av1"
    }
    
    encoding_params = {
        "240p": {"resolution": "426x240", "bitrate": "300k"},
        "360p": {"resolution": "640x360", "bitrate": "800k"},
        "720p": {"resolution": "1280x720", "bitrate": "2M"},
        "1080p": {"resolution": "1920x1080", "bitrate": "4M"}
    }

    try:
        # Validate codec
        if codec not in codecs_disponible:
            raise ValueError(f"Unsupported codec '{codec}'. Choose from {list(codecs_disponible.keys())}")
        
        # Validate resolution
        if new_resolution not in encoding_params:
            raise ValueError(f"Unsupported resolution '{new_resolution}'. Choose from {list(encoding_params.keys())}")
        
        
        # Determine container format based on codec
        container = "webm" if codec in ["VP8", "VP9"] else "mp4"
        if not output_video_name.endswith(f".{container}"):
            output_video_name += f".{container}"
        
        # Resolve resolution and bitrate
        resolution = encoding_params[new_resolution]["resolution"]
        bitrate = encoding_params[new_resolution]["bitrate"]

        # Save the uploaded video to a local path temporarily
        input_video_path = f"/tmp/{input_video.filename}"  # Save to a temporary directory
        with open(input_video_path, "wb") as f:
            shutil.copyfileobj(input_video.file, f)
        
        # Adjust audio codec for WebM
        audio_codec = "libopus" if container == "webm" else "copy"
        
        # Construct FFmpeg command
        ffmpeg_cmd = [
            "docker", "exec", "ffmpeg_container_s2",
            "ffmpeg", "-y",
            "-i", f"/app/content/{input_video.filename}",
            "-vf", f"scale={resolution}",
            "-b:v", bitrate,
            "-c:v", codecs_disponible[codec],
            "-c:a", audio_codec,  # Transcode audio for WebM
            f"/app/content/{output_video_name}",
        ]
        
        # Execute the FFmpeg command asynchronously
        process = await asyncio.create_subprocess_exec(
            *ffmpeg_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        # Check for errors in FFmpeg execution
        if process.returncode != 0:
            raise Exception(f"Error in FFmpeg: {stderr.decode()}")
        
        print(f"Output video saved as: {output_video_name}")
        return output_video_name

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        raise HTTPException(status_code=500, detail=f"FFmpeg error: {e.stderr.decode()}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Video conversion failed: {e}")

# TASK 2
# Function to process multiple resolutions (encoding ladder)
async def encoding_ladder(input_video, output_video_base, codec):
    resolutions = ["240p", "360p", "720p", "1080p"]
    tasks = []

    # Create tasks for each resolution using the convert_video function
    for resolution in resolutions:
        output_video_name = f"{output_video_base}_{resolution}_{codec}.mp4"
        tasks.append(convert_video(input_video, output_video_name, codec, resolution))

    # Execute all tasks concurrently
    results = await asyncio.gather(*tasks)

    # Return results with all output video names
    return {"message": "Encoding ladder created successfully.", "output_videos": results}

# ENDPOINTS ------------------------------------------

# app.mount("/content", StaticFiles(directory="content"), name="content")
# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     with open("index_marta.html", "r") as f:
#         return f.read()

# TASK 1
@app.post("/convert")
async def convert(input_video: UploadFile = File(...), output_video_name: str = Form(...), codec: str = Form(...), new_resolution: str = Form(...)):
        await convert_video(input_video, output_video_name, codec, new_resolution)
        return {"message": f"Video {input_video} modified and saved as {output_video_name}"}
     
# TASK 2
@app.post("/encodingLadder")
async def encodingLadder(input_video: UploadFile = File(...), output_video_base: str = Form(...), codec: str = Form(...)):
        await encoding_ladder(input_video, output_video_base, codec)
        return {"message": f"Video {input_video} modified and saved"}

