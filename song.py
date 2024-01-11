class Song:
	def __init__(self, artist, title, uri, start_time, end_time):
		self._artist = artist
		self._title = title
		self._uri = uri
		self._start_time = start_time
		self._end_time = end_time
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
		return self._start_time

	@property
	def end_time(self):
		return self._end_time

	@property
	def filepath(self):
		return self._filepath

	@filepath.setter
	def filepath(self, value):
		self._filepath = value
