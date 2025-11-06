import requests, json, os, validators, re
from bs4 import BeautifulSoup
import urllib.parse, urllib.request

from tag import tagFolder

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

trackDetails = []

# Extract downloadable signed URLs and details from API into dictionaries
for track in data['state']['loaderData']['routes/library.project.$projectSlug']['project']['tracks']:
    artwork_url = data['state']['loaderData']['routes/library.project.$projectSlug']['project']['project']['artwork_signed_url']
    file_dir = urllib.parse.quote_plus(track['audio_fallback_url'].split('/', 7)[-1])
    downloadURL = API.format(MUSIC_URL=file_dir)
    album_title = data['state']['loaderData']['routes/library.project.$projectSlug']['project']['project']['title']
    trackDetail = {
        'url': downloadURL,
        'title': track['title'],
        'album': album_title,
        'albumArt': artwork_url
    }
    trackDetails.append(trackDetail)

newpath = f'./{album_title}' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

#Download each file

# for details in trackDetails:
#     r = requests.get(details['url'])
#     print("Downloading ", details['title'], "...")
#     sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', details['title'])
#     urllib.request.urlretrieve(r.json()['url'].replace("https", "http"), f"./{details['album']}/{sanitized_name}.mp3")
    
print("Tagging each File.")    
tagFolder(f"./{album_title}", trackDetails)