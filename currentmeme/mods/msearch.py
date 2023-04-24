from mods import mdatabase
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

    def is_in_title(self):
        return self.title in [i[1] for i in self.dbdump]

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
        matches = []
        for entry in self.dbdump:
            #print(entry[1].split(),' '.join(self.tags))
            speech = entry[1].split()
            inquiry = self.tags
            result = -1
            l = 0
            r = len(inquiry)
            while r <= len(speech):
                #if speech == ['all', 'up', 'in', 'her', 'like', 'a', 'wee', 'wee', 'dinner']:
                    #print("inquiry is : ", ' '.join(inquiry), "comparing against", ' '.join(speech[l:r]))
                result = max(jarowinkler_similarity(' '.join(inquiry), ' '.join(speech[l:r])), result)
                l += 1
                r += 1
            matches.append([result, entry])
        if not history:
            return sorted(matches, key=lambda e: e[0], reverse=True)
        res = sorted(matches, key=lambda e: e[0], reverse=True)
        return [i[1] for i in res][:history]
        #return sorted(matches, key=lambda e: e[0], reverse=True)[:history]

    #OLD search
    #def search(self, history=3):
    #    if not history:
    #        if self.title in [i[1] for i in self.dbdump]:
    #            return self.dbdump[self.dbdump.index(self.title)]
    #        return sorted(self.dbdump, key=lambda e: max(jarowinkler_similarity(e[2], ' '.join(self.tags)),
    #                                                    jarowinkler_similarity(e[1], self.title)), reverse=True)
    #    return sorted(self.dbdump, key=lambda e: max(jarowinkler_similarity(e[2], ' '.join(self.tags)),
    #                                                 jarowinkler_similarity(e[1], self.title)), reverse=True)[:history]


if __name__ == '__main__':
    print(Search('compressiontest').is_in_filename())
    # print(Search('mate').search())
    # print(Search('mate').by_speech())
    # print(Search('terten', ['epic lebron james']).by_title(), 'by title res')
    # print(Search('terten', ['epic lebron james']).by_tags(), 'by title res')
    # print(Search('epic lebron james', ['epic lebron james']).search(), 'by title res')
    #
    ...
