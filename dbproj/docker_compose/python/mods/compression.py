import ffmpeg
import os
from mods import msearch
import subprocess


class Compress:
    def __init__(self, filename):
        self.target_bitrate = 7000
        #self.filepath = os.environ.get('MEMEDATAFILEPATH')
        self.filepath = '/root'
        self.filename = filename

    def check_size(self):
        return int(
            ffmpeg.probe(fr'{self.filepath}/{self.filename}.mp4', select_streams="v")['format']['size']) / 1048576 < 8

    def compress(self):
        #min_audio_bitrate = 32000
        #max_audio_bitrate = 256000
        #probe = ffmpeg.probe(fr'{self.filepath}/{self.filename}.mp4')
        #duration = float(probe['format']['duration'])
        #audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
        #target_total_bitrate = (self.target_bitrate * 1024 * 8) / (1.073741824 * duration)
        #if 10 * audio_bitrate > target_total_bitrate:
        #    audio_bitrate = target_total_bitrate / 10
        #    if audio_bitrate < min_audio_bitrate < target_total_bitrate:
        #        audio_bitrate = min_audio_bitrate
        #    elif audio_bitrate > max_audio_bitrate:
        #        audio_bitrate = max_audio_bitrate
        #file_bitrate = target_total_bitrate - audio_bitrate
        #i = ffmpeg.input(fr'{self.filepath}\{self.filename}.mp4')
        #ffmpeg.output(i, os.devnull,
        #              **{'c:v': 'libx264', 'b:v': file_bitrate, 'pass': 1, 'f': 'mp4'}
        #              ).overwrite_output().run()
        #suffix = 1
        #while msearch.Search(f'{self.filename}{suffix}').is_in_filename():
        #    print('prevention working')
        #    suffix += 1
        with open(fr'{self.filepath}/{self.filename}1.mp4', 'w') as f:
            pass
        subprocess.run(fr'/usr/bin/ffmpeg -y -i {self.filepath}/{self.filename}.mp4 -b 800k {self.filepath}/{self.filename}1.mp4')
        #ffmpeg.output(i, fr'{self.filepath}/{self.filename}{suffix}.mp4',
        #              **{'c:v': 'libx264', 'b:v': file_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
        #              ).overwrite_output().run()
        os.remove(fr'{self.filepath}/{self.filename}.mp4')
        os.rename(fr'{self.filepath}/{self.filename}1.mp4',fr'{self.filepath}/{self.filename}.mp4')

