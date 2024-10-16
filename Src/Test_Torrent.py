import Torrent as TorrentClass
import tkinter as tk
from tkinter import filedialog




def main():
    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename()
    TorrentInstance = TorrentClass.Torrent(filePath)
    print(TorrentInstance)


main()
