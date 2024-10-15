from TorrentParser import * 
import tkinter as tk
from tkinter import filedialog




def main():
    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename()
    Torrent = DecodedTorrent(filePath)
    Info = BencodedInfo(Torrent)
    SumFile = SumFileLengths(Torrent)
    print(SumFile)


main()
