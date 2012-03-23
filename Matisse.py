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

artworkDumpPath = '~/Desktop/Matisse_Dump/'
artworkDumpPath = os.path.expanduser(artworkDumpPath)

itcDumpPath = '~/Desktop/Matisse_Dump/itc_dump/'
itcDumpPath = os.path.expanduser(itcDumpPath)

"""TO DO"""
def usage():
    raise None

"""TO DO"""
def help():
    raise None
    
def locate_album_artwork_path():
    
    album_artwork_path = os.path.expanduser("~/Music")
    
    for root, subFolders, files in os.walk(album_artwork_path):
	    for sf in subFolders:
	        # We only want the Download folder, not Cache
			if sf.lower() == "download":
			    path_components = os.path.join(root, sf).split("/")
			    if path_components[-2].lower() == "album artwork":
				    return os.path.join(root, sf)
				
def retrieve_itc_files(album_artwork_path):
    
    itc_list = []
    pattern = '*.itc'

    # Grab only iTunes album artwork files (*.itc)
    for root, dirs, files in os.walk(album_artwork_path):
        for filename in fnmatch.filter(files, pattern):
            itc_list.append(os.path.join(root, filename))
                
    return itc_list
    
def create_artwork_dump():
    
    try:
        os.makedirs(artworkDumpPath)
        os.makedirs(itcDumpPath)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise Exception("Artwork dump folder already exists!")
            
def create_jpeg_from_itc(artwork_file):
    
    try:
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
    except:
        sys.stderr.write("Could not convert %s to JPEG." % str(artwork_file))

def main():

    # If we already have the JPEGs, no need to convert it again
    if not(os.path.exists(artworkDumpPath) and os.listdir(artworkDumpPath)):
        
        album_artwork_path = locate_album_artwork_path()
        itc_list = retrieve_itc_files(album_artwork_path)
        create_artwork_dump()
            
        # Copy over the .itc files so we don't modify iTunes version
        # We simply want the album artwork
        for itc_file in itc_list:
            shutil.copy(itc_file, itcDumpPath)
        
        new_itc_files = os.listdir(itcDumpPath)
        for itc_file in new_itc_files:
            create_jpeg_from_itc(os.path.join(itcDumpPath, itc_file))
        
    else:
        print "Album artwork dump folder already exists with data."


if __name__ == "__main__":
    main()
