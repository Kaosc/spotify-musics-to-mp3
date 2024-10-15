# Spotify MP3 Downloader

## Preview

![overview](./assets/overview.gif)

## Requirements

## 1. Python Dependencies

```bash
pip install selenium colored yt-dlp
```

or run the `dep-installer.py` file.

## 2. Setting Up Chrome Driver

The current version of ChromeDriver in this repository is **129**. To ensure compatibility, please check for the latest ChromeDriver version [here](https://googlechromelabs.github.io/chrome-for-testing/).

If a newer version is available:
1. Download the latest ChromeDriver.
2. Replace the existing file in the `driver` folder with the newly downloaded version.

**Note**: If you don't have Chrome installed on your system, make sure to install it before proceeding.

ChromeDriver version must be the same chrome version installed on your system. You can check your installed chrome version via Settings > About Chrome.

## 3. Installing FFmpeg 

To order to use "yt-dlp" (it's a library for downloading youtube videos, audio, etc.) you need to install FFmpeg.

#### Installing FFmpeg

Download Link: <https://www.ffmpeg.org/download.html>

#### Installation for Windows

If you have chocolatey installed, you can simply install ffmpeg by running the following command:

    choco install ffmpeg

## Usage

Run the "downloader.py", choose prefered download option and paste your spotify playlist/song link. Yeah, that's all.

## Additional Notes

- The names of the tracks and youtube links are will be collected in a text file.
- Downloaded tracks will be appear in downloads folder.
- If you want to change the folder paths, you have to define your own paths in \_paths file:

```py
savePath = 'Downloads'
textPath = 'Texts/downloaded-links.txt'
nTextPath = 'Texts/skipped-links.txt'
driverPath = 'driver/chromedriver.exe'
```

## Console Look

![console look](./assets/console.png)

## Links to the repositories of the libraries used in this tool

- [Selenium](https://github.com/SeleniumHQ/Selenium)
- [Colored](https://gitlab.com/dslackw/colored)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
