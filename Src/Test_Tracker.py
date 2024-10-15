import Torrent as TorrentClass
import Tracker as TrackerClass 
import tkinter as tk
from tkinter import filedialog


def main():
    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename()

   #Primeiro Criar o Torrent , class que faz parse
    Torrent = TorrentClass.Torrent(filePath)
    # Em seguida mandar o Torrent para o tracker e mandar conectar
    Tracker = TrackerClass.Tracker(Torrent)
    
    print(Tracker.Connect(True, 0, 0))

main()
