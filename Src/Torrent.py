from hashlib import sha1
import bencodepy
# DecodedTorrent gets the .torretn file and decodes it

class Torrent:

    def __init__(self, filepath):
        self.FilePath = filepath

        with open(self.FilePath, 'rb') as f:
            MetaInfo = f.read()
            self.MetaInfo = bencodepy.decode(MetaInfo)

        EncodedInfo = bencodepy.encode(self.MetaInfo[b'info'])
        self.InfoHash = sha1(EncodedInfo).digest() 
        self.FileLength = self.GetSumFileLengths()
        self.AnnounceUrl = self.GetAnnounceUrl()
        self.TrackerType = self.GetTrackerType()



    def GetSumFileLengths(self):
        # Access the 'info' dictionary within the torrent file
        #Se for um Torrent Single file podemos aceder diretamente ao b'lenght'
        #Se for multi File temos uma lista de ficheiros e so depois os tamanhos de cada 1
        Info = self.MetaInfo[b'info']
        total_length = 0 #Inicializacao da variavel
        #Single File Torrents
        if b'length' in Info:
            total_length = Info[b'length']
        else:        
            #MultiFile Torrents
            files_list = Info[b'files']
            for file_entry in files_list: 
                total_length += file_entry[b'length']
        

        return total_length

    def GetAnnounceUrl(self):
        announce_url = self.MetaInfo[b'announce'].decode('utf-8')
        return announce_url

    def GetTrackerType(self):    
        TrackerType = self.AnnounceUrl.split(':')[0]  
        
        return TrackerType
    
    #Function to print it 
    def __str__(self):
        """Representação legível da classe."""
        return f"Torrent Info:\n" \
               f"File Path: {self.FilePath}\n" \
               f"Info Hash: {self.InfoHash.hex()}\n" \
               f"File Length: {self.FileLength} bytes\n" \
               f"Announce URL: {self.AnnounceUrl}\n" \
               f"Tracker Type: {self.TrackerType}"