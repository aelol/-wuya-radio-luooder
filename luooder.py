# ae.h - 2017/10/22
# coding=utf-8

import re
import requests
import time
from bs4 import BeautifulSoup

LUOO_URL = "http://www.luoo.net/vol/index/{}"
MP3_URL = "http://mp3-cdn2.luoo.net/low/{}/{}.mp3"

TRACK_NAME = "{} -{}.mp3"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_song_list(volumn):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    r = requests.get(LUOO_URL.format(volumn), headers=headers)
    r.encoding = 'utf-8'

    bs = BeautifulSoup(r.content, 'html.parser')
    songs = bs.find_all('div', 'player-wrapper')

    print(bcolors.OKBLUE + "song list of volumn {}:".format(volumn) + bcolors.ENDC)
    result = []
    for song in songs:
        meta = {'name': song.find('p', 'name').getText(), 'artist': song.find('p', 'artist').getText()[7:],
                'album': song.find('p', 'album').getText()[6:]}
        print(bcolors.UNDERLINE + '{} by {}'.format(meta['name'], meta['artist']) + bcolors.ENDC)
        result.append(meta)

    return result


def download_songs_list(volumn):
    songs = get_song_list(volumn)
    if len(songs) == 0:
        print(bcolors.WARNING + 'please make sure the volumn exists in luoo.net' + bcolors.ENDC)
        return

    print(bcolors.OKBLUE + 'downloading...' + bcolors.ENDC)
    index = 0
    with open('tracks_list.txt', 'w') as f:

        for song in songs:
            track = song['name']
            track = re.findall(r'\.(.+?)\s', track)
            url = MP3_URL.format('wuya', track[0])
            f.write(url + '\n')
        f.close()


# download songs via requests.get(for url in txt.readlines)

if __name__ == '__main__':

    while True:
        # print(bcolors.HEADER + "input the volumn number to download all songs within it!\n>" + bcolors.ENDC)
        print(bcolors.HEADER + "vol == 541, wuya radio at luoo, will start in 2s\n" + bcolors.ENDC)
        time.sleep(2)
        # vol = input()
        vol = 541
        if str(vol).isdigit():
            print(bcolors.BOLD + 'initiating...' + bcolors.ENDC)
            download_songs_list(vol)
            break
