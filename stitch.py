import ffmpeg
import os
from song import Song


def stitch(songs, countdown):
	for song in songs:
		trim_song(song)
		stitch_countdown(song, countdown)


def stitch_countdown(song, countdown):
	filepath, fileext = os.path.splitext(song.filepath)
	concat_filepath = f'{filepath}-concat{fileext}'

	input_song = ffmpeg.input(song.filepath)
	input_countdown = ffmpeg.input(countdown.filepath)
	processing = ffmpeg.concat(input_countdown, input_song, v=0, a=1)
	output = ffmpeg.output(processing, concat_filepath)
	ffmpeg.run(output)

	os.remove(song.filepath)
	os.rename(concat_filepath, song.filepath)


def trim_song(song: Song):
	filepath, fileext = os.path.splitext(song.filepath)
	trimmed_filepath = f'{filepath}-trim{fileext}'

	input = ffmpeg.input(song.filepath)
	processing = input.audio.filter('atrim', start=song.start_time, end=song.end_time)
	output = ffmpeg.output(processing, trimmed_filepath)
	ffmpeg.run(output)

	os.remove(song.filepath)
	os.rename(trimmed_filepath, song.filepath)