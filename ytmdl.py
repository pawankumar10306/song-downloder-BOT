import requests
import json

search_url = "https://apis.deepjyoti30.dev/v2/ytmdl/search?q="
metadata_url = "https://apis.deepjyoti30.dev/v2/ytmdl/metadata?q="
download_url = "https://apis.deepjyoti30.dev/v2/ytmdl/download"


def search(query):
    payload_list = []
    response = requests.get(search_url+query)
    data = response.json()
    for items in data[:1]:
        for meta in metadata(query)[:5]:
            payload = {
                "song": {
                    "format": "m4a",
                    "video_id": items['id']
                },
                "metadata": meta
            }
            payload_list.append(payload)

    return payload_list

def metadata(query):
    metadata_response = requests.get(metadata_url+query)
    return metadata_response.json()

def download(payload_list):
    song_list = []
    for payload in payload_list:
        print(json.dumps(payload, indent=4))
        res = requests.post(download_url, json=payload)
        song_list.append({
            "title" : payload['metadata']['name'],
            "image": payload['metadata']['cover'],
            "url": res.json()['url'],
            "description": payload['metadata']['artist']+"\n"+payload['metadata']['album']
        })
    return song_list

# payloads = search("dil to hai dil")
# download(payloads)
