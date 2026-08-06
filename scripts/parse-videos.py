import json
import urllib.request
import xml.etree.ElementTree as ET

# Techie Sagnik YouTube Channel ID
CHANNEL_ID = "UC7iDb0g7a62P5tcSEwZeAFA"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

def parse_channel_videos():
    try:
        # Request YouTube RSS feed
        req = urllib.request.Request(
            RSS_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'yt': 'http://www.youtube.com/xml/schemas/2015'
        }

        entries = root.findall('atom:entry', ns)
        if not entries:
            print("No videos found in feed.")
            return False

        videos = []
        shorts = []

        for entry in entries:
            video_id = entry.find('yt:videoId', ns).text
            title = entry.find('atom:title', ns).text
            link = entry.find('atom:link', ns).attrib.get('href', '')

            video_item = {
                'id': video_id,
                'title': title
            }

            # Distinguish Shorts vs Regular Videos
            if '/shorts/' in link or '#shorts' in title.lower() or 'short' in title.lower():
                shorts.append(video_item)
            else:
                videos.append(video_item)

        # Structure payload
        output = {
            "latest": videos[0] if len(videos) > 0 else (shorts[0] if shorts else None),
            "mostViewed": videos[1] if len(videos) > 1 else (videos[0] if videos else None),
            "latestShort": shorts[0] if len(shorts) > 0 else (videos[0] if videos else None),
            "mostViewedShort": shorts[1] if len(shorts) > 1 else (shorts[0] if shorts else None)
        }

        # Write to root videos.json
        with open("videos.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)

        print("Successfully generated videos.json with content:")
        print(json.dumps(output, indent=2))
        return True

    except Exception as e:
        print(f"Error fetching YouTube feed: {e}")
        return False

if __name__ == "__main__":
    parse_channel_videos()
