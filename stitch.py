import ffmpeg


def stitch(songs, output_path, config):
	inputs = [ffmpeg.input(song.filepath).audio for song in songs]
	processing = ffmpeg.concat(*inputs, v=0, a=1)
	output = ffmpeg.output(processing, output_path)
	ffmpeg.run(output, overwrite_output=True)


