import requests
import InputFileParser
import Sha1
import random
# import requests

# DecodedTorrent should be the original
# torrent file Decoded by bencodepy, a dictionary


def SendRequest(file_path):
    Decoded_Torrent = InputFileParser.DecodedTorrent(file_path)
    announce_url = Decoded_Torrent[b'announce']

    # Paramater defenition
    # info_hash 	The SHA1 hash of the info dict found in the .torrent
    # peer_id 	A unique ID generated for this client
    # uploaded 	The total number of bytes uploaded
    # downloaded 	The total number of bytes downloaded
    # left 	The number of bytes left to download for this client
    # port 	The TCP port this client listens on
    # compact 	Whether or not the client accepts a compacted list of peers

    Encoded_Info = InputFileParser.BencodedInfo(Decoded_Torrent)
    info_hash = Sha1.hash_sha1(Encoded_Info)

    peer_id = '-PC0001-' + \
        ''.join([str(random.randint(0, 9)) for _ in range(12)])

    left = InputFileParser.SumFileLengths(Decoded_Torrent)

    compact = 1

    Params = {'info_hash': info_hash, 'peer_id': peer_id,
              'left': left, 'compact': compact}

    return requests.get(url=announce_url, params=Params)
