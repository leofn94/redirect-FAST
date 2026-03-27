import requests
import re
import os


OUTPUT_FILE = "truetv.m3u"

# URL del canal
CHANNEL_ID = "434159"

def get_stream():
    try:
        url = "https://play.truetvplus.com/live-tv?channelId=434159"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(url, headers=headers, timeout=10)

        # buscar tokens tipo /hls/XXXXXXX/
        tokens = re.findall(r'/hls/([A-Z0-9]+)/', r.text)

        if not tokens:
            print("❌ No se encontraron tokens")
            return None

        # eliminar duplicados manteniendo orden
        tokens = list(dict.fromkeys(tokens))

        # usar el último (más reciente)
        token = tokens[-1]

        stream = f"https://cce.noisypeak.com/hls/{token}/m.m3u8"

        print(f"✅ Token encontrado: {token}")
        print(f"🎬 Stream: {stream}")

        return stream

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
        print("⚠️ No se pudo obtener stream nuevo")

        if os.path.exists(OUTPUT_FILE):
            print("♻️ Manteniendo stream anterior")
            return
        else:
            print("❌ No hay archivo previo, usando dummy")
            stream = "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"

    write_m3u(stream)


if __name__ == "__main__":
    main()

