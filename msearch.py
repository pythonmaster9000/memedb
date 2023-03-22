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

    def __init__(self, title, tags=None):
        if tags is None:
            tags = []
        self.title = title
        self.tags = tags + [i for i in title.split()]
        self.dbdump = mdatabase.DataBase().grab_all_data()

    def is_in_filename(self):
        return self.title in [i[0] for i in self.dbdump]

    def by_speech(self, history=3):
        matches = []
        for entry in self.dbdump:
            speech = entry[3].split()
            inquiry = self.tags
            result = -1
            l = 0
            r = len(inquiry)
            while r < len(speech):
                result = max(jarowinkler_similarity(' '.join(inquiry), ' '.join(speech[l:r])), result)
                l += 1
                r += 1
            matches.append([result, entry])
        if not history:
            return sorted(matches, key=lambda e: e[0], reverse=True)
        return sorted(matches, key=lambda e: e[0], reverse=True)[:history]

    def by_title(self, history=3):
        if not history:
            return sorted(self.dbdump, key=lambda e: jarowinkler_similarity(e[1], self.title), reverse=True)
        return sorted(self.dbdump, key=lambda e: jarowinkler_similarity(e[1], self.title), reverse=True)[:history]

    def by_tags(self, history=3):
        if not history:
            return sorted(self.dbdump, key=lambda e: jarowinkler_similarity(e[2], ' '.join(self.tags)), reverse=True)
        return sorted(self.dbdump, key=lambda e: jarowinkler_similarity(e[2], ' '.join(self.tags)), reverse=True)[
               :history]

    def search(self, history=3):
        if not history:
            return sorted(self.dbdump, key=lambda e: max(jarowinkler_similarity(e[2], ' '.join(self.tags)),
                                                         jarowinkler_similarity(e[1], self.title)), reverse=True)
        return sorted(self.dbdump, key=lambda e: max(jarowinkler_similarity(e[2], ' '.join(self.tags)),
                                                     jarowinkler_similarity(e[1], self.title)), reverse=True)[:history]


if __name__ == '__main__':
    print(Search('elon_ma1').is_in_filename())
