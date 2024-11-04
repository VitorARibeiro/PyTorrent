import bencodepy
import httpx
from struct import unpack
import random
import logging
from urllib.parse import urlencode
import socket

def _CalculatePeerId():
    """
    Calculate and return a unique Peer ID.

    The `peer id` is a 20 byte long identifier. This implementation use the
    Azureus style `-PC1000-<random-characters>`.

    Read more:
        https://wiki.theory.org/BitTorrentSpecification#peer_id
    """
    return '-PC0001-' + ''.join(
        [str(random.randint(0, 9)) for _ in range(12)])


def _DecodePort(port):
    """
    Converts a 32-bit packed binary port number to int
    converts from b'\x1A\x2B' to 6699
    """
    # Convert from C style big-endian encoded as unsigned short
    return unpack(">H", port)[0]

class TrackerResponse:
    

    def __init__(self, response: dict):
        self.response = response

    @property
    def failure(self):
        """
        If this response was a failed response, this is the error message to
        why the tracker request failed.

        If no error occurred this will be None
        """
        if b'failure reason' in self.response:
            return self.response[b'failure reason'].decode('utf-8')
        return None

    @property
    def interval(self) -> int:
        """
        Interval in seconds that the client should wait between sending
        periodic requests to the tracker.
        """
        return self.response.get(b'interval', 0)

    @property
    def complete(self) -> int:
        """
        Number of peers with the entire file, i.e. seeders.
        """
        return self.response.get(b'complete', 0)

    @property
    def incomplete(self) -> int:
        """
        Number of non-seeder peers, aka "leechers".
        """
        return self.response.get(b'incomplete', 0)

    @property
    def peers(self):
        """
        A list of tuples for each peer structured as (ip, port)
        """
        # The BitTorrent specification specifies two types of responses. One
        # where the peers field is a list of dictionaries and one where all
        # the peers are encoded in a single string
        peers = self.response[b'peers']
        if type(peers) == list:
            # TODO Implement support for dictionary peer list
            print('Dictionary model peers are returned by tracker')
            raise NotImplementedError()
        else:
            print('Binary model peers are returned by tracker')

            # Split the string in pieces of length 6 bytes, where the first
            # 4 characters is the IP the last 2 is the TCP port.
            peers = [peers[i:i+6] for i in range(0, len(peers), 6)]

            # Convert the encoded address to a list of tuples
            return [(socket.inet_ntoa(p[:4]), _DecodePort(p[4:]))
                    for p in peers]

    def __str__(self):
        return "incomplete: {incomplete}\n" \
               "complete: {complete}\n" \
               "interval: {interval}\n" \
               "peers: {peers}\n".format(
                   incomplete=self.incomplete,
                   complete=self.complete,
                   interval=self.interval,
                   peers=self.peers)

class Tracker:
    def __init__(self, Torrent):
        self.Torrent = Torrent
        self.PeerId = _CalculatePeerId()
        self.httpClient = httpx.AsyncClient()

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

        url = self.Torrent.AnnounceUrl + '?' + urlencode(Params)
        # logging.info('Connecting to tracker at: ' + url)
        print('Connecting to tracker at: ' + url)

        response = await self.httpClient.get(url)
        if not response.status_code == 200:
            raise ConnectionError('Unable to connect to tracker: status code {}'.format(response.status))

        data = response.content
        self.raise_for_error(data)
        return TrackerResponse(bencodepy.decode(data))

    async def close(self):
        await self.httpClient.aclose()

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
