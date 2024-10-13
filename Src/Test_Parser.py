from InputFileParser import * 
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

filePath = filedialog.askopenfilename()



def main():
    with open(filePath, 'rb') as f:
        metainfo = f.read()
        # Torrent is now a dictionary
        torrent = bencodepy.decode(metainfo)
        print(torrent)


main()
