import ffmpeg
import os
import msearch


class Compress:
    def __init__(self, filename):
        self.target_bitrate = 7000
        self.filepath = os.environ.get('MEMEDATAFILEPATH')
        self.filename = filename

    def check_size(self):
        return int(
            ffmpeg.probe(fr'{self.filepath}\{self.filename}.mp4', select_streams="v")['format']['size']) / 1048576 < 8

    def compress(self):
        # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
        min_audio_bitrate = 32000
        max_audio_bitrate = 256000

        probe = ffmpeg.probe(fr'{self.filepath}\{self.filename}.mp4')
        # file duration, in s.
        duration = float(probe['format']['duration'])
        # Audio bitrate, in bps.
        audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
        # Target total bitrate, in bps.
        target_total_bitrate = (self.target_bitrate * 1024 * 8) / (1.073741824 * duration)

        # Target audio bitrate, in bps
        if 10 * audio_bitrate > target_total_bitrate:
            audio_bitrate = target_total_bitrate / 10
            if audio_bitrate < min_audio_bitrate < target_total_bitrate:
                audio_bitrate = min_audio_bitrate
            elif audio_bitrate > max_audio_bitrate:
                audio_bitrate = max_audio_bitrate
        # Target file bitrate, in bps.
        file_bitrate = target_total_bitrate - audio_bitrate

        i = ffmpeg.input(fr'{self.filepath}\{self.filename}.mp4')
        ffmpeg.output(i, os.devnull,
                      **{'c:v': 'libx264', 'b:v': file_bitrate, 'pass': 1, 'f': 'mp4'}
                      ).overwrite_output().run()
        suffix = 1
        while not msearch.Search(f'{self.filename}{suffix}').is_in_filename():
            suffix += 1
        ffmpeg.output(i, fr'{self.filepath}\{self.filename}{suffix}.mp4',
                      **{'c:v': 'libx264', 'b:v': file_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                      ).overwrite_output().run()
        os.remove(fr'{self.filepath}\{self.filename}.mp4')
        os.rename(fr'{self.filepath}\{self.filename}{suffix}.mp4',fr'{self.filepath}\{self.filename}.mp4')
        # make output file filename + 1 if no such file exists, else + 2 then delete the old file and remove suffix
