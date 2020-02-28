# Install Script for KRNC USB Manager
import os
import sys
from pathlib import Path
from elevate import elevate
import shutil
import time

elevate()

# Define Directories
maindir = "C:/Program Files (x86)/StanleySolutions/KRNC/USBManager/"
utilpath = "C:/ProgramData/StanleySolutions/KRNC/USBManager/"
stockpath = "C:/Users/{}/Music/KRNC/USBManager/"
filterpath = utilpath + 'Filters/'
krncbrandp = utilpath + 'KRNCbranding/'

# Create Required Paths
Path(maindir).mkdir(parents=True, exist_ok=True)
stockpath = stockpath.format(os.getlogin())
Path(krncbrandp).mkdir(parents=True, exist_ok=True)
Path(stockpath).mkdir(parents=True, exist_ok=True)

# Copy Files
try:
    shutil.copytree("SoX", maindir+"/SoX")
except FileExistsError:
    shutil.rmtree(maindir+"/SoX")
    shutil.copytree("SoX", maindir+"/SoX")
try:
    shutil.copytree("Filters", filterpath)
except FileExistsError:
    shutil.rmtree(filterpath)
    shutil.copytree("Filters", filterpath)
    