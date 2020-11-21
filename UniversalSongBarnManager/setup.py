# Import Necessary Files
import setuptools

# Load Description Document
with open("README.md", "r") as fh:
    long_description = fh.read()

# Generate Setup Tools Argument
setuptools.setup(
    name='KrncUsbManager',
    version='0.0',
    author="Joe Stanley",
    author_email="engineerjoe440@yahoo.com",
    description="KRNC Universal Song Barn (USB) Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/engineerjoe440/KRNCApps/tree/master/UniversalSongBarnManager",
    packages=['KrncUsbManager',],
    package_data={'': ['images/*.png']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
        "Operating System :: Linux",
    ],
    project_urls={
        "Source Repository": "https://github.com/engineerjoe440/KRNCApps",
    },
    entry_points = {
        'console_scripts': ['KrncUsbManager=KrncUsbManager.__main__:main'],
    }
)