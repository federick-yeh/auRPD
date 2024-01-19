import re
from datetime import timedelta

class Song:
	def __init__(self, artist, title, uri, start_time, end_time, filepath=None):
		self._artist = artist
		self._title = title
		self._uri = uri
		self._start_time = start_time
		self._end_time = end_time
		self._filepath = filepath

	def __repr__(self):
		return f"Song({self.artist} - {self.title}, {self.start_time} ~ {self.end_time}, {self.filepath})"

	@property
	def artist(self):
		return self._artist

	@property
	def title(self):
		return self._title

	@property
	def uri(self):
		return self._uri

	@property
	def start_time(self):
		return format_duration(self._start_time)

	@property
	def end_time(self):
		return format_duration(self._end_time)

	@property
	def filepath(self):
		return self._filepath

	@filepath.setter
	def filepath(self, value):
		self._filepath = value

	def get_fade_start_time(self, fade_duration):
		if self._start_time is None or self._end_time is None:
			return None
		return format_duration(self._end_time - self._start_time - timedelta(seconds=fade_duration))


def parse_duration(string):
	pattern = r"^\s*(?:(?P<hours>\d+)\s*:\s*)?(?P<minutes>\d{1,2})\s*:\s*(?P<seconds>\d{1,2})(?:\s*\.\s*(?P<milliseconds>\d+))?\s*$"
	match = re.match(pattern, string)
	if not match:
		raise ValueError(f'Invalid time format: {string}')

	hours = int(match.group('hours') or 0)
	minutes = int(match.group('minutes'))
	seconds = int(match.group('seconds'))
	milliseconds = int(match.group('milliseconds') or 0)
	return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)


def format_duration(duration):
	if duration is None:
		return None

	total_seconds = duration.total_seconds()
	hours, remainder = divmod(total_seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	milliseconds = duration.microseconds / 1000

	string = f'{int(minutes):02d}:{int(seconds):02d}'
	if hours:
		string = f'{int(hours):02d}:' + string
	if milliseconds:
		string += f'.{int(milliseconds):03d}'

	return string