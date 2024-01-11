import yt_dlp as ytdl
import os
from song import Song


def save(songs: list):
	for song in songs:
		save_song(song)


def save_song(song: Song):
	try:
		download_song(song)
	except ytdl.utils.DownloadError:
		if (os.path.isfile(song.uri)):
			song.filepath = song.uri
		else:
			raise FileNotFoundError(f'Could not process {song.artist} - {song.title}. "{song.uri}" not recognized as a valid URL or file path.')


def download_song(song: Song, extension='mp3'):
	ytdl_opts = get_ytdl_opts(audio_extension=extension)
	with ytdl.YoutubeDL(ytdl_opts) as ydl:
		video_info = ydl.extract_info(song.uri, download=False)
		filename, _ = os.path.splitext(ydl.prepare_filename(video_info))
		song.filepath = f'{filename}.{extension}'
		ydl.download([song.uri])


def get_ytdl_opts(audio_extension='mp3', temp_dir='_temp'):
	return {
		'format': 'bestaudio/best',
		'outtmpl': f'/{temp_dir}/%(id)s - %(title)s.%(ext)s',
		'postprocessors': [
			{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': audio_extension,
				'preferredquality': '192',  # TODO: needs to change to reflect codec?
			},
		]
	}
