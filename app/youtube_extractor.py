import youtube_dl
from youtube_dl.utils import DateRange


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'youtube_include_dash_manifest': False,
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'no_color': True,
    'ignoreerrors': True
}

def download_mp3(videoid, stdout=False):
    ydl_opts.update({
        'audio-format': 'mp3',
        'format': 'worstvideo+worstaudio',
        'audio-quality': '9',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '9',
        }]
    })
    if not stdout:
        ydl_opts['outtmpl'] = 'app/static/%(id)s.%(ext)s'
    else:
        ydl_opts['outtmpl'] = '-'

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        return ydl.download(['https://www.youtube.com/watch?v={}'.format(videoid)])


def get_video_info(videoid):
    ydl_opts['extract_flat'] = True
    ydl_opts['dump_single_json'] = True

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(
            'https://www.youtube.com/watch?v={}'.format(videoid),
            download=False
        )

def get_channel_videos(channel, short=False, daterange=None):
    #if daterange is None:
    #    daterange = DateRange(start='now-8months', end='now')
    #    print(daterange)
    #ydl_opts['daterange'] = daterange

    ydl_opts['dump_single_json'] = True
    if short: ydl_opts['extract_flat'] = True

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:

        if short:
            url = ydl.extract_info(
                'https://www.youtube.com/user/{}'.format(channel),
                download=False
            ).get('url')
            return ydl.extract_info(
                url,
                download=False
            ).get('entries', [])
        else:
            return ydl.extract_info(
                'https://www.youtube.com/user/{}'.format(channel),
                download=False
            ).get('entries', [])


