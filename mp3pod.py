
import glob, os, re, sys
import stagger
from stagger.id3 import *
import shutil

ultimate_regex = [
'''# Shit
^
(?P<Artist>.+)
\s-\s
(?P<ReleaseYear>\d{4})
\.
(?P<ReleaseMonth>\d{2})
\.
(?P<ReleaseDay>\d{2})
\s-\s
(?P<Title>.+)
[.]+?''']

walkdir = './ipod'
sortedDir = './sorted'

# Scan every directory for file
for dirName, subdirList, fileList in os.walk(walkdir):
    for file in fileList:
        # Get the full path of the scanned file
        fullFilePath = os.path.join(os.path.abspath(dirName), file)

        # The file must be a mp3 file and larger than zero in size
        if file.lower().endswith('.mp3') and os.stat(fullFilePath).st_size>0:

            # Use stagger to get tags from mp3 file
            mp3file = stagger.read_tag(fullFilePath)

            # Here we check if we can use id3 tags
            # to get our artist, title, album and track
            if TPE2 in mp3file:
                tpe2 = mp3file[TPE2].text[0]
            else:
                tpe2 = ''

            if TIT2 in mp3file:
                tit2 = mp3file[TIT2].text[0]
            else:
                tit2 = ''

            if TALB in mp3file:
                talb = mp3file[TALB].text[0]
            else:
                talb = ''

            if TRCK in mp3file:
                trck = mp3file[TRCK].text[0]
            else:
                trck = ''

            # Here is just temporary variables to get artist, title, album and track
            tmp_artist = mp3file.artist if mp3file.artist is not '' else tpe2

            tmp_title = mp3file.title if mp3file.title is not '' else tit2

            tmp_album = mp3file.album if mp3file.album is not '' else talb

            tmp_track = mp3file.track if mp3file.track else trck

            # Here is checked if the tags are empty. If so the text is replaced.
            # We also replace bad char in filename (for linux at least)
            artist = str(tmp_artist if tmp_artist is not '' else 'unknown artist').replace(':', '').replace('/', '')
            title = str(tmp_title if tmp_title is not '' else 'unknown title').replace(':', '').replace('/', '')
            album = str(tmp_album if tmp_album is not '' else '').replace(':', '').replace('/', '')
            track = tmp_track if tmp_track else ''

            # If the album name is empty and artist
            # we just get the title and use that as our filename
            if artist == 'unknown artist' and album == '':
                    newName = mp3file.title

            # Else use what we got from reading the tags
            else:
                if track is not '':
                    newName = "%02d - %s - %s" % (track, artist, title)
                else:
                    newName = "%s - %s" % (artist, title)

            newName = "%s.mp3" % newName

            # Create the new folder path as in ./sorted/Artist/Album/
            fullNewPath = os.path.join(sortedDir, os.path.join(artist, album))

            # Create the new filename and file path, ./sorted/Artist/Album/track number - Artist - Title
            fullNewName = os.path.join(fullNewPath, newName)

            # Create the new path
            if not os.path.exists(fullNewPath):
                try:
                    os.makedirs(fullNewPath)
                except:
                    print("Error making path %s", fullNewPath)

            # If the file doesn't exist we move it
            if not os.path.exists(fullNewName):
                try:
                    shutil.move(fullFilePath, fullNewName)
                except:
                    print("Error moving %s to %s" % (fullFilePath, fullNewName) )
