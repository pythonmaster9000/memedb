from deepgram import Deepgram
import json
import os


class Stt:
    def __init__(self, filename):
        self.filename = filename
        self.deepgram = Deepgram('d637d492f0e01c6578488b2c2403d95fb4de63a4')
        self.filepath = os.environ.get('MEMEDATAFILEPATH')
        #self.filepath = '/root'

    def get_speech(self):
        try:
            with open(fr'{self.filepath}\{self.filename}.mp4', 'rb') as audio:
                info = {'buffer': audio, 'mimetype': 'video/mp4'}
                result = self.deepgram.transcription.sync_prerecorded(info, {'punctuate': False})
                speech = json.loads(json.dumps(result))['results']['channels'][0]['alternatives'][0]['transcript']
            return speech
        except FileNotFoundError:
            print('File path incorrect')
        except Exception as e:
            print(f"Most likely invalid API KEY {e}")
        return ''


if __name__ == "__main__":
    ...

