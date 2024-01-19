class Config:
	def __init__(self, options: dict = None):
		self._temp_dir = '_temp/'
		self._audio_extension = 'wav'
		self._fade_in_duration = 2
		self._fade_out_duration = 1
		self._fade_in_curve = 'losi'
		self._fade_out_curve = 'tri'

	@property
	def audio_extension(self):
		return self._audio_extension

	@property
	def temp_dir(self):
		return self._temp_dir

	@property
	def fade_in_duration(self):
		return self._fade_in_duration

	@property
	def fade_out_duration(self):
		return self._fade_out_duration

	@property
	def fade_in_curve(self):
		return self._fade_in_curve

	@property
	def fade_out_curve(self):
		return self._fade_out_curve

	@property
	def ytdl_opts(self):
		return {
			'format': 'bestaudio/best',
			'outtmpl': f'/{self._temp_dir}%(id)s-%(title)s.%(ext)s',
			'postprocessors': [
				{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': self._audio_extension,
					'preferredquality': '192',
				},
			]
		}