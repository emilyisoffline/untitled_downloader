from download import extractScriptJSON, getTrackDetails, downloadFile
import validators, os, threading

URL = input("project name ? : ")
if not validators.url(URL):
    print("URL is NOT valid. Try again.")
    quit()

trackDetails = []
data = extractScriptJSON(URL)

for track in data['tracks']:
    getTrackDetails(track, trackDetails)

artwork_url = data['project']['artwork_signed_url']
album_title = data['project']['title']

newpath = f'./{album_title}' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

threads = []

for details in trackDetails:
    t = threading.Thread(target=downloadFile, args=(details, album_title,))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()