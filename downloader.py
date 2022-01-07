from __future__ import print_function, unicode_literals
import selenium.common.exceptions as sl_exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from pytube import exceptions
from pytube import YouTube
import youtube_dl
from colored import fg, attr
import warnings
import _paths
import time
import sys
import os

warnings.filterwarnings("ignore", category=DeprecationWarning)

class SpotifyMusicDownloader:

    def __init__ (self):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.headless = True
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

    def soloDownloader(self):
        os.system("cls")

        while self.islinkVerified == False:
            spotifySongLink = str(input('%s\nPASTE THE PLAYLIST LINK: %s' % (fg(33), attr(0))))

            if "https://open.spotify.com/track" in spotifySongLink:
                self.islinkVerified = True
            elif "https://open.spotify.com/playlist" in spotifySongLink:
                print("%s\nThis is a playlist link! If you want to download a playlist, try the option 1%s" % (fg(1), attr(0)))
            else:
                print("%s\nSomething wrong with the link. Please try again.\n%s" % (fg(1), attr(0)))

        self.browser = webdriver.Chrome(self.driverPath, chrome_options=self.browserProfile)
        os.system("cls")

        print("%s\nGETTING SONG NAME...\n%s" % (fg(46), attr(0)))

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

        self.browser.get(f'https://www.youtube.com/results?search_query={trackLinkResult}')
        trackLink = self.browser.find_element(By.XPATH, '//*[@id="dismissible"]/ytd-thumbnail/a').get_attribute("href")

        os.system("cls")
        print("%s\nDOWNLOADING...\n%s" % (fg(46), attr(0)))

        yt = YouTube(trackLink)

        try:
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path=self.savePath)
            base, ext = os.path.splitext(out_file)
            new_file = base + self.AudioFormat

            os.system("cls")

            try:
                os.rename(out_file, new_file)
                print(f"%s{yt.title} : Downloaded%s" % (fg(99), attr(0)))
            except FileExistsError:
                os.remove(out_file)
                print(f"%s{yt.title} Already Downloaded!%s" % (fg(3), attr(0)))

            print("%s\nSong Downloaded Successfully!\n%s" % (fg(2), attr(0)))
            print(f"%sDirectory --> {self.savePath}\n%s" % (fg(1), attr(0)))
        except exceptions.AgeRestrictedError:
            print(f"%s{yt.title} is have age restrict. Cannot download it!%s" % (fg(1), attr(0)))

        self.islinkVerified = False

    def getSongNamesFromSpotifyPlaylist(self):
        os.system("cls")

        while self.islinkVerified == False:
            spotifyPlayListLink = str(input('%s\nPASTE THE PLAYLIST LINK: %s' % (fg(33), attr(0))))

            if "https://open.spotify.com/playlist" in spotifyPlayListLink:
                self.islinkVerified = True
            elif "https://open.spotify.com/track" in spotifyPlayListLink:
                print("%s\nThis is not a playlist link. If you want to download just one track, try the option 2%s" % (fg(1), attr(0)))
            else:
                print("%s\nSomething wrong with the link. Please try again.\n%s" % (fg(46), attr(0)))

        self.browser = webdriver.Chrome(self.driverPath, chrome_options=self.browserProfile)
        action = webdriver.ActionChains(self.browser)
        os.system("cls")

        print("%s\nCollecting songs from Spotify\n%s" % (fg(46), attr(0)))

        self.browser.get(spotifyPlayListLink)
        self.browser.back()
        self.browser.get(spotifyPlayListLink)

        time.sleep(3)

        totalTrackText = self.browser.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[1]/div[5]/div/span').text
        if "like" in totalTrackText:
            totalTrackText = self.browser.find_element(By.XPATH,'//*[@id="main"]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[1]/div[5]/div/span[2]').text
        
        totalTrackSplitedText = str(totalTrackText).split()
        self.totalTrackNum = int(totalTrackSplitedText[0])
        
        self.browser.find_element(By.XPATH,f'//*[@aria-rowindex="1"]').click()

        print(f"%s\nTOTAL SONG: {str(self.totalTrackNum)}\n%s" % (fg(10), attr(0)))

        currentTrackNum = 2
        while currentTrackNum <= self.totalTrackNum+1:
            selectedTrackName = self.browser.find_element(By.XPATH, f'//*[@aria-rowindex="{currentTrackNum}"]/div/div[2]/div/div')
            selectedTrackArtist = self.browser.find_element(By.XPATH, f'//*[@aria-rowindex="{currentTrackNum}"]/div/div[2]/div/span')

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

    def getYoutubeLinks(self):
        self.browser = webdriver.Chrome(self.driverPath, chrome_options=self.browserProfile)
        os.system("cls")

        file = open(self.textPath,"w")

        print("%s\n -> Collecting songs from Youtube\n%s" % (fg(1), attr(0)))

        currentTrackNum = 0
        while currentTrackNum < self.totalTrackNum:
            self.browser.get(f'https://www.youtube.com/results?search_query={self.trackNamesList[currentTrackNum]}')
            trackLink = self.browser.find_element(By.XPATH, '//*[@id="dismissible"]/ytd-thumbnail/a').get_attribute("href")
            print(f"%s[{currentTrackNum+1}/{str(self.totalTrackNum)}] : {self.trackNamesList[currentTrackNum]} : {trackLink} %s" % (fg(98), attr(0)))
            self.trackLinks.append(str(trackLink))

            try:
                file.write(f"{str(currentTrackNum+1)} - {self.trackNamesList[currentTrackNum]} : {trackLink}\n")
            except (UnicodeEncodeError, UnicodeDecodeError):
                file.write(f"{str(currentTrackNum+1)} - Song name cannot specified : {self.trackLinks[currentTrackNum]}\n")

            currentTrackNum+=1
        
        self.browser.close()
        file.close()

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
        print(f"%sDirectory --> {self.savePath}\n%s" % (fg(1), attr(0)))
        self.islinkVerified = False

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

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            os.system('cls')
            currentTrackNum+=1

        print("%s\nAll Songs Downloaded Successfully!\n%s" % (fg(2), attr(0)))
        print(f"%sDirectory --> {self.savePath}\n%s" % (fg(1), attr(0)))
        self.islinkVerified = False

    def execute(self,downloadOption):
        self.getSongNamesFromSpotifyPlaylist()
        self.getYoutubeLinks()

        if downloadOption == "1":
            self.pytube()
        elif downloadOption == "2":
            self.youtubedl()

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
    Choose A Download Opiton

    [1] - pytube [Fast / It may give a reading error on some devices.]
    [2] - youtube_dl [It may be slow. Pretty much compatible with all devices.]

    Enter Number: %s""" % (fg(105), attr(0)))

            if dOp == "1" or dOp == "2":
                spmd.execute(dOp)
                break
            else:
                print("%s\nPlease enter the correct number%s" % (fg(1), attr(0)))
                






