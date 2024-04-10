import json
import asyncio
import requests
from jiosaavn import JioSaavn

saavn = JioSaavn()

async def search(song):
    songlist = []
    data = await saavn.search_songs(song)
    for songDetail in data['data']:
        url = await saavn.get_song_direct_link(songDetail['url'])
        audio = requests.get(url)
        songdoc = {
            "title" : songDetail['title'],
            "image": songDetail['image'],
            "audio": audio.url,
            "url": audio,
            "description": songDetail['description']
        }
        songlist.append(songdoc)
    return songlist

# async def main(text):
#     result = await search(text)
#     for item in result:
#         print(item["url"])

# asyncio.run(main())