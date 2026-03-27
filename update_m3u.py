import re
import requests

URL = "https://play.truetvplus.com/live-tv?channelId=434159"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_stream():
    r = requests.get(URL, headers=HEADERS)

    # buscar cualquier m3u8 (más amplio)
    matches = re.findall(r'https://[^\s"]+\.m3u8[^\s"]*', r.text)

    if matches:
        print("Encontrados:", matches)
        return matches[0]

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

print(r.text[:2000])
