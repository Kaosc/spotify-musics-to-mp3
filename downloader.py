from __future__ import print_function, unicode_literals
import warnings
import _paths
import time
import sys
import os

from selenium import webdriver
import selenium.common.exceptions as sl_exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from yt_dlp import YoutubeDL
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, ExtractorError
from colored import fg, attr

## IGNORE CONSOLE WARNINGS ##
warnings.filterwarnings("ignore", category=DeprecationWarning)

class SpotifyMusicDownloader:

    def __init__(self):
        ## CHROME OPTIONS ##
        self.service = Service(_paths.driverPath)
        self.browserProfile = webdriver.ChromeOptions()

        self.browserProfile.add_argument("--headless=old") # HEADLESS
        self.browserProfile.add_argument("--log-level=3")
        self.browserProfile.add_argument("--lang=en")
        self.browserProfile.add_argument("--disable-notifications")
        self.browserProfile.add_argument("--disable-gpu")
        self.browserProfile.add_argument("--mute-audio")
        self.browserProfile.add_argument("window-size=1920,1080")
        self.browserProfile.add_argument("window-position=0,0")
        self.browserProfile.add_argument("--start-maximized")
        self.browserProfile.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.browserProfile.add_experimental_option("prefs", {"intl.accept_languages": "en,en_US"})
        self.browserProfile.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
        self.browserProfile.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": "2"})

        ## VERIABLES ##
        self.islinkVerified = False
        self.trackNamesList = []
        self.trackLinks = []
        self.YTDLAudioFormat = "mp3"
        self.bitrate = "320"

        # PATHS
        self.savePath = _paths.savePath
        self.textPath = _paths.textPath
        self.nTextPath = _paths.nTextPath
        self.driverPath = _paths.driverPath

        # YT-DLP Options
        self.ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": self.YTDLAudioFormat, "preferredquality": self.bitrate}],
            "outtmpl": self.savePath + "/%(title)s.%(ext)s",
        }

    def executeChrome(self):
        self.browser = webdriver.Chrome(service=self.service, options=self.browserProfile)

    def soloDownloader(self):
        os.system("cls")

        # CHECK IN
        while self.islinkVerified == False:
            spotifySongLink = str(input("%s\nPASTE THE SONG LINK: %s" % (fg(33), attr(0))))

            if "https://open.spotify.com/track" in spotifySongLink:
                self.islinkVerified = True
            elif "https://open.spotify.com/playlist" in spotifySongLink:
                print("%s\nThis is a playlist link! If you want to download a playlist, try the option 1%s" % (fg(1), attr(0)))
            elif "https://open.spotify.com/album" in spotifySongLink:
                print("%s\nThis is an album link! If you want to download an album, try the option 1%s" % (fg(1), attr(0)))
            else:
                print("%s\nSomething wrong with the link. Please be sure it's a valid link.\n%s" % (fg(1), attr(0)))

        self.executeChrome()
        os.system("cls")

        print("%s\nGETTING SONG NAME...\n%s" % (fg(46), attr(0)))

        # SPOTIFY
        self.browser.get(spotifySongLink)

        time.sleep(2)

        trackName = self.browser.find_element(By.TAG_NAME, "h1").text
        try:
            trackArtist = self.browser.find_element(By.XPATH, "//figure/div/img").get_attribute("alt")
            trackLinkResult = trackArtist + " " + trackName
        except sl_exceptions.NoSuchElementException:
            trackArtist = self.browser.find_element(By.XPATH, '//*[@property="og:description"]').get_attribute("content")
            trackArtistSplited = trackArtist.split("· ")
            trackLinkResult = trackArtistSplited[0] + " " + trackName

        # YOUTUBE
        self.browser.get(f"https://www.youtube.com/results?search_query={trackLinkResult}")
        trackLink = self.browser.find_element(By.XPATH, '//*[@id="dismissible"]/ytd-thumbnail/a').get_attribute("href")

        os.system("cls")
        print("%s\nDOWNLOADING...\n%s" % (fg(46), attr(0)))

        try:
            with YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([trackLink])
        except (DownloadError, ExtractorError):
            print(f"%sSomething went wrong while downloading!%s" % (fg(1), attr(0)))

        os.system("cls")

        print("%s\nSong Downloaded Successfully!\n%s" % (fg(2), attr(0)))
        print(f"%sDestination --> {self.savePath}\n%s" % (fg(1), attr(0)))
        self.islinkVerified = False
        self.browser.close()

    def getSongNamesFromSpotifyPlaylist(self):
        os.system("cls")

        while self.islinkVerified == False:
            spotifyPlayListLink = str(input("%s\nPASTE THE PLAYLIST/ALBUM LINK: %s" % (fg(33), attr(0))))

            if "https://open.spotify.com/playlist" in spotifyPlayListLink:
                self.islinkVerified = True
            elif "https://open.spotify.com/album" in spotifyPlayListLink:
                self.islinkVerified = True
            elif "https://open.spotify.com/track" in spotifyPlayListLink:
                print("%s\nThis is not a playlist link. If you want to download just one track, try the option 2%s" % (fg(1), attr(0)))
            else:
                print("%s\nSomething wrong with this link. Please be sure it's a valid link.\n%s" % (fg(46), attr(0)))

        self.executeChrome()
        action = webdriver.ActionChains(self.browser)
        os.system("cls")

        print("%s\nCollecting songs from Spotify\n%s" % (fg(46), attr(0)))

        self.browser.get(spotifyPlayListLink)
        self.browser.back()
        self.browser.get(spotifyPlayListLink)

        time.sleep(3)

        playListPageMainEl = '//*[@data-testid="playlist-page"]'
        albumPageMainEl = '//*[@data-testid="album-page"]'
        isPlaylist = True
        
        # Check is it playlist or album page
        try:
            self.browser.find_element(By.XPATH, playListPageMainEl)
        except sl_exceptions.NoSuchElementException:
            isPlaylist = False

        # Get total track text
        if isPlaylist:
            el = playListPageMainEl + "/div/div[3]/div[3]/div/div[2]/"
            totalTrackText = self.browser.find_element(By.XPATH, el + "span[1]").text

            # If total track is not a "like" text
            if "like" in totalTrackText:
                totalTrackText = self.browser.find_element(By.XPATH, el + "span[2]").text
        else:
            # Check is Album or Single
            try:
                totalTrackText = self.browser.find_element(By.XPATH, albumPageMainEl + "/div/div[3]/div[2]/div/div[2]/span").text
            except sl_exceptions.NoSuchElementException:
                totalTrackText = self.browser.find_element(By.XPATH, albumPageMainEl + "/div/div[3]/div[2]/div/div/span").text


        # Get total track number
        totalTrackSplitedText = str(totalTrackText).split()
        self.totalTrackNum = int(totalTrackSplitedText[0])

        self.browser.find_element(By.XPATH, f'//*[@aria-rowindex="1"]').click()

        print(f"%s\nTOTAL SONG: {str(self.totalTrackNum)}\n%s" % (fg(10), attr(0)))

        currentTrackNum = 2
        while currentTrackNum <= self.totalTrackNum + 1:
            selectedTrackName = self.browser.find_element(By.XPATH, f'//*[@aria-rowindex="{currentTrackNum}"]/div//a')
            selectedTrackArtist = self.browser.find_element(By.XPATH, f'//*[@aria-rowindex="{currentTrackNum}"]/div/div[2]//span')

            if selectedTrackArtist.text == "E":  # prevents explicit content icon
                selectedTrackArtist = self.browser.find_element(By.XPATH, f'//*[@aria-rowindex="{currentTrackNum}"]/div/div[2]/div/span[2]')

            print(f"%s[{str(currentTrackNum-1)}/{str(self.totalTrackNum)}] : {selectedTrackArtist.text} : {selectedTrackName.text}%s" % (fg(63), attr(0)))
            resultTrack = selectedTrackArtist.text + " " + selectedTrackName.text
            self.trackNamesList.append(resultTrack)
            action.key_down(Keys.ARROW_DOWN).perform()
            currentTrackNum += 1
            time.sleep(0.1)

        print("%s\nDONE! %s" % (fg(46), attr(0)))
        self.browser.close()

    def getYoutubeLinks(self):
        self.executeChrome()
        os.system("cls")

        file = open(self.textPath, "w")

        print("%s\n -> Collecting songs from Youtube\n%s" % (fg(1), attr(0)))

        currentTrackNum = 0
        while currentTrackNum < self.totalTrackNum:
            self.browser.get(f"https://www.youtube.com/results?search_query={self.trackNamesList[currentTrackNum]}")
            time.sleep(1)
            trackLink = self.browser.find_element(By.XPATH, '//*[@id="dismissible"]/ytd-thumbnail/a').get_attribute("href")
            print(f"{fg(98)}[{currentTrackNum+1}/{str(self.totalTrackNum)}] : {self.trackNamesList[currentTrackNum]} : {trackLink} {attr(0)}")

            self.trackLinks.append(str(trackLink))

            try:
                file.write(f"{str(currentTrackNum+1)} - {self.trackNamesList[currentTrackNum]} : {trackLink}\n")
            except (UnicodeEncodeError, UnicodeDecodeError):
                file.write(f"{str(currentTrackNum+1)} - Song name cannot specified : {self.trackLinks[currentTrackNum]}\n")

            currentTrackNum += 1

        self.browser.close()
        file.close()

    def youtubedl(self):

        print("%s\nDownloading Songs... This may take some time.\n%s" % (fg(2), attr(0)))

        currentTrackNum = 0
        while currentTrackNum < self.totalTrackNum:
            link = self.trackLinks[currentTrackNum]
            print(f"%s[{currentTrackNum+1}/{str(self.totalTrackNum)}]: {self.trackNamesList[currentTrackNum]} : Downloading%s" % (fg(99), attr(0)))

            try:
                with YoutubeDL(self.ydl_opts) as ydl:
                    ydl.download([link])
            except (DownloadError, ExtractorError):
                print(f"%s[{currentTrackNum+1}/{str(self.totalTrackNum)}] : {self.trackNamesList[currentTrackNum]} : Something went wrong while downloading!%s" % (fg(1), attr(0)))

            os.system("cls")
            currentTrackNum += 1

        print("%s\nAll Songs Downloaded Successfully!\n%s" % (fg(2), attr(0)))
        print(f"%sDestination --> {self.savePath}\n%s" % (fg(1), attr(0)))
        self.islinkVerified = False

    def execute(self):
        self.getSongNamesFromSpotifyPlaylist()
        self.getYoutubeLinks()
        self.youtubedl()

        # Cleanup
        self.trackLinks = []
        self.trackNamesList = []
        self.islinkVerified = False


spmd = SpotifyMusicDownloader()

while True:
    print("")
    print("%s - - - SPOTIFY MUSIC DOWNLOADER - - - %s" % (fg(82), attr(0)))
    opt = input(
        """%s
    [1] - Download Playlist/Album
    [2] - Download Song
    [3] - Exit \n
    Enter Number: %s"""
        % (fg(82), attr(0))
    )
    if opt == "3":
        sys.exit()
    elif opt == "2":
        spmd.soloDownloader()
    elif opt == "1":
        spmd.execute()
