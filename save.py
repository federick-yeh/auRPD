import yt_dlp as ytdl
import ffmpeg
import os
from song import Song


def save_and_process(songs, countdown, config):
	save(songs, countdown, config)
	process(songs, countdown, config)


def save(songs, countdown, config):
	save_song(countdown, config)
	for song in songs:
		save_song(song, config)


def save_song(song, config):
	if os.path.isfile(song.uri):
		original_filename, _ = os.path.splitext(os.path.basename(song.uri))
		filepath = f'{config.temp_dir}{original_filename} {song.artist}-{song.title}.{config.audio_extension}'
		song.filepath = filepath

		input = ffmpeg.input(song.uri)
		output = ffmpeg.output(input.audio, song.filepath)
		ffmpeg.run(output, overwrite_output=True)
	else:
		with ytdl.YoutubeDL(config.ytdl_opts) as ydl:
			ydl.download([song.uri])


def process(songs, countdown, config):
	for song in songs:
		trim_song(song, config)
		apply_fade(song, config)
		stitch_countdown(song, countdown, config)


def trim_song(song, config):
	filepath, fileext = os.path.splitext(song.filepath)
	trimmed_filepath = f'{filepath}-trim{fileext}'

	input = ffmpeg.input(song.filepath)
	processing = input.audio.filter('atrim', start=song.start_time, end=song.end_time)
	output = ffmpeg.output(processing, trimmed_filepath)
	ffmpeg.run(output)

	os.remove(song.filepath)
	os.rename(trimmed_filepath, song.filepath)


def apply_fade(song, config):
	filepath, fileext = os.path.splitext(song.filepath)
	fade_filepath = f'{filepath}-fade{fileext}'

	input = ffmpeg.input(song.filepath)
	processing = input.audio.filter('afade',
																  type='in',
																  curve=config.fade_in_curve,
																	duration=config.fade_in_duration)
	processing = processing.filter('afade',
																 type='out',
																 curve=config.fade_out_curve,
																 start_time=song.get_fade_start_time(config.fade_out_duration),
																 duration=config.fade_out_duration)
	output = ffmpeg.output(processing, fade_filepath)
	ffmpeg.run(output)

	os.remove(song.filepath)
	os.rename(fade_filepath, song.filepath)


def stitch_countdown(song, countdown, config):
	filepath, fileext = os.path.splitext(song.filepath)
	concat_filepath = f'{filepath}-concat{fileext}'

	input_song = ffmpeg.input(song.filepath)
	input_countdown = ffmpeg.input(countdown.filepath)
	processing = ffmpeg.concat(input_countdown, input_song, v=0, a=1)
	output = ffmpeg.output(processing, concat_filepath)
	ffmpeg.run(output)

	os.remove(song.filepath)
	os.rename(concat_filepath, song.filepath)