import tkinter as tk
from tkinter import filedialog
import os

class PapertrailUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PaperTrail")
        self.root.configure(bg="white")

        # Styles
        self.label_style = {'font': ('Arial', 12), 'bg': 'white'}
        self.button_style = {'font': ('Arial', 12), 'width': 20, 'bg': 'lightgrey', 'bd': 0, 'highlightthickness': 0, 'borderwidth': 0}
        self.entry_style = {'font': ('Arial', 12)}


        self.title_label = tk.Label(self.root, text="PaperTrail", font=('Arial', 18, 'bold'), bg='white')
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')


        tk.Label(self.root, text="Encrypt", font=('Arial', 14, 'bold'), bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='n')


        self.encrypt_frame = tk.LabelFrame(self.root, text="", padx=20, pady=20, bg='white')
        self.encrypt_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        tk.Label(self.encrypt_frame, text="Select a file to encrypt:", **self.label_style).grid(row=0, column=0, sticky='w')
        self.select_file_button_encryption = tk.Button(self.encrypt_frame, text="Select File", **self.button_style, command=self.select_file_encryption)
        self.select_file_button_encryption.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        tk.Label(self.encrypt_frame, text="Encryption Password (12 characters minimum):", **self.label_style).grid(row=2, column=0, sticky='w')
        self.password_entry_encryption = tk.Entry(self.encrypt_frame, show="*", **self.entry_style)
        self.password_entry_encryption.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        self.encrypt_button = tk.Button(self.encrypt_frame, text="Encrypt", **self.button_style)
        self.encrypt_button.grid(row=4, column=0, padx=5, pady=5, sticky='w')


        tk.Label(self.root, text="Decrypt", font=('Arial', 14, 'bold'), bg='white').grid(row=1, column=1, padx=10, pady=10, sticky='n')


        self.decrypt_frame = tk.LabelFrame(self.root, text="", padx=20, pady=20, bg='white')
        self.decrypt_frame.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        tk.Label(self.decrypt_frame, text="Select a scan to decrypt:", **self.label_style).grid(row=0, column=0, sticky='w')
        self.select_file_button_decryption = tk.Button(self.decrypt_frame, text="Select File", **self.button_style, command=self.select_file_decryption)
        self.select_file_button_decryption.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        tk.Label(self.decrypt_frame, text="Decryption Password (12 characters minimum):", **self.label_style).grid(row=2, column=0, sticky='w')
        self.password_entry_decryption = tk.Entry(self.decrypt_frame, show="*", **self.entry_style)
        self.password_entry_decryption.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        self.decrypt_button = tk.Button(self.decrypt_frame, text="Decrypt", **self.button_style)
        self.decrypt_button.grid(row=4, column=0, padx=5, pady=5, sticky='w')

    def select_file_encryption(self):
        self.filepath_encryption = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File to Encrypt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

    def select_file_decryption(self):
        self.filepath_decryption = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File to Decrypt", filetypes=(("Encrypted files", "*.enc"), ("All files", "*.*")))


if __name__ == "__main__":
    root = tk.Tk()
    app = PapertrailUI(root)
    root.mainloop()