import requests
import TorrentParser  
import Sha1
import random
# import requests

# DecodedTorrent should be the original
# torrent file Decoded by bencodepy, a dictionary


def SendRequest(file_path):
    # Paramater defenition
    # info_hash 	The SHA1 hash of the info dict found in the .torrent
    # peer_id 	A unique ID generated for this client
    # uploaded 	The total number of bytes uploaded
    # downloaded 	The total number of bytes downloaded
    # left 	The number of bytes left to download for this client
    # port 	The TCP port this client listens on
    # compact 	Whether or not the client accepts a compacted list of peers


    Decoded_Torrent = TorrentParser.GetDecodedTorrent(file_path)

    announce_url = TorrentParser.GetAnnounceUrl(Decoded_Torrent)
    Encoded_Info = TorrentParser.GetBencodedInfo(Decoded_Torrent)
    info_hash = Sha1.hash_sha1(Encoded_Info)

    peer_id = '-PC0001-' + \
        ''.join([str(random.randint(0, 9)) for _ in range(12)])
    uploaded = 0
    downloaded =  0
    left = TorrentParser.GetSumFileLengths(Decoded_Torrent)
    port = 6969
    event = "started"
    compact = 1

    #Temos de Testar se é um Http Tracker ou UDP Tracker
    #TODO Adicionar suporte para UDP Trackers
    Trackertype = TorrentParser.GetTrackerType(announce_url)
    if(Trackertype == "https" or Trackertype == "http"):
        Params = {'info_hash': info_hash,
                    'peer_id': peer_id,
                    'uploaded': uploaded,
                    'downloaded': downloaded,
                    'left': left,
                    'port':port,
                    'event': event,
                    'compact': compact}
        return requests.get(url=announce_url, params=Params)
    else:
        print("Tracker Type not suported (Not HTTPS or HTTP)")
        return None

