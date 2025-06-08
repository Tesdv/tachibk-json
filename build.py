import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import gzip
from json import dumps, loads
from google.protobuf.json_format import MessageToDict, Parse
from schema_pb2 import Backup

def tachi_to_json(input_path, output_path):
    """Convert .tachibk to .json"""
    msg = Backup()
    with gzip.open(input_path, 'rb') as f:
        msg.ParseFromString(f.read())
    Path(output_path).write_text(dumps(MessageToDict(msg), indent=2), encoding='utf-8')

def json_to_tachi(input_path, output_path):
    """Convert .json to .tachibk"""
    data = loads(Path(input_path).read_text(encoding='utf-8'))
    with gzip.open(output_path, 'wb') as w:
        w.write(Parse(dumps(data), Backup()).SerializeToString())

def get_conversion_info(input_path):
    """Return conversion function, output extension, and filetypes based on input file extension."""
    ext = Path(input_path).suffix.lower()
    if ext == ".tachibk":
        return tachi_to_json, ".json", [("JSON", "*.json")]
    elif ext == ".json":
        return json_to_tachi, ".tachibk", [("Tachiyomi Backup", "*.tachibk")]
    else:
        return None, None, None

class ConverterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tachibk/JSON Converter")
        self.input_file = tk.StringVar()

        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Input file:").grid(row=0, column=0, sticky='w')
        tk.Entry(frame, textvariable=self.input_file, width=40).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5)

        self.convert_btn = tk.Button(frame, text="Convert and Save", command=self.convert)
        self.convert_btn.grid(row=1, column=0, columnspan=3, pady=15)

    def browse_input(self):
        filetypes = [("TachiBackup / JSON", "*.tachibk *.json"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(title="Select file", filetypes=filetypes)
        if filename:
            self.input_file.set(filename)
            self.update_button_text(filename)

    def update_button_text(self, filename):
        ext = Path(filename).suffix.lower()
        if ext == ".tachibk":
            self.convert_btn.config(text="Convert and Save to JSON")
        elif ext == ".json":
            self.convert_btn.config(text="Convert and Save to Tachibk")
        else:
            self.convert_btn.config(text="Convert and Save")

    def convert(self):
        input_path = self.input_file.get()
        if not input_path:
            messagebox.showerror("Error", "Please select an input file.")
            return

        convert_func, default_ext, filetypes = get_conversion_info(input_path)
        if not convert_func:
            messagebox.showerror("Error", "Unsupported file type. Please select a .tachibk or .json file.")
            return

        output_path = filedialog.asksaveasfilename(
            title="Save converted file as...",
            defaultextension=default_ext,
            filetypes=filetypes
        )
        if not output_path:
            return

        try:
            convert_func(input_path, output_path)
            messagebox.showinfo("Success", f"File saved to:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed:\n{e}")

if __name__ == "__main__":
    ConverterGUI().mainloop()