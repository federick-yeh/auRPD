import argparse
import csv
import os
import re
import yt_dlp

from song import Song, parse_duration


def parse(queue_path, countdown_path, config):
	errors = []

	try:
		countdown = parse_countdown(countdown_path, config)
	except ValueError as e:
		errors.extend(e.args)

	try:
		songs = parse_queue(queue_path, config)
	except ValueError as e:
		errors.extend(e.args)

	if errors:
		raise ValueError(*errors)
	return songs, countdown


def parse_countdown(countdown_path, config):
	ydl = yt_dlp.YoutubeDL(config.ytdl_opts)

	if not os.path.isfile(countdown_path):
		try:
			with ydl:
				info = ydl.extract_info(countdown_path, download=False)
		except yt_dlp.utils.DownloadError:
			raise ValueError(f'[Countdown]: "{countdown_path}" not recognized as a valid URL or file path.')

	return Song('COUNTDOWN', 'AUDIO', countdown_path, None, None)


def parse_queue(queue_path, config):
	errors = []

	rows = []
	with open(queue_path, 'r') as csv_file:
		csv_reader = csv.reader(csv_file)
		next(csv_reader)  # skip header
		for row in csv_reader:
			if len(row) != 5 or any(not col for col in row):
				continue
			rows.append(row)

	songs = []
	for row in rows:
		try:
			song = parse_row(row, config)
		except ValueError as e:
			errors.extend(e.args)
		else:
			songs.append(song)

	if errors:
		raise ValueError(*errors)
	return songs


def parse_row(row, config):
	artist, title, uri, start_time_string, end_time_string = row
	ydl = yt_dlp.YoutubeDL(config.ytdl_opts)
	errors = []

	# validate link / filepath
	if not os.path.isfile(uri):
		try:
			with ydl:
				info = ydl.extract_info(uri, download=False)
		except yt_dlp.utils.DownloadError:
			errors.append(f'{artist} - {title}: "{uri}" not recognized as a valid URL or file path.')
		else:
			filename, _ = os.path.splitext(ydl.prepare_filename(info))
			filepath = f'{filename}.{config.audio_extension}'
	else:
		filepath = f'{config.temp_dir}{os.path.basename(uri)} {artist}-{title}.{config.audio_extension}'

	# validate timestamp format
	try:
		start_time = parse_duration(start_time_string)
	except ValueError:
		errors.append(f'{artist} - {title}: Invalid start time format: "{start_time_string}"')
	try:
		end_time = parse_duration(end_time_string)
	except ValueError:
		errors.append(f'{artist} - {title}: Invalid end time format: "{end_time_string}"')

	if errors:
		raise ValueError(*errors)
	return Song(artist, title, uri, start_time, end_time, filepath=filepath)


def parse_cmdline_args():
	argparser = argparse.ArgumentParser(
		prog='auRPD',
		description='Stitch together music for a Random Play Dance.'
	)

	argparser.add_argument("songs_uri",
												 metavar="songs",
												 help="path to csv file listing songs and timestamps")
	argparser.add_argument("countdown_uri",
												 metavar="countdown",
												 help="path or link to countdown audio")

	return argparser.parse_args()