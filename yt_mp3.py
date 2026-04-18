import yt_dlp
from concurrent.futures import ThreadPoolExecutor


playlist_url = 'https://www.youtube.com/playlist?list=PLViFofX5-U5A5yQVjl1Va3-JN_FinGrC1'


# function to download mp3 from a url:
def download_video(url):
    opts = {
        'format': 'bestaudio/best',
        'js_runtimes': {'node': {}},
        'remote_components': ['ejs:github'],
        'outtmpl': r'D:\projects\failed\%(title)s.%(ext)s',
        'retries': 10,
        'fragment_retries': 10,
        'sleep_interval': 2,
        'max_sleep_interval': 5,
        
        # netscape cookies
        'cookiefile': r'D:\projects\cookies.txt',

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3'
        }],
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception:
        with open(r"D:\projects\failed.txt", "a", encoding="utf-8") as f:
            f.write(url + "\n")

# extract all 4705 links:
ydl_opts = {
    'quiet': True,
    'extract_flat': True,
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(playlist_url, download=False)
    urls = []
    for entry in info['entries']:
        urls.append(entry['url'])

# run 8 parallel downloads:
with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(download_video, urls)