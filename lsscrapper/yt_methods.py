from pytube import YouTube

hashtag = "#ConferenciaAMLO"
video_download_folder = "../youtube/video/"
audio_download_folder = "../youtube/audio/"
confs = [
        "https://www.youtube.com/watch?v=9xXj0tAXjt8", #21 nov 2019
        "https://www.youtube.com/watch?v=I3qT_yPIcq0",
        "https://www.youtube.com/watch?v=AsSS29zmdls",
        "https://www.youtube.com/watch?v=Xud-81Fjw0E",
        "https://www.youtube.com/watch?v=8iFXAPeclps",
        "https://www.youtube.com/watch?v=UVCg_zbcU8s",
        "https://www.youtube.com/watch?v=9Am_Cmafsx4",
        "https://www.youtube.com/watch?v=XnSCJ4dMpdQ",
        "https://www.youtube.com/watch?v=qKUmiuHUYPc",
        "https://www.youtube.com/watch?v=OWL413dIzI8",
        ]

for link in confs:
    yt = YouTube(link)
    title = yt.title
    try:
        possible_filename = yt.title.split(",")[1].strip().replace(" ", "_")
    except:
        possible_filename = yt.title.replace(" ", "_")
    streams = yt.streams.all()
    candidate = None
    for stream in yt.streams.filter(file_extension="webm", progressive=False).all():
        if stream.resolution == "720p":
            if stream.video_codec == "vp9":
                import ipdb;ipdb.set_trace()
                #stream.download(video_download_folder, 
                #                possible_filename + ".webm")
                break

    for stream in yt.streams.filter(only_audio=True, progressive=False).all():
        import ipdb;ipdb.set_trace()
        #stream.download(audio_download_folder,
        #                possible_filename + "")
    break
import ipdb;ipdb.set_trace()
