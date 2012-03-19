#!/usr/bin/env python

# Written by Irving Y. Ruan <irvingruan@gmail.com>
# All rights reserved.

# See README for instructions on how to use Matisse

import os
import fnmatch
import errno
import mmap
import contextlib
import shutil

pathToAlbumArtwork = '~/Music/iTunes/Album Artwork/Download/'
pathToAlbumArtwork = os.path.expanduser(pathToAlbumArtwork)

artworkDumpPath = '~/Desktop/Matisse_Dump/itc_dump/'
artworkDumpPath = os.path.expanduser(artworkDumpPath)

itcDumpPath = '~/Desktop/Matisse_Dump/itc_dump/'
itcDumpPath = os.path.expanduser(itcDumpPath)

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
        os.makedirs(itcDumpPath)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise Exception("Artwork dump directory already exists!")
            
# def copy_itc_files(itc_files):
#     for itc_file in itc_files:
#         copy(itc_file, artworkDumpPath)
            
def parse_itunes_artwork(artwork_file):
    
    with open(artwork_file, 'r') as itc_file:
        with contextlib.closing(mmap.mmap(itc_file.fileno(), 0,                access=mmap.ACCESS_READ)) as m:
            print 'Bytes via 490 - 520 : ', m[490:521]

def main():

    itc_list = retrieve_itc_files()
    create_artwork_dump()
    
    for itc_file in itc_list:
        shutil.copy(itc_file, itcDumpPath)

if __name__ == "__main__":
    main()
