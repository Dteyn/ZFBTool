# ZFBTool

ZFBTool is a utility specifically designed for the Data Frog SF2000 retro handheld. It provides a user-friendly way to create .zfb files by pairing custom thumbnail images with game ROMs. It includes features for single-file processing and bulk processing from a selected folder. ZFBTool is a great tool for enhancing the SF2000 user experience by personalizing your game library.

## Features

- Easily create .zfb files for your arcade ROMs
- Add custom thumbnail images for each ROM
- Single file and bulk processing capabilities

## Required Python Packages

- tkinter
- PIL

You can install these packages using pip:

```
pip install tkinter Pillow
```

## How to Use

1. Download the `ZFBTool.pyw` file provided in the repository.
2. Ensure you have Python and the necessary packages installed.
3. Run the `ZFBTool.pyw` file, and you will see the GUI.
4. In the GUI, you can either create a .zfb file from a single ROM or choose to compress an entire folder of ROMs.
    - For a single ROM, input your PNG file and the name of your ROM file. Then click "Create ZFB File".
    - For multiple ROMs, go to File > Compress Entire Folder, and select the folder containing your PNG and ROM files. You will then be prompted to select an output folder.
    - When compressing multiple ROMs, your .PNG and .ZIP filenames must be the same.
    - After .ZFB files are created, you can rename them to change the title of the ROMs in the Arcade menu
5. After building the .zfb files, they should be moved into the following folders:
   - ZFB files: `\ARCADE\`
   - ROM files: `\ARCADE\bin`
6. Run [frogtool](https://github.com/tzlion/frogtool) to rebuild the game list

Please note that the thumbnail images must be in PNG format.


## Advanced Users

Here are a few scripts for advanced users, or for implementing into your own scripts.

[create-thumbnail.py](https://github.com/Dteyn/ZFBTool/blob/master/src/create-thumbnail.py)

[extract-thumbnail.py](https://github.com/Dteyn/ZFBTool/blob/master/src/extract-thumbnail.py)

[extract-all-thumbnails.py](https://github.com/Dteyn/ZFBTool/blob/master/src/extract-all-thumbnails.py)


## .ZFB File Format

The `.zfb` files used by the Data Frog SF2000 are custom files that include a thumbnail image and references to a ROM file. Here's a brief overview of how these files are structured:

- The first 0xEA00 bytes: This portion is reserved for a thumbnail image in RGB565 RAW format with dimensions of 144x208px.

- The following bytes: This portion contains the actual filename of the ROM in the "bin" folder, preceded by four `00` bytes and followed by two further `00` bytes.

It's important to note that .zfb files for arcade games don't contain the actual game ROM, they only reference to it.


## Credits

Thank you to tzlion for the great work on [frogtool](https://github.com/tzlion/frogtool), and to the entire Data Frog SF2000 community. This script is only possible thanks to the information that tzlion posted here: https://github.com/tzlion/frogtool#technical-details

Thank you also to Von Millhausen for his excellent repository of information on the SF2000, which can be found here: https://github.com/vonmillhausen/sf2000

## Contact

If you encounter any issues or have suggestions for improvements, feel free to open an issue on this repository.
