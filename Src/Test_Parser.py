from TorrentParser import * 
import tkinter as tk
from tkinter import filedialog




def main():
    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename()
    Torrent = GetDecodedTorrent(filePath)
    info = GetBencodedInfo(Torrent)
    SumFile = GetSumFileLengths(Torrent)
    print(SumFile)


main()
