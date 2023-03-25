import pymysql.cursors


class DataBase:
    """
        TODO: Add backup dump function to happen every day
        Represents interactions with database.
        Grabbing all data from database
        Storing new entries with:
        file name, title and tags

    """

    def __init__(self):
        self.connection = pymysql.connect(host='mysql',
                                          user='root',
                                          password='root',
                                          database='db',
                                          port=3306
                                          )
        self.cur = self.connection.cursor()

    def grab_all_data(self):
        try:
            self.cur.execute("SELECT * FROM `memes`")
            return self.cur.fetchall()
        except pymysql.err.ProgrammingError:
            print('ProgrammingError')
            return False

    def insert_row(self, file_name, title, tags, speech=''):
        command = f'INSERT INTO `memes`(file_name,title,tags,speech)\nVALUES("{file_name}", "{title}", "{tags}", "{speech}") '
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
    print(DataBase().grab_all_data())
    ...
