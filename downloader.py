from __future__ import print_function, unicode_literals
import selenium.common.exceptions as sl_exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from pytube import YouTube, exceptions
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError, ExtractorError
from colored import fg, attr
import warnings
import _paths
import time
import sys
import os

## IGNORE CONSOLE WARNINGS ##
warnings.filterwarnings("ignore", category=DeprecationWarning)

"""
* The code may give error depends on your internet connection. In this case
please increase the wait times where exception throwed.

--> time.sleep("> wait time (seconds) here <")

* Even its a very low possibility, sometimes code could crash in headless mode.
To be sure and prevent this, set headless mode to false. if its needed.

--> self.browserProfile.headless = False
"""

class SpotifyMusicDownloader:

    def __init__ (self):
        ## CHROME OPTIONS ##
        self.service = Service(_paths.driverPath)
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.headless = True # HEADLESS
        self.browserProfile.add_argument("--log-level=3")
        self.browserProfile.add_argument('--lang=en')
        self.browserProfile.add_argument("--disable-notifications")
        self.browserProfile.add_argument('--disable-gpu')
        self.browserProfile.add_argument('--mute-audio')
        self.browserProfile.add_argument('window-size=1920,1080')
        self.browserProfile.add_argument('window-position=0,0')
        self.browserProfile.add_argument("--start-maximized")
        self.browserProfile.add_experimental_option('excludeSwitches',['enable-logging'])
        self.browserProfile.add_experimental_option('prefs',{"intl.accept_languages":"en,en_US"})
        self.browserProfile.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
        self.browserProfile.add_experimental_option('prefs', {"profile.default_content_setting_values.notifications" : "2"})
        ## VERIABLES ##
        self.islinkVerified = False
        self.trackNamesList = []
        self.trackLinks = []
        self.YTDLAudioFormat = 'mp3' # m4a
        self.PYTUBEAudioFormat = '.mp3' # .m4a
        # PATHS
        self.savePath = _paths.savePath
        self.textPath = _paths.textPath
        self.nTextPath = _paths.nTextPath
        self.driverPath = _paths.driverPath

    def executeChrome(self):
        self.browser = webdriver.Chrome(service=self.service, options=self.browserProfile)

    ## SOLO DOWNLOADER START ##
    def soloDownloader(self):
        os.system("cls")

        # CHECK IN
        while self.islinkVerified == False:
            spotifySongLink = str(input('%s\nPASTE THE SONG LINK: %s' % (fg(33), attr(0))))

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

        trackName = self.browser.find_element(By.TAG_NAME, 'h1').text
        try:
            trackArtist = self.browser.find_element(By.XPATH, '//figure/div/img').get_attribute("alt")
            trackLinkResult = trackArtist + " " + trackName
        except sl_exceptions.NoSuchElementException:
            trackArtist = self.browser.find_element(By.XPATH, '//*[@property="og:description"]').get_attribute("content")
            trackArtistSplited = trackArtist.split("· ")
            trackLinkResult = trackArtistSplited[0] + " " + trackName
        
        # YOUTUBE
        self.browser.get(f'https://www.youtube.com/results?search_query={trackLinkResult}')
        trackLink = self.browser.find_element(By.XPATH, '//*[@id="dismissible"]/ytd-thumbnail/a').get_attribute("href")

        os.system("cls")
        print("%s\nDOWNLOADING...\n%s" % (fg(46), attr(0)))

        # DOWNLOAD
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.YTDLAudioFormat,
                'preferredquality': '320',
            }],
            'outtmpl': self.savePath + '/%(title)s.%(ext)s',
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([trackLink])
        except (DownloadError, ExtractorError) :
            print(f"%sSomething went wrong while downloading!%s" % (fg(1), attr(0)))

        os.system('cls')

        print("%s\nSong Downloaded Successfully!\n%s" % (fg(2), attr(0)))
        print(f"%sDestination --> {self.savePath}\n%s" % (fg(1), attr(0)))
        self.islinkVerified = False
        self.browser.close()
    ## SOLO DOWNLOADER END ##

    ## SPOTIFY START ##
    def getSongNamesFromSpotifyPlaylist(self):
        os.system("cls")

        while self.islinkVerified == False:
            spotifyPlayListLink = str(input('%s\nPASTE THE PLAYLIST/ALBUM LINK: %s' % (fg(33), attr(0))))

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

        mainEl = '//*[@id="main"]/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/'
        try: 
            # ALBUM
            totalTrackText = self.browser.find_element(By.XPATH, mainEl + 'div/div[2]/main/section/div[1]/div[5]/div/span[2]').text
        except sl_exceptions.NoSuchElementException:
            # PLAYLIST
            el = mainEl + 'div/div[2]/main/div[1]/section/div[1]/div[5]/div/'

            totalTrackText = self.browser.find_element(By.XPATH, el + 'span[1]').text
            if "like" in totalTrackText:                           
                totalTrackText = self.browser.find_element(By.XPATH, el + 'span[2]').text

        totalTrackSplitedText = str(totalTrackText).split()
        self.totalTrackNum = int(totalTrackSplitedText[0])
        
        self.browser.find_element(By.XPATH,f'//*[@aria-rowindex="1"]').click()

        print(f"%s\nTOTAL SONG: {str(self.totalTrackNum)}\n%s" % (fg(10), attr(0)))

        currentTrackNum = 2
        while currentTrackNum <= self.totalTrackNum+1:
            selectedTrackName = self.browser.find_element(By.XPATH, f'//*[@aria-rowindex="{currentTrackNum}"]/div//a')
            selectedTrackArtist = self.browser.find_element(By.XPATH, f'//*[@aria-rowindex="{currentTrackNum}"]/div/div[2]//span')

            if selectedTrackArtist.text == "E": # prevents explicit content icon
                selectedTrackArtist = self.browser.find_element(By.XPATH, f'//*[@aria-rowindex="{currentTrackNum}"]/div/div[2]/div/span[2]')
            
            print(f"%s[{str(currentTrackNum-1)}/{str(self.totalTrackNum)}] : {selectedTrackArtist.text} : {selectedTrackName.text}%s" % (fg(63), attr(0)))
            resultTrack = selectedTrackArtist.text + " " + selectedTrackName.text  
            self.trackNamesList.append(resultTrack)
            action.key_down(Keys.ARROW_DOWN).perform()
            currentTrackNum+=1
            time.sleep(0.1)
            
        print("%s\nDONE! %s" % (fg(46), attr(0)))
        self.browser.close()
    ## SPOTIFY END ##

    ## YOUTUBE START ##
    def getYoutubeLinks(self):
        self.executeChrome()
        os.system("cls")

        file = open(self.textPath,"w")

        print("%s\n -> Collecting songs from Youtube\n%s" % (fg(1), attr(0)))

        currentTrackNum = 0
        while currentTrackNum < self.totalTrackNum:
            self.browser.get(f'https://www.youtube.com/results?search_query={self.trackNamesList[currentTrackNum]}')
            time.sleep(1)
            trackLink = self.browser.find_element(By.XPATH, '//*[@id="dismissible"]/ytd-thumbnail/a').get_attribute("href")
            print(f"{fg(98)}[{currentTrackNum+1}/{str(self.totalTrackNum)}] : {self.trackNamesList[currentTrackNum]} : {trackLink} {attr(0)}")

            self.trackLinks.append(str(trackLink))

            try:
                file.write(f"{str(currentTrackNum+1)} - {self.trackNamesList[currentTrackNum]} : {trackLink}\n")
            except (UnicodeEncodeError, UnicodeDecodeError):
                file.write(f"{str(currentTrackNum+1)} - Song name cannot specified : {self.trackLinks[currentTrackNum]}\n")

            currentTrackNum+=1
        
        self.browser.close()
        file.close()
    ## YOUTUBE END ##

    ## PYTUBE START ##
    def pytube(self):
        os.system("cls")
        file = open(self.nTextPath,"w")

        currentTrackNum = 0
        while currentTrackNum < self.totalTrackNum:
            yt = YouTube(self.trackLinks[currentTrackNum])

            try:
                video = yt.streams.filter(only_audio=True).first()
            except exceptions.AgeRestrictedError:
                print(f"%s[{currentTrackNum+1}/{str(self.totalTrackNum)}] : {yt.title} : is have age restrict. Cannot download it!%s" % (fg(1), attr(0)))
                try:
                    file.write(f"{str(currentTrackNum+1)} - {self.trackNamesList[currentTrackNum]} : {self.trackLinks[currentTrackNum]}\n")
                except (UnicodeEncodeError, UnicodeDecodeError):
                    file.write(f"{str(currentTrackNum+1)} - Song name cannot specified : {self.trackLinks[currentTrackNum]}\n")
                currentTrackNum+=1
                continue

            out_file = video.download(output_path=self.savePath)
            base, ext = os.path.splitext(out_file)
            new_file = base + self.PYTUBEAudioFormat

            try:
                os.rename(out_file, new_file)
                print(f"%s[{currentTrackNum+1}/{str(self.totalTrackNum)}]: {yt.title} : Downloaded%s" % (fg(99), attr(0)))
            except FileExistsError:
                os.remove(out_file)
                print(f"%s[{currentTrackNum+1}/{str(self.totalTrackNum)}] : {yt.title} Already Downloaded!%s" % (fg(3), attr(0)))
                
            currentTrackNum+=1

        print("%s\nAll Songs Downloaded Successfully!\n%s" % (fg(2), attr(0)))
        print(f"%sDestination --> {self.savePath}\n%s" % (fg(1), attr(0)))
        self.islinkVerified = False
    ## PYTUBE END ##

    ## YT_DLP START ##
    def youtubedl(self):
        
        print("%s\nDownloading Songs... This may take some time.\n%s" % (fg(2), attr(0)))

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.YTDLAudioFormat,
                'preferredquality': '320',
            }],
            'outtmpl': self.savePath + '/%(title)s.%(ext)s',
        }

        currentTrackNum = 0
        while currentTrackNum < self.totalTrackNum:
            link = self.trackLinks[currentTrackNum]
            print(f"%s[{currentTrackNum+1}/{str(self.totalTrackNum)}]: {self.trackNamesList[currentTrackNum]} : Downloading%s" % (fg(99), attr(0)))

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])
            except (DownloadError, ExtractorError) :
                print(f"%s[{currentTrackNum+1}/{str(self.totalTrackNum)}] : {self.trackNamesList[currentTrackNum]} : Something went wrong while downloading!%s" % (fg(1), attr(0)))

            os.system('cls')
            currentTrackNum+=1

        print("%s\nAll Songs Downloaded Successfully!\n%s" % (fg(2), attr(0)))
        print(f"%sDestination --> {self.savePath}\n%s" % (fg(1), attr(0)))
        self.islinkVerified = False
    ## YT_DLP END ##

    ## EXECUTE START ##
    def execute(self,downloadOption):
        self.getSongNamesFromSpotifyPlaylist()
        self.getYoutubeLinks()

        if downloadOption == "1":
            self.pytube()
        elif downloadOption == "2":
            self.youtubedl()
    ## EXECUTE END ##

spmd = SpotifyMusicDownloader()

while True:
    print("")
    print("%s - - - SPOTIFY MUSIC DOWNLOADER - - - %s" % (fg(82), attr(0)))
    opt = input("""%s
    [1] - Download Playlist
    [2] - Download Song
    [3] - Exit \n
    Enter Number: %s""" % (fg(82), attr(0)))
    if opt == "3":
        sys.exit()
    elif opt == "2":
        spmd.soloDownloader()
    elif opt == "1":

        while True:
            dOp = input("""%s 
    Choose a download option:

    [1] - pytube
    [2] - yt_dlp

    Enter Number: %s""" % (fg(105), attr(0)))

            if dOp == "1" or dOp == "2":
                spmd.execute(dOp)
                break
            else:
                print("%s\nPlease enter the correct number%s" % (fg(1), attr(0)))





