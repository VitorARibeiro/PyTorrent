import Tracker as Tracker
import tkinter as tk
from tkinter import filedialog


def main():
    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename()
    
    print(Tracker.SendRequest(filePath))


main()
