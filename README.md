# Download your spotify playlist or just spesific tracks as a mp3 file without any key or token requirements.

## Requirements

###  Pip's
Selenium
    
    pip install selenium

Colored 

    pip install colored
    
Pytube

    pip install pytube
### Chrome Driver
    
 Current Chrome Driver version: 96
 
 Download the latest [Chrome Driver](https://chromedriver.chromium.org/downloads). It must be the same version of Chome with in your computer.
 Add chromedriver.exe to in "driver" folder.
 
## Usage

Run the "downloader.py", choose prefered download option and paste your spotify playlist/song link. Yeah, that's all.
    
## Notes

- The names of the tracks and youtube links are will be collected in a text file.
- Downloaded tracks will be appear in downloads folder. 

#### If you want to change the folder paths, you have to define your own paths in code file.

        self.savePath = 'SpotifyPlaylistDownloader\Downloads'
        self.textPath = 'SpotifyPlaylistDownloader\musiclinklist.txt'
        self.driverPath = 'driver/chromedriver.exe'

## Console look

![console look](https://i.ibb.co/znCymsc/Ekran-g-r-nt-s-2021-12-26-140751.png)
