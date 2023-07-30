import glob
import os
import struct
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image


def exit_handler():
    os._exit(0)


# Main application class
class Application(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.master: tk.Tk = master
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
        self.filemenu.add_command(label="Rename ZFB files", command=self.rename_zfb_files)
        self.filemenu.add_command(label="Exit", command=exit_handler)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.master.config(menu=self.menubar)

    def donothing(self):
        pass

    def confirm_intention(self):
        """Ask for user's confirmation before modifying files"""
        msg = ("Files are about to be modified.\n"
               "Please ensure you have a backup of your files before proceeding.\n"
               "Do you want to continue?")
        return messagebox.askyesno("Confirmation", msg)

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
            # img.putdata(raw_data)  # Fix warning: Convert raw data to integer
            img.putdata([r * 65536 + g * 256 + b for (r, g, b) in raw_data])

            # Save the image as a .png file
            img.save(save_path)

    def extract_zfb_file(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[('ZFB Files', '*.zfb')])
            # Check if user cancelled the operation
            if not file_path:
                return

            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[('PNG Files', '*.png')])
            # Check if user cancelled the operation
            if not save_path:
                return

            # Attempt extraction
            self.extract_zfb_image(file_path, save_path)

            # If extraction is successful
            messagebox.showinfo('Success', 'ZFB file extracted.')
        except Exception as e:
            # Show an error message box with the exception message
            messagebox.showerror('Error', f'An error occurred while extracting the ZFB file: {str(e)}')

    def extract_entire_folder(self):
        """Extracts an entire folder of .ZFB files into .PNG files"""
        try:
            folder_path = filedialog.askdirectory()
            # Check if user cancelled the operation
            if not folder_path:
                return

            save_folder = filedialog.askdirectory()
            # Check if user cancelled the operation
            if not save_folder:
                return

            for file_name in os.listdir(folder_path):
                if file_name.lower().endswith('.zfb'):
                    file_path = os.path.join(folder_path, file_name)
                    png_filename = os.path.splitext(file_name)[0] + '.png'
                    save_path = os.path.join(save_folder, png_filename)
                    # Attempt extraction
                    self.extract_zfb_image(file_path, save_path)

            # If extraction is successful
            messagebox.showinfo('Success', 'ZFB files extracted.')
        except Exception as e:
            # Show an error message box with the exception message
            messagebox.showerror('Error', f'An error occurred while extracting the ZFB files: {str(e)}')

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
        try:
            png_filename = self.png_filename_var.get()
            rom_filename = self.rom_filename_var.get()

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
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred while creating the ZFB file: {str(e)}')

    def process_entire_folder(self):
        """Process an entire folder of .PNG and .ZIP files to create .ZFB files"""
        try:
            # Ask user for input folder
            input_folder = filedialog.askdirectory(title="Select input folder containing .PNG and .ZIP files")

            # Check if user cancelled the operation
            if not input_folder:
                return

            # Ask user for output folder
            output_folder = filedialog.askdirectory(title="Select output folder to save .ZFB files in")

            # Check if user cancelled the operation
            if not output_folder:
                return

            missing_rom_files = []
            processing_errors = []

            # Iterate over all .png files in the input folder
            for png_file in glob.glob(input_folder + '/*.png'):
                png_filename = os.path.basename(png_file)
                rom_filename = os.path.join(input_folder, png_filename.rsplit('.', 1)[0] + '.zip')

                # Skip if corresponding .zip file is not found
                if not os.path.exists(rom_filename):
                    missing_rom_files.append(png_filename)
                    continue

                try:
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
                except Exception as e:
                    processing_errors.append((png_filename, str(e)))

            if missing_rom_files:
                messagebox.showwarning('Warning',
                                       'Could not find corresponding ROM file for the following images:\n' + '\n'.join(
                                           missing_rom_files))
            if processing_errors:
                messagebox.showerror('Error', 'The following errors occurred during processing:\n' + '\n'.join(
                    [f'{filename}: {error}' for filename, error in processing_errors]))
            if not missing_rom_files and not processing_errors:
                messagebox.showinfo('Success', 'All files processed.')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred during processing: {str(e)}')

    def rename_zfb_files(self):
        # Ask user to select the folder containing .ZFB files
        zfb_folder = filedialog.askdirectory(title="Select the Folder Containing .ZFB Files")

        # If no folder was selected, return
        if not zfb_folder:
            return

        # Ask user to select the romnames.txt file
        romnames_file = filedialog.askopenfilename(title="Select the romnames.txt file",
                                                   filetypes=[("Text files", "*.txt")])

        # If no file was selected, return
        if not romnames_file:
            return

        # Confirm user's intention to modify files
        if self.confirm_intention():
            # Create a dictionary to map old names to new names
            name_map = {}

            # Open and read the romnames.txt file
            with open(romnames_file, 'r') as file:
                for line in file:
                    # Split each line into old name and new name
                    old_name, new_name = line.strip().split('=')
                    # Add to the name map
                    name_map[old_name] = new_name

            # Path for the error log file
            error_log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ERRORLOG-romnames.txt')

            # Counter for errors
            error_counter = 0

            # Error log file will be opened when first error occurs
            error_log = None

            # Iterate over all files in the selected directory
            for filename in os.listdir(zfb_folder):
                # If the file is a .ZFB file
                if filename.endswith('.zfb'):
                    # Remove the .zfb extension to get the old name
                    old_name = filename[:-4]
                    # If the old name is in the name map
                    if old_name in name_map:
                        # Get the new name
                        new_name = name_map[old_name]
                        # Create the full old and new file paths
                        old_file_path = os.path.join(zfb_folder, filename)
                        new_file_path = os.path.join(zfb_folder, new_name + '.zfb')
                        # Try to rename the file
                        try:
                            if len(old_name) < 8:  # If the old name is less than 8 characters long
                                # Workaround required to capitalize any name shorter than 8 chars
                                temp_file_path = os.path.join(zfb_folder, old_name + '_temp.zfb')
                                os.rename(old_file_path, temp_file_path)
                                os.rename(temp_file_path, new_file_path)
                            else:  # If the old name is 8 or more characters long, workaround not required
                                os.rename(old_file_path, new_file_path)
                        except Exception as e:
                            # Open the error log file in append mode when first error occurs
                            if error_log is None:
                                error_log = open(error_log_path, 'w')
                            # Write the error to the error log
                            error_log.write(f"Failed to rename {old_name}.zfb. Error: {str(e)}\n\n")
                            error_counter += 1

            # Close the error log file if it was opened
            if error_log is not None:
                error_log.close()

            # Notify the user of the result
            if error_counter == 0:
                messagebox.showinfo("Rename ZFB files", "All ZFB files were renamed successfully.")
            else:
                messagebox.showinfo("Rename ZFB files",
                                    f"Some ZFB files could not be renamed.\n"
                                    "Please see the error log (ERRORLOG-romnames.txt) for details.")
        else:
            messagebox.showinfo("Cancelled Operation", "The operation has been cancelled.")


# Define script paths
script_dir = os.path.dirname(os.path.realpath(__file__))
icon_path = os.path.join(script_dir, 'zfbtool.ico')

# Define the size of the thumbnail
thumb_size = (144, 208)

# Create the application window
root = tk.Tk()
root.geometry("630x160")
root.resizable(False, False)
root.title("ZFBTool for Data Frog SF2000")
if os.path.exists(icon_path):  # Check if the icon file exists
    root.iconbitmap(icon_path)


app = Application(master=root)

# Redefine the window's close button to trigger the custom exit handler
root.protocol("WM_DELETE_WINDOW", exit_handler)

# Start the application
app.mainloop()
