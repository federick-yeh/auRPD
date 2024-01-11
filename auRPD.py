from parse import parse
from save import save, save_song
from stitch import stitch

songs, countdown = parse()
save_song(countdown)
save(songs)
stitch(songs, countdown)