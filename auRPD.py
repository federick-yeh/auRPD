from parse import parse
from save import save_and_process
from stitch import stitch
from config import Config

import os


def generate_audio(queue_path: str, countdown_path: str, output_path: str, config: dict = None):
	if not os.path.isfile(queue_path):
		raise FileNotFoundError(f'Song queue file not found: {queue_path}')

	config = Config(config)

	try:
		songs, countdown = parse(queue_path, countdown_path, config)
	except ValueError as e:
		raise ValueError('\n'.join(e.args))
	save_and_process(songs, countdown, config)
	stitch(songs, output_path, config)


if __name__ == '__main__':
	generate_audio(
		'test\songs_list.csv',
		r'C:\dev\_federick\auRPD\default_countdown.mp3',
		'rpd_audio.mp3'
	)