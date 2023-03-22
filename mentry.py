import mdatabase
import requests
import os
import stt
import compression

class Entry:
    """
        TODO : Check size of video
        Represents a new meme entry to the database which includes:
        attachment url from discord message
        title given by user
        tags space separated

    """

    def __init__(self, attachment_url, title, tags=''):
        self.attachment_url = attachment_url
        self.tags = tags
        self.title = title
        self.filename = '_'.join(title.split())
        self.filepath = os.environ.get('MEMEDATAFILEPATH')
        self.Compress = compression.Compress(self.filename)
    def save_to_database(self):
        if not self.save_to_folder():
            return False
        speech = stt.Stt(self.filename).get_speech()
        if mdatabase.DataBase().insert_row(file_name=self.filename, title=self.title, tags=self.tags, speech=speech):
            print('done')
            return True
        return False

    def save_to_folder(self):
        if not self.filepath:
            print('Set env variable filepath: MEMEDATAFILEPATH')
            return False
        try:
            r = requests.get(self.attachment_url)
        except requests.exceptions.ConnectionError:
            print(f'Bad request {self.attachment_url}')
            return False
        except requests.exceptions.MissingSchema:
            print('No scheme supplied invalid url')
            return False
        with open(fr'{self.filepath}\{self.filename}.mp4', 'wb') as file:
            file.write(r.content)
        if self.Compress.check_size():
            return True
        self.Compress.compress()
        print('compressed')
        return True


if __name__ == '__main__':
    #f = Entry('nothing', 'elon ma')
    #print(compression.Compress(f.filename).check_size())
    #print(os.environ.get('MEMEDATAFILEPATH'))
    #f = Entry('https://cdn.discordapp.com/attachments/743195774518689814/1084338837213413386/2023-01-20_21-49-03_UTC.mp4','you cant park there')
    #f.save_to_database()
    ...
