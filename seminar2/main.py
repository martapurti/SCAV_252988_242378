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

# New functions ---------------------------------------------------------------------

# TASK 1 

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

# TASK 2 
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
            "-c:v", "libx264",
            "-b:v", "2M", 
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", 
            f"/app/content/{output_video}"
        ]

        # Run the ffmpeg command
        subprocess.run(ffmpeg_cmd, check=True)

        print(f"Output video saved as {output_video}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

#----------------------------------------------------------------------------

# TASK 3 
#Create a new endpoint/feature which lets you read the video info and print at least 5 relevant data from the video
def info_video(input_video):
    try:
        # Construir el comando ffprobe para obtener información del video
        cmd = [
            "docker", "exec", "ffmpeg_container_s2",
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,duration,bit_rate,codec_name,chroma_location",
            "-of", "json",
            f"/app/content/{input_video}"
        ]

        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)

        video_info = json.loads(result)

        print("Information:")
        print(f"Width: {video_info['streams'][0]['width']} pixels")
        print(f"Height: {video_info['streams'][0]['height']} pixels")
        print(f"Duration: {video_info['streams'][0]['duration']} seconds")
        print(f"Bit Rate: {video_info['streams'][0]['bit_rate']} bps")
        print(f"Codec: {video_info['streams'][0]['codec_name']}")
        print(f"Chroma Location: {video_info['streams'][0]['chroma_location']}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

#----------------------------------------------------------------------------

# TASK 4 
#Cut BBB into 20 seconds only video
#Export BBB(20s) audio as AAC mono track
#Export BBB(20s) audio in MP3 stereo w/ lower bitrate
#Export BBB(20s) audio in AC3 codec
# TASK 4
async def new_container(input_video, output_video):
    try:
        ffmpeg_cmd = [
            "docker", "exec", "ffmpeg_container_s2",
            "ffmpeg", "-y",
            "-i", f"/app/content/{input_video}",
            "-t", "20",
            "-c:v", "copy",
            "-map", "0:v:0", "-map", "0:a:0", "-c:a:0", "aac", "-ac", "1", "-b:a:0", "128k", # ACC
            "-map", "0:a:0", "-c:a:1", "libmp3lame", "-b:a:1", "96k", "-ac:1", "2", # MP3
            "-map", "0:a:0", "-c:a:2", "ac3", "-b:a:2", "192k", # AC3
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

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

#----------------------------------------------------------------------------

# TASK 5 
#use ffprobe: a tool that comes with ffmpeg to inspect the media file structure
async def count_tracks(input_video):
    try:
        ffmpeg_cmd = [ "docker", "exec", "ffmpeg_container_s2",
                "ffprobe", "-v", "error",
                "-show_entries", "stream=index,codec_type",
                "-of", "json",
                f"/app/content/{input_video}"]

        process = await asyncio.create_subprocess_exec(
                *ffmpeg_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
        stdout, stderr = await process.communicate()
            
        if process.returncode != 0:
            raise Exception(f"FFprobe error: {stderr.decode()}")
            
        # Parse the FFprobe output
        metadata = json.loads(stdout.decode())
        streams = metadata.get("streams", [])
            
        # Count track types
        track_counts = {"video": 0, "audio": 0, "subtitle": 0}
        for stream in streams:
            codec_type = stream.get("codec_type")
            if codec_type in track_counts:
                track_counts[codec_type] += 1
            
        print(track_counts)

    except Exception as e:
        print(f"An error occurred: {e}")
    

#----------------------------------------------------------------------------


# TASK 6 
# Creat a new endpoint / feature which will output a video that will show the motion vectors
# Los macroblockes no se pueden hacer con ffmpeg
async def motion_vectors(input_video, output_video):
    try:
        ffmpeg_cmd = [
            "docker", "exec", "ffmpeg_container_s2",
            "ffmpeg", "-y",
            "-i", f"/app/content/{input_video}",
            "-vf", "codecview=mv=1",   # Filtro para mostrar motion vectors
            "-c:v", "libx264",  # Codec de salida H.264
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

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

#----------------------------------------------------------------------------   

# TASK 7 
# Create a new endpoint / feature which will output a video that will show the YUV histogram
async def yuv_histogram(input_video, output_video):
    try:
        ffmpeg_cmd = [
            "docker", "exec", "ffmpeg_container_s2",
            "ffmpeg", "-y",
            "-i", f"/app/content/{input_video}",
            "-vf", "split[main][hist];[hist]histogram,[main]overlay", # YUV histograma
            "-c:v", "libx264",
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

#TASK 2
@app.post("/chromass")
async def chromass(input_video:str, output_video:str, subsampling_3ratio:int):
    chroma_subsampling(input_video, output_video, subsampling_3ratio)
    return {"message": f"Video {input_video} modified and saved as {output_video}"}

#TASK 3
@app.post("/video_infomation")
def information(input_video:str):
    info_video(input_video)

# TASK 4
@app.post("/container")
async def container(input_video: str, output_video: str):
    await new_container(input_video, output_video)
    return {"message": f"Video {input_video} modified and saved as {output_video}"}

# TASK 5
@app.post("/count_tracks")
async def countt(input_video:str):
    await count_tracks(input_video)
    

# TASK 6
@app.post("/mvectors")
async def mvectors(input_video: str, output_video: str):
    await motion_vectors(input_video, output_video)
    return {"message": f"Video {input_video} modified and saved as {output_video}"}

# TASK 7
@app.post("/histogram")
async def histogram(input_video: str, output_video: str):
    await yuv_histogram(input_video, output_video)
    return {"message": f"Video {input_video} modified and saved as {output_video}"}