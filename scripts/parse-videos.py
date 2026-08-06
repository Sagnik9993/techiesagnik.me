import json
import urllib.request
import xml.etree.ElementTree as ET
import sys

CHANNEL_ID = "UC7iDb0g7a62P5tcSEwZeAFA"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

def parse_channel_videos():
    print(f"Fetching RSS feed from: {RSS_URL}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    try:
        req = urllib.request.Request(RSS_URL, headers=headers)
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'yt': 'http://www.youtube.com/xml/schemas/2015'
        }

        entries = root.findall('atom:entry', ns)
        print(f"Found {len(entries)} total items in RSS feed.")

        if not entries:
            print("ERROR: RSS feed contains 0 entries.")
            sys.exit(1)

        videos = []
        for entry in entries:
            v_id = entry.find('yt:videoId', ns).text
            title = entry.find('atom:title', ns).text
            videos.append({'id': v_id, 'title': title})

        # Fallback handling so values are NEVER null
        latest = videos[0] if len(videos) > 0 else {"id": "", "title": "Visit YouTube"}
        most_viewed = videos[1] if len(videos) > 1 else latest
        latest_short = videos[2] if len(videos) > 2 else latest
        most_viewed_short = videos[3] if len(videos) > 3 else latest

        output = {
            "latest": latest,
            "mostViewed": most_viewed,
            "latestShort": latest_short,
            "mostViewedShort": most_viewed_short
        }

        with open("videos.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)

        print("SUCCESS: Wrote videos.json successfully!")
        print(json.dumps(output, indent=2))

    except Exception as e:
        print(f"FATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parse_channel_videos()
