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

        matches = re.findall(r'https://cce\.noisypeak\.com/hls/[A-Z0-9]+/[A-Z0-9]+/m\.m3u8', r.text)

        if matches:
            print("🔎 Streams encontrados:")
            for m in matches:
                print(m)

            # agarramos el último (suele ser el bueno)
            stream = matches[-1]
            print(f"\n✅ Usando stream:\n{stream}")
            return stream

        print("❌ No se encontró stream válido")
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

