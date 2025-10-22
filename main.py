import requests, json, os, validators
from bs4 import BeautifulSoup
import urllib.parse, urllib.request

URL = input("project name ? : ")
if not validators.url(URL):
    print("URL is NOT valid. Try again.")
    quit()

API = "https://untitled.stream/api/storage/buckets/private-transcoded-audio/objects/{MUSIC_URL}/signedUrl?durationInSeconds=10800&cacheBufferInSeconds=600"

r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')
script_tag = soup.find_all('script')[2]
data = script_tag.text.split("window.__remixContext = ", 1)[-1].rsplit(';', 1)[0]
data = json.loads(data)

downloadable_urls = []

for track in data['state']['loaderData']['routes/library.project.$projectSlug']['project']['tracks']:
    file_dir = urllib.parse.quote_plus(track['audio_fallback_url'].split('/', 7)[-1])
    downloadURL = API.format(MUSIC_URL=file_dir)
    album_title = data['state']['loaderData']['routes/library.project.$projectSlug']['project']['project']['title']
    downloadable_urls.append([downloadURL, track['title'], album_title])

newpath = f'./{album_title}' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

for url in downloadable_urls:
    r = requests.get(url[0])
    print(r.json()['url'])
    urllib.request.urlretrieve(r.json()['url'].replace("https", "http"), f"./{url[2]}/{url[1]}.mp3")
    
