import bencodepy

# DecodedTorrent gets the .torretn file and decodes it


def DecodedTorrent(filepath):

    with open(filepath, 'rb') as f:
        metainfo = f.read()
        # Torrent is now a dictionary
        Decoded_torrent = bencodepy.decode(metainfo)

    return Decoded_torrent

# BencodedInfoHash gets info from .torrent decoded file and encodes it back


def BencodedInfo(Decoded_Torrent):

    Bencoded_Info = bencodepy.encode(Decoded_Torrent[b'info'])

    return Bencoded_Info


def SumFileLengths(Decoded_Torrent):

    # Access the 'info' dictionary within the torrent file
    info_dict = Decoded_Torrent[b'info']

    # Access the 'files' list within the 'info' dictionary
    files_list = info_dict[b'files']

    # Initialize sum of file lengths
    total_length = 0

    # Iterate over each file entry in the 'files' list
    for file_entry in files_list:
        # Add the length of the current file to the total length
        total_length += file_entry[b'length']

    return total_length
