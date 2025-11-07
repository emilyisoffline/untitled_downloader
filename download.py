import requests, json, os, validators, re, threading
from bs4 import BeautifulSoup
import urllib.parse, urllib.request

API = "https://untitled.stream/api/storage/buckets/private-transcoded-audio/objects/{MUSIC_URL}/signedUrl?durationInSeconds=10800&cacheBufferInSeconds=600"

def extractScriptJSON(URL):
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    script_tag = soup.find_all('script')[2]
    data = script_tag.text.split("window.__remixContext = ", 1)[-1].rsplit(';', 1)[0]
    data = json.loads(data)
    return data['state']['loaderData']['routes/library.project.$projectSlug']['project']

def getTrackDetails(track, trackDetails):
    file_dir = urllib.parse.quote_plus(track['audio_fallback_url'].split('/', 7)[-1])
    downloadURL = API.format(MUSIC_URL=file_dir)
    trackDetail = {
        'url': downloadURL,
        'title': track['title'],
    }
    trackDetails.append(trackDetail)

def downloadFile(details, album_title):
    try:
        r = requests.get(details['url'], timeout=15)
        r.raise_for_status()
        signed_url = r.json()['url']  # actual MP3 URL
        
        sanitized_name = re.sub(r'[<>:\"/\\|?*]', '_', details['title'])
        file_path = os.path.join(album_title, f"{sanitized_name}.mp3")

        with requests.get(signed_url, stream=True, timeout=60) as audio:
            audio.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in audio.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        print(f"Downloaded {details['title']}")
    except Exception as e:
        print(f"Failed to download {details['title']} : {e}")