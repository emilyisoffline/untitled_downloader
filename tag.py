# load the libraries that we'll use  
from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3  
import mutagen.id3  
from mutagen.id3 import ID3, APIC, PictureType
import glob, os, mimetypes
import numpy as np
import urllib.request, urllib.parse


def tagFolder(path, trackDetails):
    # extract the file names (including folders)  
    # for the mp3s in the album  
    filez = glob.glob(path+"/*.mp3")  
    # print the first element of filez:  
    albumArtName = urllib.parse.urlparse(trackDetails[0]['albumArt'])[2].split('/')[-1]
    if not os.path.exists(path+"/"+albumArtName):
        urllib.request.urlretrieve(trackDetails[0]['albumArt'], path+"/"+albumArtName)

    image_mime_type = mimetypes.guess_file_type(path+"/"+albumArtName)[0]

    with open(path+"/"+albumArtName, 'rb') as f:
        image_data = f.read()

    for file in filez:
        print("Tagging", file)
        tags = ID3(file)
        tags.setall('APIC', [APIC(
            mime=image_mime_type,
            type=PictureType.COVER_FRONT,
            data=image_data
        )])
        tags.save(v2_version=3)