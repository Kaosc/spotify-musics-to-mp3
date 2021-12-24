from __future__ import print_function, unicode_literals
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from pytube import YouTube
from colored import fg, attr
import warnings
import time
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

        self.trackNamesList = []
        self.trackLinks = []

        # Paths
        self.savePath = 'spotify-playlist-downloader\Downloads'            # <------ download path goes here
        self.textPath = 'spotify-playlist-downloader\musiclinklist.txt'    # <------ text file path goes here
        self.driverPath = 'driver/chromedriver.exe'                        # <------ driver path goes here   

    def getSongNamesFromSpotifyPlaylist(self):
        os.system("cls")
        spotifyPlayListLink = str(input('Paste the playlist link: '))

        self.browser = webdriver.Chrome(self.driverPath, chrome_options=self.browserProfile)
        action = webdriver.ActionChains(self.browser)
        os.system("cls")

        print("%s\nCollecting songs from Spotify\n%s" % (fg(46), attr(0)))

        self.browser.get(spotifyPlayListLink)
        self.browser.back()
        self.browser.get(spotifyPlayListLink)

        time.sleep(3)

        totalTrackText = self.browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[1]/div[5]/div/span').text

        if "like" in totalTrackText:
            totalTrackText = self.browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[1]/div[5]/div/span[2]').text
        totalTrackSplitedText = str(totalTrackText).split()
        self.totalTrackNum = int(totalTrackSplitedText[0])
        
        self.browser.find_element_by_xpath(f'//*[@aria-rowindex="1"]').click()

        currentTrackNum = 2
        while currentTrackNum <= self.totalTrackNum+1:
            selectedTrackName = self.browser.find_element_by_xpath(f'//*[@aria-rowindex="{currentTrackNum}"]/div/div[2]/div/div')
            selectedTrackArtist = self.browser.find_element_by_xpath(f'//*[@aria-rowindex="{currentTrackNum}"]/div/div[2]/div/span')

            if selectedTrackArtist.text == "E": # prevents explicit content icon
                selectedTrackArtist = self.browser.find_element_by_xpath(f'//*[@aria-rowindex="{currentTrackNum}"]/div/div[2]/div/span[2]')
            
            print(f"%s{str(currentTrackNum-1)} : {selectedTrackArtist.text} : {selectedTrackName.text}%s" % (fg(63), attr(0)))
            resultTrack = selectedTrackArtist.text + " " + selectedTrackName.text  
            self.trackNamesList.append(resultTrack)
            action.key_down(Keys.ARROW_DOWN).perform()
            currentTrackNum+=1
            time.sleep(0.1)
            
        print("%s\nDONE! %s" % (fg(46), attr(0)))
        print(f"%s\nTOTAL SONG: {len(self.trackNamesList)}%s" % (fg(10), attr(0)))
        self.browser.close()

    def getYoutubeLinks(self):
        self.browser = webdriver.Chrome(self.driverPath, chrome_options=self.browserProfile)
        file = open(self.textPath,"w")

        os.system("cls")

        print("%s\n -> Collecting songs from Youtube\n%s" % (fg(46), attr(0)))

        currentTrackNum = 0
        while currentTrackNum < self.totalTrackNum:
            self.browser.get(f'https://www.youtube.com/results?search_query={self.trackNamesList[currentTrackNum]}')
            trackLink = self.browser.find_element_by_xpath('//*[@id="dismissible"]/ytd-thumbnail/a').get_attribute("href")
            print(f"%s{currentTrackNum+1} : {self.trackNamesList[currentTrackNum]} : {trackLink} %s" % (fg(98), attr(0)))
            self.trackLinks.append(str(trackLink))
            file.write(f"{str(currentTrackNum+1)} {self.trackNamesList[currentTrackNum]} : {trackLink}\n")
            currentTrackNum+=1
        
        self.browser.close()
        file.close()

    def download(self):
        os.system("cls")

        currentTrackNum = 0
        while currentTrackNum < self.totalTrackNum:
            yt = YouTube(self.trackLinks[currentTrackNum])
            
            video = yt.streams.filter(only_audio=True).first()

            out_file = video.download(output_path=self.savePath)

            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'

            try:
                os.rename(out_file, new_file)
                print(f"%s{currentTrackNum+1} : {yt.title} : Downloaded%s" % (fg(99), attr(0)))
            except FileExistsError:
                os.remove(out_file)
                print(f"%s{currentTrackNum+1} : {yt.title} Already Downloaded!%s" % (fg(3), attr(0)))
                
            currentTrackNum+=1

        print("%s\nAll Songs Downloaded Successfully!\n%s" % (fg(2), attr(0)))
        print(f"%sDirectory --> {self.savePath}\n%s" % (fg(1), attr(0)))

    def execute(self):
        self.getSongNamesFromSpotifyPlaylist()
        self.getYoutubeLinks()
        self.download()

spmd = SpotifyMusicDownloader()
spmd.execute()

