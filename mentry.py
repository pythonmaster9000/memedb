import mdatabase
import requests
import os


class Entry:
    """
        Represents a new meme entry to the database which includes:
        attachment url from discord message
        title given by user
        tags space separated

    """

    def __init__(self, attachment_url, title, tags):
        self.attachment_url = attachment_url
        self.title = title
        self.tags = tags
        self.filename = '_'.join(title.split())
        self.filepath = os.environ.get('MEMEDATAFILEPATH')

    def save_to_database(self):
        if mdatabase.DataBase().insert_row(file_name=self.filename, title=self.title, tags=self.tags):
            self.save_to_folder()
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
            print('No scheme supplied')
        with open(fr'{self.filepath}\{self.filename}.mp4', 'wb') as file:
            file.write(r.content)
        return True


if __name__ == '__main__':
    ...
    #Entry('testurl','testentry','test test tags').save_to_database()
    #Entry('urltester', 'mega fart', 'test test tags').save_to_database()
    #Entry('funny_meme', 'toot memes e', 'tooting toot meme').save_to_database()
    #Entry('fart_meme', 'epic lebron james', 'epic ding dong').save_to_database()
    #Entry('fart_meme', 'not epic lebron james', 'epic lebron james epic lebron james epic lebron james').save_to_database()
