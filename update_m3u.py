import requests
import re

OUTPUT_FILE = "truetv.m3u"

# URL del canal
CHANNEL_ID = "434159"

def get_stream():
    try:
        # Endpoint interno (esto es lo importante)
        api_url = f"https://api.truetvplus.com/api/v1/channels/{CHANNEL_ID}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(api_url, headers=headers, timeout=10)

        if r.status_code != 200:
            print(f"❌ Error API: {r.status_code}")
            return None

        data = r.json()

        # 🔥 buscar el stream dentro del JSON
        stream_url = None

        if "streamUrl" in data:
            stream_url = data["streamUrl"]

        # fallback por si cambia estructura
        if not stream_url:
            text = str(data)
            match = re.search(r'https://[^\s"]+\.m3u8', text)
            if match:
                stream_url = match.group(0)

        if stream_url:
            print(f"✅ Stream encontrado:\n{stream_url}")
            return stream_url
        else:
            print("❌ No se encontró el stream en la API")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def write_m3u(url):
    content = f"""#EXTM3U
#EXTINF:-1 tvg-id="truetv" tvg-name="TrueTV",TrueTV
{url}
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Archivo M3U actualizado")


def main():
    stream = get_stream()

    if not stream:
        print("❌ No se pudo obtener el stream")
        return

    write_m3u(stream)


if __name__ == "__main__":
    main()

