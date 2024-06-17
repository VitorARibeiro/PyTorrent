import Src.Tracker as Tracker


def main():
    path = '/home/vitor-ribeiro/Downloads/ubuntu-22.04.4-desktop-amd64.iso.torrent'
    Resposnse = Tracker.SendRequest(path)
    print(Resposnse)


main()
