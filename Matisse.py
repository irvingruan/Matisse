#!/usr/bin/env python

# Written by Irving Y. Ruan <irvingruan@gmail.com>
# All rights reserved.

# See README for instructions on how to use Matisse

import sys
import os
import fnmatch
import errno
import mmap
import contextlib
import shutil
import subprocess
import mhtml
import Image

JPEG_SIGNATURE_OFFSET = 492

artwork_item_count = 0
artwork_name_prefix = "AlbumArtwork"
local_url_prefix = "file://"

artworkDumpPath = '~/Desktop/MatisseAlbumArtwork/'
artworkDumpPath = os.path.expanduser(artworkDumpPath)

def print_usage():
    print "Usage: ./Matisse.py\n"

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
        os.makedirs(artworkDumpPath+'/artwork')
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise Exception("Artwork dump folder already exists!")
            
def create_jpeg_from_itc(artwork_file):
    global artwork_item_count
    global artwork_name_prefix
    
    try:
        artwork_item_count += 1
        
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
        
        artwork_path_components = jpeg_file.split("/")
        artwork_path_components[-1] = artwork_name_prefix + str(artwork_item_count) + ".jpeg"
        jpeg_file = "/".join(artwork_path_components)
        
        os.rename(artwork_file, jpeg_file)
    except:
        sys.stderr.write("Error: could not convert %s to JPEG." % str(artwork_file))
        
def generate_html():
    try:
        artwork_jpegs = os.listdir(artworkDumpPath + "/artwork")
        
        html_output = open('matisse.html', 'w')
        html_output.write(mhtml.header)
        html_output.write(mhtml.body_start)
        
        item = 0
        for i in range(0, len(artwork_jpegs) - 200):
            html_output.write("\t\t<div class=\"item\">\n")
            html_output.write("\t\t\t<img class=\"content\" src=\"artwork/AlbumArtwork" + str(i+1) + ".jpeg\"/>\n")
            html_output.write("\t\t</div>\n")
        
        html_output.write(mhtml.body_end)   
        html_output.close()
        
    except:
        sys.stderr.write("Error: Unable to generate matisse.html.")
        sys.exit(-1)
        
def deploy_matisse():
    try:
        # Copy over the .html, .js, and .css files
        shutil.move(os.getcwd() + "/index.html", artworkDumpPath)
        matisse_publish_files = os.listdir(os.getcwd() + '/publish')
        
        rv = subprocess.Popen('cp -rf ' + os.getcwd() + '/publish/. ' + artworkDumpPath, shell=True)
        rv.wait()
        
        rv = subprocess.Popen('open /Applications/Safari.app ' + artworkDumpPath + '/index.html', shell=True)
        rv.wait()
        
    except:
        sys.stderr.write("Error: Could not publish Matisse Cover Flow.\n")
        sys.exit(-1)
        
def convert_proc():
    global local_url_prefix
    
    album_artwork_path = locate_album_artwork_path()
    itc_list = retrieve_itc_files(album_artwork_path)
    create_artwork_dump()
        
    # Copy over the .itc files so we don't modify iTunes version
    # We simply want the album artwork
    for itc_file in itc_list:
        shutil.copy(itc_file, artworkDumpPath+'/artwork')
    
    artwork_path = artworkDumpPath + 'artwork'
    new_itc_files = os.listdir(artwork_path)
    for itc_file in new_itc_files:
        create_jpeg_from_itc(os.path.join(artwork_path, itc_file))
    
    print "Finished converting iTunes album artwork files to JPEGs.\nThey are located at " + artwork_path
    

def main():
    
    if len(sys.argv) > 1:
        print_usage()
        sys.exit(-1)
    
    global artwork_item_count
    artwork_item_count = 0

    # If we already have the JPEGs, no need to convert it again
    if not(os.path.exists(artworkDumpPath) and os.listdir(artworkDumpPath)):       
        convert_proc()
        generate_html()
        deploy_matisse()
       
    else:
        sys.stderr.write("Album artwork dump folder already exists. Recreate anyway? (y/n):")
        key = 0
        try:
            key = sys.stdin.read(1)
        except KeyboardInterrupt:
            key = 0
            
        if key == 'y':
            convert_proc()
            generate_html()
            deploy_matisse()
            
        elif key == 'n':
            sys.stderr.write("\nView your artwork at " + artworkDumpPath)
        elif key == 0:
            sys.stderr.write("\nError: keyboard interrupted.")


if __name__ == "__main__":
    main()
