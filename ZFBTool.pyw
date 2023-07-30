import glob
import os
import struct
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

global thumb_size


def exit_handler():
    os._exit(0)


# Main application class
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(anchor="w")
        self.create_widgets()

        # Create frame for header
        self.header_frame = tk.Frame(self.master)
        self.header_frame.pack(anchor="w")

        # Create frame for PNG File selection
        self.frame = tk.Frame(self.master)
        self.frame.pack(anchor="w")

        # Create bold font for label
        bold_font = ("Helvetica", 10, "bold")
        label_font = ("Helvetica", 10, "normal")

        instructions_text = "Select thumbnail PNG file, ROM file, and ZFB output filename"

        # Instructions
        self.header_label = tk.Label(self.header_frame, text=instructions_text, font=bold_font)
        self.header_label.pack()

        # PNG File - Label
        self.png_filename_label = tk.Label(self.frame, text="Thumbnail PNG file: ", font=label_font)
        self.png_filename_label.grid(row=1, column=0, sticky="w")

        # PNG File - Input box
        self.png_filename_var = tk.StringVar()
        self.png_filename_entry = tk.Entry(self.frame, textvariable=self.png_filename_var, width=70)
        self.png_filename_entry.grid(row=1, column=1, sticky="w")

        # PNG File - Browse button
        self.png_filename_button = tk.Button(self.frame, text="Browse", command=self.select_png_file)
        self.png_filename_button.grid(row=1, column=2, sticky="w")

        # ROM File - Label
        self.rom_filename_label = tk.Label(self.frame, text="ARCADE ROM .ZIP file: ", font=label_font)
        self.rom_filename_label.grid(row=2, column=0, sticky="w")

        # ROM File - Input box
        self.rom_filename_var = tk.StringVar()
        self.rom_filename_entry = tk.Entry(self.frame, textvariable=self.rom_filename_var, width=70)
        self.rom_filename_entry.grid(row=2, column=1, sticky="w")

        # ROM File - Browse button
        self.rom_filename_button = tk.Button(self.frame, text="Browse", command=self.select_rom_file)
        self.rom_filename_button.grid(row=2, column=2, sticky="w")

        # ZFB File - Label
        self.zfb_filename_label = tk.Label(self.frame, text="ZFB Filename to save as: ", font=label_font)
        self.zfb_filename_label.grid(row=3, column=0, sticky="w")

        # ZFB File - Input box
        self.zfb_filename_var = tk.StringVar()
        self.zfb_filename_entry = tk.Entry(self.frame, textvariable=self.zfb_filename_var, width=70)
        self.zfb_filename_entry.grid(row=3, column=1, sticky="w")

        # ZFB File - Browse button
        self.zfb_filename_button = tk.Button(self.frame, text="Browse", command=self.select_zfb_file)
        self.zfb_filename_button.grid(row=3, column=2, sticky="w")

        # Create ZFB File button
        self.create_zfb_button = tk.Button(self.frame, text="Create ZFB File", command=self.create_zfb_file,
                                           font=("Helvetica", 14))
        self.create_zfb_button.grid(row=4, column=0, sticky="w", columnspan=3)

    def create_widgets(self):
        self.menubar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Extract thumbnail from ZFB", command=self.extract_zfb_file)
        self.filemenu.add_command(label="Extract entire folder", command=self.extract_entire_folder)
        self.filemenu.add_command(label="Create ZFB in bulk", command=self.process_entire_folder)
        self.filemenu.add_command(label="Exit", command=exit_handler)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.master.config(menu=self.menubar)

        # Code for input boxes and browse buttons goes here

    def donothing(self):
        pass

    def about(self):
        messagebox.showinfo("About", "ZFB Creator and Extractor Tool by Dteyn\nhttps://github.com/Dteyn/ZFBTool")

    def open_png_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('PNG Files', '*.png')])
        # Add code here to display the selected PNG file in the application window

    def save_zfb_file(self):
        file_path = filedialog.asksaveasfilename(filetypes=[('ZFB Files', '*.zfb')])
        # Add code here to save the output ZFB file to the selected location

    def extract_zfb_image(self, file_path, save_path):
        """Extracts an image from a ZFB file"""
        if file_path and save_path:
            # Open the .zfb file and read the raw image data
            with open(file_path, 'rb') as zfb:
                raw_data_bytes = zfb.read(0xEA00)

            raw_data = []

            # Unpack the RGB565 raw data
            for i in range(0, len(raw_data_bytes), 2):
                rgb = struct.unpack('H', raw_data_bytes[i:i + 2])[0]
                r = ((rgb >> 11) & 0x1F) << 3
                g = ((rgb >> 5) & 0x3F) << 2
                b = (rgb & 0x1F) << 3
                raw_data.append((r, g, b))

            img = Image.new('RGB', thumb_size)
            img.putdata(raw_data)

            # Save the image as a .png file
            img.save(save_path)

    def extract_zfb_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('ZFB Files', '*.zfb')])
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[('PNG Files', '*.png')])
        self.extract_zfb_image(file_path, save_path)
        messagebox.showinfo('Success', 'ZFB file extracted.')

    def extract_entire_folder(self):
        """Extracts an entire folder of .ZFB files into .PNG files"""
        folder_path = filedialog.askdirectory()
        save_folder = filedialog.askdirectory()

        if folder_path and save_folder:
            for file_name in os.listdir(folder_path):
                if file_name.lower().endswith('.zfb'):
                    file_path = os.path.join(folder_path, file_name)
                    png_filename = os.path.splitext(file_name)[0] + '.png'
                    save_path = os.path.join(save_folder, png_filename)
                    self.extract_zfb_image(file_path, save_path)

            messagebox.showinfo('Success', 'ZFB files extracted.')

    def select_png_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('PNG Files', '*.png')])
        if file_path:
            self.png_filename_var.set(file_path)

    def select_zfb_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".zfb", filetypes=[('ZFB Files', '*.zfb')])
        if file_path:
            self.zfb_filename_var.set(file_path)

    def select_rom_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".zip", filetypes=[('ARCADE ROM Files', '*.zip')])
        if file_path:
            self.rom_filename_var.set(file_path)

    def create_zfb_file(self):
        """Creates a .ZFB file with input .PNG file and ARCADE ROM .ZIP name"""
        png_filename = self.png_filename_var.get()
        rom_filename = self.rom_filename_var.get()

        thumb_size = (144, 208)  # Define thumbnail size

        with Image.open(png_filename) as img:
            img = img.resize(thumb_size)
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
            zfb_filename = self.zfb_filename_var.get()

            # Write the image data to the .zfb file
            with open(zfb_filename, 'wb') as zfb:
                zfb.write(raw_data_bytes)

                # Write four 00 bytes
                zfb.write(b'\x00\x00\x00\x00')

                # Write the ROM filename
                zfb.write(rom_filename.encode())

                # Write two 00 bytes
                zfb.write(b'\x00\x00')

        messagebox.showinfo('Success', 'ZFB file created successfully.')

    def process_entire_folder(self):
        """Process an entire folder of .PNG and .ZIP files to create .ZFB files"""

        # Ask user for input folder
        input_folder = filedialog.askdirectory(title="Select input folder containing .PNG and .ZIP files")

        # Ask user for output folder
        output_folder = filedialog.askdirectory(title="Select output folder to save .ZFB files in")

        thumb_size = (144, 208)  # Define thumbnail size

        # Iterate over all .png files in the input folder
        for png_file in glob.glob(input_folder + '/*.png'):
            png_filename = os.path.basename(png_file)
            rom_filename = os.path.join(input_folder, png_filename.rsplit('.', 1)[0] + '.zip')

            # Skip if corresponding .zip file is not found
            if not os.path.exists(rom_filename):
                print('Could not find corresponding ROM file for:', png_filename)
                continue

            # Process the .png file and create the .zfb file
            with Image.open(png_file) as img:
                img = img.resize(thumb_size)
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
                zfb_filename = os.path.join(output_folder, png_filename.rsplit('.', 1)[0] + '.zfb')

                # Write the image data to the .zfb file
                with open(zfb_filename, 'wb') as zfb:
                    zfb.write(raw_data_bytes)

                    # Write four 00 bytes
                    zfb.write(b'\x00\x00\x00\x00')

                    # Write the ROM filename
                    rom_file = os.path.basename(rom_filename)
                    zfb.write(rom_file.encode())

                    # Write two 00 bytes
                    zfb.write(b'\x00\x00')

        messagebox.showinfo('Success', 'All files processed.')


# Define the size of the thumbnail
thumb_size = (144, 208)

# Create the application window
root = tk.Tk()
root.geometry("630x160")
root.resizable(0, 0)
root.title("ZFBTool for Data Frog SF2000")
root.iconbitmap('zfbtool.ico')


app = Application(master=root)

# Redefine the window's close button to trigger the custom exit handler
root.protocol("WM_DELETE_WINDOW", exit_handler)

# Start the application
app.mainloop()
