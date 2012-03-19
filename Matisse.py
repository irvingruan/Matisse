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

JPEG_SIGNATURE_OFFSET = 492

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
            itc_list.append(os.path.join(root, filename))
                
    return itc_list
    
def create_artwork_dump():
    
    try:
        os.makedirs(artworkDumpPath)
        os.makedirs(itcDumpPath)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise Exception("Artwork dump directory already exists!")
            
def create_jpeg_from_itc(artwork_file):
    
    itc_file_handle = open(artwork_file, "r+")
    byte_data = mmap.mmap(itc_file_handle.fileno(),0)
    
    file_size = len(byte_data)
    new_size = file_size - JPEG_SIGNATURE_OFFSET

    byte_data.move(0, JPEG_SIGNATURE_OFFSET, file_size - JPEG_SIGNATURE_OFFSET)
    byte_data.flush()
    byte_data.close()
    itc_file_handle.truncate(new_size)
    byte_data = mmap.mmap(itc_file_handle.fileno(),0)
    
    jpeg_file = artwork_file.replace('.itc', '.jpeg')
    os.rename(artwork_file, jpeg_file)

def main():

    itc_list = retrieve_itc_files()
    create_artwork_dump()
    
    # Copy over the .itc files so we don't modify iTunes version
    # We simply want the album artwork
    for itc_file in itc_list:
        shutil.copy(itc_file, itcDumpPath)
        
    new_itc_files = os.listdir(itcDumpPath)
    for itc_file in new_itc_files:
        create_jpeg_from_itc(os.path.join(itcDumpPath, itc_file))


if __name__ == "__main__":
    main()
