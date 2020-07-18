#############################################################
"""
    Zip and Distribute The Ranch!
    
    `AutoZipper.py`
    
    A simple Python script to zip all local imaging files in
    preparation to be pushed to GitHub and distributed.
"""
#############################################################
# Automatic Zipper File

import os
import zipfile
import argparse

# Create Parser Object
parser = argparse.ArgumentParser(description="`AutoZipper.py` " + 
    "A simple Python script to package all imaging files in a zipped " +
    "folder structure in preparation to upload to GitHub for distribution.")
parser.add_argument('-s','--source',default=os.getcwd(),
    help="the fully-qualified directory path to locate files from")
parser.add_argument('-o','--output',default='KrncBranding.zip',
    help="the zipped folder structure which should be created")

# Zip Files
def zipdir(path, ziph, extpath=''):
    for file in os.listdir(path):
        if file.endswith('.mp3'):
            # Collect all Imaging Files
            ziph.write(os.path.join(extpath, file))

# Main Function
def main( parser ):
    args = parser.parse_args()
    src = args.source
    out = args.output
    # Create Zipfile Object and Store Files
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(src, zipf)


# Run Main Operation
if __name__ == '__main__':
    main( parser )