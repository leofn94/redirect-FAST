import re
import requests

URL = "https://play.truetvplus.com/live-tv?channelId=434159"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_stream():
    r = requests.get(URL, headers=HEADERS)

    match = re.search(r'https://cce\.noisypeak\.com/hls/.*?/m\.m3u8', r.text)

    if match:
        return match.group(0)

    return None

def update_playlist(link):
    with open("truetv.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write('#EXTINF:-1 tvg-id="truetv" tvg-name="TrueTV",TrueTV\n')
        f.write(link + "\n")

if __name__ == "__main__":
    link = get_stream()

    if link:
        print("✅ Link encontrado:", link)
        update_playlist(link)
    else:
        print("❌ No se encontró el stream")