import os
from PIL import Image
import struct

# Define the size of the thumbnail
thumb_size = (144, 208)

# Iterate through each .zfb file in the current directory
for zfb_filename in [f for f in os.listdir() if f.endswith('.zfb')]:
    # Open the .zfb file and read the raw image data
    with open(zfb_filename, 'rb') as zfb:
        raw_data_bytes = zfb.read(0xEA00)

        raw_data = []

        # Unpack the RGB565 raw data
        for i in range(0, len(raw_data_bytes), 2):
            rgb = struct.unpack('H', raw_data_bytes[i:i+2])[0]
            r = ((rgb >> 11) & 0x1F) << 3
            g = ((rgb >> 5) & 0x3F) << 2
            b = (rgb & 0x1F) << 3
            raw_data.append((r, g, b))

        img = Image.new('RGB', thumb_size)
        img.putdata(raw_data)

        # Create .png filename
        png_filename = zfb_filename.rsplit('.', 1)[0] + '.png'

        # Save the image as a .png file
        img.save(png_filename)

        print(f"Extracted {png_filename}")
