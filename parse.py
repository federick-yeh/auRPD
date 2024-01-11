from song import Song
import argparse
import csv

def parse():
	args = parse_cmdline_args()
	songs = parse_songs(args.songs_uri)
	countdown = parse_countdown(args.countdown_uri)
	return songs, countdown


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


def parse_songs(songs_uri):
	songs = []
	with open(songs_uri, 'r') as csv_file:
		csv_reader = csv.reader(csv_file)
		next(csv_reader) # skip header
		for row in csv_reader:
			if any(not col for col in row):
				continue
			songs.append(Song(row[0], row[1], row[2], row[3], row[4]))

	return songs


def parse_countdown(countdown_uri):
	return Song(None, None, countdown_uri, None, None)