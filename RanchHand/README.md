# KRNC Ranch Hand <a href="https://github.com/engineerjoe440/KRNCApps"><img src="https://github.com/engineerjoe440/KRNCApps/blob/master/common/images/KRNC.png" width="100" alt="KRNC" align="right"></a>

*VirtualDJ Database, Settings, Playlist, and Information Manager*

---

This folder is dedicated to the application known as the Ranch Hand which is
designed to manage the database (.xml) and related settings files used by VirtualDJ
software in order to appropriately manage sharing settings and configuration across
multiple personal computers.

---

*KRNC - Welcome Home.*

---

Ranch Hand utilizes both a user interface and Windows service to perform the actions
necessry to synchronize the settings across multiple machines. Ranch Hand requires a
shared cloud file service such as OneDrive or GoogleDrive with files stored locally
on the machine to manage appropriate synchronization.

Ranch Hand relies upon a file structure as shown below to manage files appropriately,
and as such, the installer will perform the folder construction that is required.

```
 C:\
  ├─── ProgramData
  │    └─── StanleySolutions
  │         └─── KRNC
  │              └─── RanchHand
  │                   └── config.ini
  │
  ├─── Program Files (x86)
       └─── StanleySolutions
            └─── KRNC
                 └─── RanchHand
                      ├─── RanchHand.exe
                      ├─── RanchHandService.exe
                      │
                      └─── images
                           ├─── help.png
                           ├─── KRNC.png
                           ├─── KRNCnegative.png
                           ├─── KRNC.ico
                           └─── KRNCnegative.ico
```

The Ranch Hand management app is accessible from the system tray and supports a
small set of settings that describe the location of the three primary folder
locations of interest. These three folders are the local VirtualDJ folder, the
remote (cloud-drive folder) VirtualDJ folder, and the cloud-drive folder where
music files (*.mp3, *.wav, etc.) are stored.

<img src="https://github.com/engineerjoe440/KRNCApps/blob/master/common/images/RanchHandApp.png">

The application provides methods to directly pull all settigns from the remote
folder location, and push settings from the local VirtualDJ folder. Additionally,
the application allows the user to save configuration which restarts the
associated Windows service.

The Windows service associated with the KRNC Ranch Hand is accessible through the
Windows system tray with the KRNC icon. From this tray icon, the management app
can be opened and the service can be stopped as well.

## Control Features
As mentioned, a couple control options are available for configuration with the
graphical RanchHand application. These options are described in the detailed table
below.

| Control Feature       | Description                                                                                                                                                          | Automated Service Restart? |
|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|
| Save Configuration    | Saves the configured directory locations, restarts the RanchHand service to appropriately monitor for changes.                                                       | Yes                        |
| Push VDJ Settings Now | Push the VirtualDJ settings from the local storage folder to the remote cloud drive service folder with generic string replacement.                                  | No, not needed             |
| Pull VDJ Settings Now | Pull the VirtualDJ settings from the remote cloud service folder to the local storage folder replacing generic strings with the appropriate local folder references. | No, not needed             |

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
