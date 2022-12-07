

class Similarity:

    adjs = []

    def compare(self, item):
        item.likely = 0

        for a in self.adjs:
            if item.adjectives.__contains__(a):
                item.likely += 1

        return item



