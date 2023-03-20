import mdatabase
from jarowinkler import *


class Search:
    """
        Searches the database using title and tags.
        Methods:
            by_title for searching from title ONLY
            by_tags for searhcing from tags ONLY
            search for the best match between title and tags
    """

    def __init__(self, title, tags):
        self.title = title
        self.tags = tags + [i for i in title.split()]
        self.dbdump = mdatabase.DataBase().grab_all_data()

    def by_title(self):
        return sorted(self.dbdump, key=lambda e: jarowinkler_similarity(e[1], self.title), reverse=True)

    def by_tags(self):
        return sorted(self.dbdump, key=lambda e: jarowinkler_similarity(e[2], ' '.join(self.tags)), reverse=True)

    def search(self):
        return sorted(self.dbdump, key=lambda e: max(jarowinkler_similarity(e[2], ' '.join(self.tags)),
                                                     jarowinkler_similarity(e[1], self.title)), reverse=True)


print(Search('terten', ['epic lebron james']).by_title(), 'by title res')
print(Search('terten', ['epic lebron james']).by_tags(), 'by title res')
print(Search('epic lebron james', ['epic lebron james']).search(), 'by title res')
