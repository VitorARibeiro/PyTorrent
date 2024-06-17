import bencodepy


def main():
    with open('/home/vitor-ribeiro/Downloads/ubuntu-22.04.4-desktop-amd64.iso.torrent', 'rb') as f:
        metainfo = f.read()
        # Torrent is now a dictionary
        torrent = bencodepy.decode(metainfo)
        print(torrent[b'announce'])


main()
