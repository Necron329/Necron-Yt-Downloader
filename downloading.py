downloadInProgress = False

def transformToMp3(title, path, pd, os):
        audio = pd.from_file(f"{path}{title}.mp4", format="mp4")
        audio.export(f"{path}{title}.mp3", format="mp3")
        if os.path.exists(f"{path}{title}.mp4"):
            os.remove(f"{path}{title}.mp4")

def validateName(title, re):
        prohibited_chars = [r'[^a-zA-Z0-9 ]']
        pattern = "|".join(prohibited_chars)
        updated_string = re.sub(pattern, '', title)
        return updated_string

def defineTypeOfLink(link, pt):
        try:
            yt = pt.YouTube(link)
            return yt
        except:
            try:
                yt = pt.Playlist(link)
                if len(yt)<1:
                    raise
                return yt
            except:
                return None

def downloadVideo(link, path, format, os, re, pd):
    title = validateName(link.title, re)
    video_streams = link.streams
    if format == "MP4":
        stream = video_streams.filter(file_extension="mp4", progressive=True).get_highest_resolution()
        stream.download(path, filename=f"{title}.mp4")
    else:
        stream = video_streams.filter(only_audio=True, file_extension="mp4").order_by('abr').last()
        stream.download(path, filename=f"{title}.mp4")
        transformToMp3(title, path, pd, os)

def downloadPlaylist(link, path, format, os, re, pd):
    pass


def downloadThread(link, path, format, os, re, pt, pd):
    global downloadInProgress
    if isinstance(link, pt.YouTube):
        downloadVideo(link, path, format, os, re, pd)
        downloadInProgress = False
    elif isinstance(link, pt.Playlist):
        downloadPlaylist(link, path, format, os, re, pd)
        downloadInProgress = False


def download(link, path, format, os, re, threading, pt, pd):
    global downloadInProgress
    link = defineTypeOfLink(link, pt)
    if link is not None and downloadInProgress == False:
        downloadInProgress = True
        thread = threading.Thread(target=downloadThread, args=(link,path,format,os,re,pt,pd,))
        thread.start()