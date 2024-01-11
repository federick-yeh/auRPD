import re
from datetime import timedelta

class Song:
	def __init__(self, artist, title, uri, start_time, end_time):
		self._artist = artist
		self._title = title
		self._uri = uri
		self._start_time = parse_timedelta(start_time) if start_time else None
		self._end_time = parse_timedelta(end_time) if end_time else None
		self._filepath = None

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
		return str_timedelta(self._start_time)

	@property
	def end_time(self):
		return str_timedelta(self._end_time)

	@property
	def filepath(self):
		return self._filepath

	@filepath.setter
	def filepath(self, value):
		self._filepath = value

	def get_fade_start_time(self, fade_duration):
		if self._start_time is None or self._end_time is None:
			return None
		return str_timedelta(self._end_time -self._start_time - timedelta(seconds=fade_duration))


def parse_timedelta(td_str):
	pattern = r"^\s*((?P<hours>\d+):)?(?P<minutes>\d{1,2}):(?P<seconds>\d{2})\s*$"
	match = re.match(pattern, td_str)
	if match:
		hours = int(match.group('hours') or 0)
		minutes = int(match.group('minutes'))
		seconds = int(match.group('seconds'))
		return timedelta(hours=hours, minutes=minutes, seconds=seconds)
	else:
		raise ValueError(f'Invalid time format: {td_str}')


def str_timedelta(td):
	total_seconds = td.total_seconds()
	hours, remainder = divmod(total_seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'