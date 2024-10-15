import Tracker as Tracker
import tkinter as tk
from tkinter import filedialog


def main():
    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename()

    response = Tracker.SendRequest(filePath) 

    if response == None:
        return 
    
    if(response.status_code == 200):
        print(response.text)
    else:
        print("Erro na resposta do tracker")
        print(response.status_code)


main()
