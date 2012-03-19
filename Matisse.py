#!/usr/bin/env python

# Written by Irving Y. Ruan <irvingruan@gmail.com>
# All rights reserved.

# See README for instructions on how to use Matisse

import os
import fnmatch
import errno

pathToAlbumArtwork = '~/Music/iTunes/Album Artwork/Download/'
pathToAlbumArtwork = os.path.expanduser(pathToAlbumArtwork)

artworkDumpPath = '~/Desktop/Matisse_Dump'
artworkDumpPath = os.path.expanduser(artworkDumpPath)

"""TO DO"""
def usage():
    raise None

"""TO DO"""
def help():
    raise None

def retrieve_itc_files():
    
    itc_list = []
    pattern = '*.itc'

    # Grab only iTunes album artwork files (*.itc)
    for root, dirs, files in os.walk(pathToAlbumArtwork):
        for filename in fnmatch.filter(files, pattern):
            print( os.path.join(root, filename))
            itc_list.append(os.path.join(root, filename))
                
    return itc_list
    
def create_artwork_dump():
    
    try:
        os.makedirs(artworkDumpPath)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
            
def parse_itunes_artwork(artwork_file):

def main():

    itc_list = retrieve_itc_files()

    create_artwork_dump()

if __name__ == "__main__":
    main()
