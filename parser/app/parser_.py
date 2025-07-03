from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from yt_dlp import YoutubeDL

import csv
import time
import os
from pathlib import PurePath


class Parser:
    current_channel_index = int()

    @staticmethod
    def read_channels() -> list:
        with open(PurePath('data', 'channels.txt'), 'r', encoding='utf-8') as file:
            return file.readlines()
        
    @staticmethod
    def read_videos() -> list:
        with open(PurePath('data', 'vlinks.csv'), 'r', encoding='utf-8') as file:
            return [x for x in csv.reader(file)]
    
    @staticmethod
    def write_videos(videos: list):
        with open(PurePath('data', 'vlinks.csv'), 'w', encoding='utf-8') as file:
            csv.writer(file).writerows(videos)

    @staticmethod
    def video_filter(info, *, incomplete):
        duration = info.get('duration')
        if duration and duration > 240:
            return 'Too long'

    @staticmethod
    def collect_videos(channel: str, limit: int) -> list:
        driver = webdriver.Remote(command_executor='http://selenium_hub:4444/wd/hub', options=Options())
        driver.get(channel)

        collected_links = list()

        counter = 0

        while counter != limit:
            for el in driver.find_elements(By.TAG_NAME, 'a'):
                

                if el.get_attribute('href'):
                    el_href = el.get_attribute('href')
                else:
                    continue

                if '/watch?v=' in el_href and [el_href, 'free'] not in collected_links:
                    collected_links.append([el_href, 'free'])

            counter += 1  
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

            time.sleep(0.5)

        driver.quit()
        return collected_links
    
    @classmethod
    def get_video(cls) -> str:
        videos = cls.read_videos()

        if not videos:
            videos = cls.collect_videos(channel=cls.read_channels()[cls.current_channel_index], limit=10)
            cls.write_videos(videos=videos)

        while True:
            for video in videos:
        
                if video[1] != 'expiry':
                    
                    ydl_opts = {
                        'cookiefile': 'data/cookies.txt',
                        'match_filter': cls.video_filter,
                        'outtmpl': f'data/video.mp4',
                        'format': 'best',
                        'quiet': True,
                    }

                    with YoutubeDL(ydl_opts) as ydl:
                        if ydl.download([video[0]]):
                            video[1] = 'expiry'
                            cls.write_videos(videos=videos)
                            continue
                    
                    with open('data/video.mp4', 'rb') as file:
                        video_bytes = file.read()
                    
                    os.remove('data/video.mp4')

                    video[1] = 'expiry'
                    cls.write_videos(videos=videos)
                    return video_bytes
        
            cls.current_channel_index += 1 
            if cls.current_channel_index > 5: cls.current_channel_index = 0
            
            videos = cls.collect_videos(channel=cls.read_channels()[cls.current_channel_index], limit=20)

            cls.write_videos(videos=videos)