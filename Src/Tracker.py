import bencodepy
import aiohttp
import random
import logging
from urllib.parse import urlencode
# import requests

# DecodedTorrent should be the original
# torrent file Decoded by bencodepy, a dictionary

class Tracker:

    def __init__(self, Torrent):
        self.Torrent = Torrent
        self.PeerId = CalculatePeerId()
        self.httpClient = aiohttp.ClientSession()

    async def Connect(self,
                first:bool = None,
                uploaded: int = 0,
                downloaded: int = 0):
        # Paramater defenition
        # info_hash 	The SHA1 hash of the info dict found in the .torrent
        # peer_id 	A unique ID generated for this client
        # uploaded 	The total number of bytes uploaded
        # downloaded 	The total number of bytes downloaded
        # left 	The number of bytes left to download for this client
        # port 	The TCP port this client listens on
        # compact 	Whether or not the client accepts a compacted list of peers


        Params = {'info_hash': self.Torrent.InfoHash,
                    'peer_id': self.PeerId,
                    'uploaded': uploaded,
                    'downloaded': downloaded,
                    'left': self.Torrent.FileLength - downloaded,
                    'port':6969,
                    'compact': 1}
        if first:
            Params['event'] = 'started'

        url = self.torrent.announce + '?' + urlencode(Params)
        logging.info('Connecting to tracker at: ' + url)

        async with self.http_client.get(url) as response:
            if not response.status == 200:
                raise ConnectionError('Unable to connect to tracker: status code {}'.format(response.status))
            data = await response.read()
            self.raise_for_error(data)
            return bencodepy.decode(data)

        def close(self):
            self.httpClient.close()

        def raise_for_error(self, tracker_response):
            """
            A (hacky) fix to detect errors by tracker even when the response has a status code of 200  
            """
            try:
                # a tracker response containing an error will have a utf-8 message only.
                # see: https://wiki.theory.org/index.php/BitTorrentSpecification#Tracker_Response
                message = tracker_response.decode("utf-8")
                if "failure" in message:
                    raise ConnectionError('Unable to connect to tracker: {}'.format(message))

            # a successful tracker response will have non-uncicode data, so it's a safe to bet ignore this exception.
            except UnicodeDecodeError:
                pass

def CalculatePeerId():
    PeerId = '-PC0001-' + \
            ''.join([str(random.randint(0, 9)) for _ in range(12)])
    return PeerId 