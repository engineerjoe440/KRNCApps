# KRNC Universal Song Barn Manager <a href="https://github.com/engineerjoe440/KRNCApps"><img src="https://github.com/engineerjoe440/KRNCApps/blob/master/common/images/KRNC.png" width="100" alt="KRNC" align="right"></a>

*USB Flash Drive Audio Manager for Mobile and Vehicle Playback*

---

This folder is dedicated to the application known as the Universal Song Barn Manager
which is designed to manage the filtering and audio compression for audio files that
should be loaded onto a USB flash drive for playback in vehicle sound systems. Such
drives can easily be managed with this tool to update and change the available
playlist.

Originally intended to function solely as a Windows application, this design is now
intended to be cross-platform-compatible between Windows and Linux environments where
TK graphics are supported. Eventually, with luck this app will be released into
Linux package managers/software stores and on PyPI for direct source installation.
Right now, the app can only be installed by way of cloning this repository.

### Development Installation:
- clone repository to a desired location (e.g., (`C:`)`/<my-folder-path>/usbmanager`)
- `cd` to the new directory (e.g., `cd <my-folder-path>/usbmanager`)
- use *pip* to install:
  - on Windows: `> pip install .`
  - on Linux: `$ pip3 install .` *this is because Python2 is not supported*
- run the app! `KrncUsbManager`

### Standard Compressor:
According to an interesting article [here](https://medium.com/@jud.dagnall/dynamic-range-compression-for-audio-with-ffmpeg-and-compand-621fe2b1a892)
it seems that the following ffmpeg command may work nicely!
`ffmpeg -i in.mp3 -filter_complex "compand=attacks=0:points=-80/-900|-45/-15|-27/-9|0/-7|20/-7:gain=5" out.mp3`

---

*KRNC - Welcome Home.*

---


    
---

### Brief History
KRNC, a ficticious broadcast radio station is a radio station for everyone, it is
everyone's own station. "Your music lives here," the musical positioning statement
for the station.

The station call-letters (KRNC) are derived as follows:
 - K: The "West-Coast" signifier used by all radio stations west of the Mississippi River
 - RNC: The "prominent" and "leading" consonants of the word "RaNCh"

The station name, call letters, and phrases were developed by Joe Stanley (Stanley
Solutions Owner) in 2015 and have led the KRNC branding scheme since.

---
© 2020 - Stanley Solutions
