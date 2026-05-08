from pytube import YouTube

def download_audio(url):

    yt = YouTube(url)

    stream = yt.streams.filter(
        only_audio=True
    ).first()

    output = stream.download()

    return output
