"""
#######################################################################################
Ranch Hand - VirtualDJ Settings Push/Pull and Management
(c) Stanley Solutions

By: Joe Stanley
#######################################################################################
"""

# Import Dependencies
import os
import shutil

# Define Monitored Files
monitoredFiles = [
    'ini',
    'xml',
    'txt',
    'm3u',
    'vdjfolder',
]


# Define Generic Text Section
generic_path = '<krnc-path>'

# Define "Empty Folder" Test Function
def folderisempty( folderpath ):
    return([f for f in os.listdir(folderpath) if not f.startswith('.')] == [])

# Define Modify and Move Function for Single Files
def modify_move_file(srcfpath, dstfpath, srcstring, dststring):
    # Format Source and Destination Folders with "Windows" Backslashes
    srcfpath = srcfpath.replace('/','\\')
    dstfpath = dstfpath.replace('/','\\')
    srcstring = srcstring.replace('/','\\')
    dststring = dststring.replace('/','\\')
    print("Resolving: '{}'  to: '{}'".format(srcfpath, dstfpath))
    print("   - '{}' replaced with '{}' placeholder".format(srcstring, dststring))
    # Validate Not License (Never Changes)
    if srcfpath.endswith('license.dat'):
        print("Skipping 'license.dat' File")
    # Check for Monitored File Type
    elif os.path.basename(srcfpath).split('.')[-1] in monitoredFiles:
        try:
            # Read Source
            with open(srcfpath, encoding='utf-8') as f:
                s = f.read()
            # Replace
            s = s.replace(srcstring, dststring)
            # Write to Destination
            with open(dstfpath, "w", encoding='utf-8') as f:
                f.write(s)
        except:
            try:
                shutil.copy(srcfpath,dstfpath)
            except:
                print("Warning - Skipping")
    # Un-manageable File Type
    else:
        try:
            shutil.copy(srcfpath,dstfpath)
        except:
            print("Warning - Skipping")

# Define Modify and Move Function for Entire Folders
def modify_move_folders(srcpath, dstpath, srcstring, dststring):
    # Walk over Source Path
    for dname, dirs, files in os.walk(srcpath):
        for fname in files:
            # Determine Fully-Qualified File Paths
            srcfpath = os.path.join(dname, fname)
            dstfpath = os.path.join(dname, fname).replace(srcpath,dstpath)
            # Modify and Move File
            modify_move_file(srcfpath, dstfpath, srcstring, dststring)


# END