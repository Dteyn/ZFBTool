# Creates output.zfb using thumbnail.png. User specifies ROM .zip name
from PIL import Image
import struct

png_filename = 'thumbnail.png'
rom_filename = input("Which ROM is this for? (ex: kof.zip) ")
game_name = input("What is the name of the game? (ex: King of Fighters) ")

# Define the size of the thumbnail
thumb_size = (144, 208)

with Image.open(png_filename) as img:
    img = img.resize(thumb_size, Image.LANCZOS)
    img = img.convert("RGB")

    raw_data = []

    # Convert image to RGB565
    for y in range(thumb_size[1]):
        for x in range(thumb_size[0]):
            r, g, b = img.getpixel((x, y))
            rgb = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
            raw_data.append(struct.pack('H', rgb))

    raw_data_bytes = b''.join(raw_data)

    # Create .zfb filename
    zfb_filename = game_name + '.zfb'

    # Write the image data to the .zfb file
    with open(zfb_filename, 'wb') as zfb:
        zfb.write(raw_data_bytes)

        # Write four 00 bytes
        zfb.write(b'\x00\x00\x00\x00')

        # Write the ROM filename
        zfb.write(rom_filename.encode())

        # Write two 00 bytes
        zfb.write(b'\x00\x00')

print("Done. Move the ZFB file into the 'ARCADE' folder. Make sure zip is in 'ARCADE\\bin'")
print("Then run 'frogtool' to rebuild the game list")
