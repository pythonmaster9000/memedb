import pymysql.cursors


class DataBase:
    """
        Represents interactions with database.
        Grabbing all data from database
        Storing new entries with:
        file name, title and tags

    """

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='meme',
                                          database='sakila'
                                          )
        self.cur = self.connection.cursor()

    def grab_all_data(self):
        try:
            self.cur.execute("SELECT * FROM `memes`")
            return self.cur.fetchall()
        except pymysql.err.ProgrammingError:
            print('ProgrammingError')
            return False

    def insert_row(self, file_name, title, tags):
        command = f'INSERT INTO `memes`(file_name,title,tags)\nVALUES("{file_name}", "{title}", "{tags}")'
        try:
            self.cur.execute(command)
            self.connection.commit()
            return True
        except pymysql.err.DataError:
            print('DataError')
            return False
        except pymysql.err.OperationalError:
            print('OperationalError')
            return False

if __name__ == '__main__':
    ...