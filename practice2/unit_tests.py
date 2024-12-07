import os
import unittest
import asyncio
from main import convert_video, encoding_ladder

class Test1(unittest.TestCase):
    def test_convert_video(self):
        # Parameters
        input_image = "BBB.mp4"  
        output_image = "test1.mp4"
        codec = 'h265'
        resolution = '240p'

        # Ejecutar 
        asyncio.run(convert_video(input_image, output_image, codec, resolution))


class Test2(unittest.TestCase): 
    def test_encoding_ladder(self):
        # Parameters
        input_image = "BBB.mp4" 
        output_image = "test2"
        codec = 'VP8'

        # Ejecutar
        asyncio.run(encoding_ladder(input_image, output_image, codec))


# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()
