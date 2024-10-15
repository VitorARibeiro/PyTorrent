import bencodepy
# DecodedTorrent gets the .torretn file and decodes it


def GetDecodedTorrent(filepath):

    with open(filepath, 'rb') as f:
        metainfo = f.read()
        # Torrent is now a dictionary
        Decoded_torrent = bencodepy.decode(metainfo)

    return Decoded_torrent

# BencodedInfoHash gets info from .torrent decoded file and encodes it back


def GetBencodedInfo(Decoded_Torrent):

    Bencoded_Info = bencodepy.encode(Decoded_Torrent[b'info'])

    return Bencoded_Info


def GetSumFileLengths(Decoded_Torrent):
    # Access the 'info' dictionary within the torrent file
    info_dict = Decoded_Torrent[b'info']

    #Se for um Torrent Single file podemos aceder diretamente ao b'lenght'
    #Se for multi File temos uma lista de ficheiros e so depois os tamanhos de cada 1
    total_length = 0 #Inicializacao da variavel
    if b'length' in info_dict:
        total_length = info_dict[b'length']
    else:        
        files_list = info_dict[b'files']
        for file_entry in files_list: 
            total_length += file_entry[b'length']
    

    return total_length


def GetAnnounceUrl(Decoded_Torrent):
    announce_url = Decoded_Torrent[b'announce'].decode('utf-8')
    return announce_url


def GetTrackerType(announceUrl):    
    TrackerType = announceUrl.split(':')[0]  
    
    return TrackerType