import os
from main import convert_video, encoding_ladder
import unittest

class Test1(unittest.TestCase):
    def test_convert_video(self):
        # Parameters
        input_image = "BBB.mp4"
        output_image = "test1.mp4" 
        codec = 'h256'
        resolution = '240p'

        convert_video(input_image, output_image, codec, resolution)

class Test2(unittest.TestCase): 
    def test_encoding_ladder(self):
        # Parameters
        input_image = "BBB.mp4"
        output_image = "test3" 
        codec = 'VP8'

        encoding_ladder(input_image, output_image, codec)



# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()

