import asyncio
from Torrent import Torrent
import tkinter as tk
from tkinter import filedialog

def main():
    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename()


main()