"""
#######################################################################################
Ranch Hand - Updater/Installer System
(c) Stanley Solutions

By: Joe Stanley
#######################################################################################
"""

# Import Required Dependencies
import os
import sys
import csv
import time
import ctypes
import urllib
from pathlib import Path

# Define Folder Locations
programData  = 'C:/ProgramData/StanleySolutions/KRNC/RanchHand'
programFiles = 'C:/Program Files (x86)/StanleySolutions/KRNC/RanchHand/images'

# Define Download Descriptor Location
web_requirements_file = 'https://raw.githubusercontent.com/engineerjoe440/KRNCApps/master/requirements.csv'

# Define UAC Elevation Decorator
def elevateUAC( func ):
    """ Simple Wrapper Function to Elevate to Admin with UAC """
    # Define Imports Required for Elevation
    import ctypes, sys
    import time
    # Define Inner Test to Evaluate
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    # Define Inner Wrapper Function
    def inner():
        # Test for Admin Level
        if is_admin():
            # Run the Function at Admin Level
            func()
        else:
            # Re-run the program with admin rights
            command = '"{}" {}'.format(sys.argv[0], " ".join(sys.argv[1:]))
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, 
                                                command, None, 1)
    # Return Inner Function
    return( inner )

# Define Function to Generate Folder Paths
def build_folders():
    # Check for Folder Locations
    if not os.path.exists(programData):
        Path(os.path.dirname(programData)).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(programFiles):
        Path(os.path.dirname(programFiles)).mkdir(parents=True, exist_ok=True)

# Define Function to Read Requirements from Web-Based CSV
def read_requirements():
    # Open File from Web to Identify Requirements
    with urllib.urlopen(web_requirements_file) as requires:
        requirements_text = csv.reader( requires )
    # Build Descriptive Structure
    requirements = []
    for row in requirements_text:
        requirements.append( row.split(',') )
    return(requirements)


# Define Main Function
@elevateUAC
def main():
    # Build Folders
    build_folders()
    # Identify Requirements
    try:
        requires = read_requirements()
    except:
        print("Unable to open web-handle for requirements file.")
        time.sleep(5)
        sys.exit(1)
    print(requires)



# Create Entrypoint
if __name__ == '__main__':
    # Call Main Function
    main()


# END
