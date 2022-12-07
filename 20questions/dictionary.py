
from similar import Similarity


class Word:
    def __init__(self, item, adjectives):
        self.name = item
        self.adjectives = adjectives
        self.likely = 0


class Question:
    def __init__(self, prompt, yes_tag, no_tag, mabey_tag = ''):
        self.prompt = prompt
        self.yes_tag = yes_tag
        self.no_tag = no_tag
        self.mabey_tag = mabey_tag


def compare_function(item):
    return item.likely


class Dictionary:
    _dictionary = []
    similarity_handler = Similarity()
    _questions = []
    question_index = 0

    def __init__(self, source_path, category):
        self.load(source_path, category)

    def get_best_match(self, adjs):
        self.update_list(adjs)
        return self._dictionary[0]

    def update_list(self, adjs):
        self.similarity_handler.adjs = adjs[:]
        to_remove = []

        for i in range(len(self._dictionary)):
            self._dictionary[i] = self.similarity_handler.compare(self._dictionary[i])
            if self._dictionary[i].likely == 0:
                to_remove.append(i)

        to_remove.sort(reverse=True)

        for i in to_remove:
            self._dictionary.pop(i)

        self._dictionary.sort(key=compare_function, reverse=True)


    def load(self, source_path, category):
        self._dictionary = [Word('dog', ['domestic', 'pet', 'fast', 'mammal', 'eats_meat', 'not_food', 'plays_catch', 'larger']),
                            Word('cat', ['domestic', 'pet', 'fast', 'mammal', 'eats_meat', 'not_food', 'doesnt_play_catch', 'smaller']),
                            Word('turtle', ['domestic', 'pet', 'slow', 'reptile', 'eats_meat', 'not_food', 'doesnt_play_catch']),
                            Word('bunny', ['domestic', 'pet', 'fast', 'mammal', 'vegetarian', 'food', 'doesnt_play_catch', 'larger']),
                            Word('hamster', ['domestic', 'pet', 'slow', 'mammal', 'vegetarian', 'not_food', 'doesnt_play_catch', 'smaller'])]

        self._questions = [Question('Is this creature considered domestic?', 'domestic', 'wild'),
                           Question('Is this creature often kept as a pet?', 'pet', 'livestock', 'exotic'),
                           Question('Is this creature fast?', 'fast', 'slow', 'neither'),
                           Question('Is this a mammal?', 'mammal', ''),
                           Question('Is it a vegetarian?', 'vegetarian', 'eats_meat'),
                           Question('Is it often considered as food?', 'food', 'not_food'),
                           Question('Will it play catch?', 'plays_catch', 'doesnt_play_catch'),
                           Question('Can certain varieties grow to be big?', 'larger', 'smaller')]

    def questions(self):
        return self._questions
