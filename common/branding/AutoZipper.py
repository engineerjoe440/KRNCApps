# Automatic Zipper File

import os
import zipfile

# Zip Files
def zipdir(path, ziph, extpath=''):
    for file in os.listdir(path):
        if file.endswith('.mp3'):
            # Collect all Imaging Files
            ziph.write(os.path.join(extpath, file))

# Run Main Operation
if __name__ == '__main__':
    zipf = zipfile.ZipFile('KrncBranding.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('.', zipf)
    zipf.close()
