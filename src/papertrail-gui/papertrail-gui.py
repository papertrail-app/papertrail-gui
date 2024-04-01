import tkinter as tk
from tkinter import ttk
import sv_ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import sys
from papertrail.papertraildriver import PaperTrailDriver

class PaperTrailGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PaperTrail")

        # Initialize Vars
        self.filepath_encryption = ""
        self.filepath_decryption = ""

        # Add and Bind Widgets
        self.__add_widgets()
        self.__bind_theme()

        # Initialize PaperTrailDriver
        self.driver = PaperTrailDriver()


    def __add_widgets(self):
        
        ### GRID CONFIGURATION
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        ### ENCRYPT SIDE ###
        
        self.encrypt_frame = ttk.LabelFrame(self.root, text="Encrypt", padding=(20, 20))
        self.encrypt_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.encrypt_sel_label = ttk.Label(self.encrypt_frame, text="Select a file to encrypt:")
        self.encrypt_sel_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.select_file_button_encryption = ttk.Button(self.encrypt_frame, text="Select File", command=self.__select_file_encryption)
        self.select_file_button_encryption.grid(row=2, column=0, padx=5, pady=5, sticky='w')

        self.spacer03 = ttk.Label(self.encrypt_frame, text="")
        self.spacer03.grid(row=3, column=0, padx=0, pady=0, sticky='w')
        
        self.encrypt_pass_label = ttk.Label(self.encrypt_frame, text="Encryption Password (12 characters minimum):")
        self.encrypt_pass_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.password_entry_encryption = ttk.Entry(self.encrypt_frame, show="*")
        self.password_entry_encryption.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

        self.spacer06 = ttk.Label(self.encrypt_frame, text="")
        self.spacer06.grid(row=6, column=0, padx=0, pady=0, sticky='w')
        
        self.encrypt_button = ttk.Button(self.encrypt_frame, text="Encrypt", style="Accent.TButton", command=self.__submit_encrypt)
        self.encrypt_button.grid(row=7, column=0, padx=5, pady=5, sticky='w')

        ### DECRYPT SIDE ###

        self.decrypt_frame = ttk.LabelFrame(self.root, text="Decrypt", padding=(20, 20))
        self.decrypt_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.decrypt_sel_label = ttk.Label(self.decrypt_frame, text="Select a scan to decrypt:")
        self.decrypt_sel_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.select_file_button_decryption = ttk.Button(self.decrypt_frame, text="Select File", command=self.__select_file_decryption)
        self.select_file_button_decryption.grid(row=2, column=0, padx=5, pady=5, sticky='w')

        self.spacer13 = ttk.Label(self.decrypt_frame, text="")
        self.spacer13.grid(row=3, column=1, padx=0, pady=0, sticky='w')

        self.decrypt_pass_label = ttk.Label(self.decrypt_frame, text="Decryption Password (12 characters minimum):")
        self.decrypt_pass_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.password_entry_decryption = ttk.Entry(self.decrypt_frame, show="*")
        self.password_entry_decryption.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

        self.spacer16 = ttk.Label(self.decrypt_frame, text="")
        self.spacer16.grid(row=6, column=1, padx=0, pady=0, sticky='w')

        self.decrypt_button = ttk.Button(self.decrypt_frame, text="Decrypt", style="Accent.TButton", command=self.__submit_decrypt)
        self.decrypt_button.grid(row=7, column=0, padx=5, pady=5, sticky='w')

        
    def __select_file_encryption(self):
        self.filepath_encryption = filedialog.askopenfilename(initialdir=os.path.expanduser( '~' ), title="Select Data File to Encrypt")


    def __select_file_decryption(self):
        self.filepath_decryption = filedialog.askopenfilename(initialdir=os.path.expanduser( '~' ), title="Select PaperTrail Document to Decrypt", filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))


    def __validate_pass_encryption(self, *_):
        if len(self.password_entry_encryption.get()) < 12:
            self.password_entry_encryption.state(["invalid"])
        else:
            self.password_entry_encryption.state(["!invalid"])        

        
    def __validate_pass_decryption(self, *_):
        if len(self.password_entry_decryption.get()) < 12:
            self.password_entry_decryption.state(["invalid"])
        else:
            self.password_entry_decryption.state(["!invalid"]) 


    def __bind_theme(self):
        self.password_entry_encryption.bind("<FocusOut>", self.__validate_pass_encryption)
        self.password_entry_encryption.bind("<FocusIn>", self.__validate_pass_encryption)
        self.password_entry_encryption.bind("<KeyRelease>", self.__validate_pass_encryption)

        self.password_entry_decryption.bind("<FocusOut>", self.__validate_pass_decryption)
        self.password_entry_decryption.bind("<FocusIn>", self.__validate_pass_decryption)
        self.password_entry_decryption.bind("<KeyRelease>", self.__validate_pass_decryption)


    def __submit_encrypt(self):
        enc_fp = self.filepath_encryption
        enc_pass = self.password_entry_encryption.get()
        if enc_fp == "":
            messagebox.showerror(title="Error", message="No file to encrypt was selected!")
        elif len(enc_pass) < 12:
            messagebox.showerror(title="Error", message="Password must be at least 12 characters long")
        else:
            designator = self.driver.gen_designator()
            encryption_dest = filedialog.asksaveasfilename(title="Select where to save PaperTrail Document",initialdir=os.path.expanduser( '~' ), initialfile=f"papertrail_{designator}.pdf")
            try:
                return_path = self.driver.encrypt(password=enc_pass, data_path=enc_fp, dest_path=encryption_dest, designator=designator)
                messagebox.showinfo(title="Encrypted Successfully!", message=f"Document has been saved to {return_path}.")
            except Exception as e:
                messagebox.showerror(title="Error", message=f"Something went wrong and the data couldn't be encrypted!\n\nError:\n{e}")


    def __submit_decrypt(self):
        dec_fp = self.filepath_decryption
        dec_pass = self.password_entry_decryption.get()
        if dec_fp == "":
            messagebox.showerror(title="Error", message="No file to decrypt was selected!")
        elif len(dec_pass) < 12:
            messagebox.showerror(title="Error", message="Password must be at least 12 characters long")
        else:
            decryption_dest = filedialog.asksaveasfilename(title="Select file to save decrypted data in", initialdir=os.path.expanduser( '~' ))
            try:
                return_path = self.driver.decrypt(password=dec_pass, document_path=dec_fp, dest_path=decryption_dest)
                messagebox.showinfo(title="Decrypted Successfully!", message=f"Data has been saved to {return_path}.")
            except Exception as e:
                messagebox.showerror(title="Error", message=f"Something went wrong and the file couldn't be decrypted!\n\nError:\n{e}")


def add_poppler_path():
    # Adds poppler in resources folder to PATH on Windows
    rel_poppler_binpath = os.path.join("poppler", "Library", "bin")
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller onefile compatibility
        os.chdir(sys._MEIPASS)
        poppler_binpath = os.path.join(sys._MEIPASS, rel_poppler_binpath)
    else:
        # Just use path of the python script
        poppler_binpath = os.path.abspath(os.path.join(os.path.dirname(__file__), rel_poppler_binpath))
    os.environ["PATH"]+=os.pathsep+poppler_binpath


if __name__ == "__main__":
    # Adds bundled poppler to PATH if on Windows
    if sys.platform.startswith('win'):
        add_poppler_path()
    
    # Initialize root window and application
    root = tk.Tk()
    app = PaperTrailGUI(root)

    # Set Sun Valley TTK theme
    sv_ttk.set_theme("dark")

    # Main Loop
    root.mainloop()
