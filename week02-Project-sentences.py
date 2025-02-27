# added a default for a second parameter in the make sentence function so that the second verb in the sentence has a different tense
# Added an additional determiner, noun, verb and prepositional phrase to the final sentence

import os
import random

os.system('cls' if os.name == 'nt' else 'clear')

def main():
    
    print(make_sentence(1,'past'))
    print(make_sentence(1,'present'))
    print(make_sentence(1, 'future'))
    print(make_sentence(2,'past'))
    print(make_sentence(2,'present'))
    print(make_sentence(2,'future'))


def make_sentence(quantity, tense, second_tense="past"):
    determiner = get_determiner(quantity)
    determiner_two = get_determiner(quantity)
    noun = get_noun(quantity)
    noun_two = get_noun(quantity)
    verb = get_verb(quantity, tense)
    preposition = get_preposition()
    prepositional_phrase = get_prepositional_phrase(quantity)
    verb_two = get_verb(quantity, second_tense)
    prepositional_phrase_two = get_prepositional_phrase(quantity)
    sentence = f'{determiner} {noun} {preposition} {determiner_two} {noun_two} {verb} {prepositional_phrase} and {verb_two} {prepositional_phrase_two}'
    return sentence.capitalize()

def get_determiner(quantity):
    """Return a randomly chosen determiner. A determiner is
  a word like "the", "a", "one", "some", "many".
  If quantity is 1, this function will return either "a",
  "one", or "the". Otherwise this function will return
  either "some", "many", or "the".
  Parameter
      quantity: an integer.
          If quantity is 1, this function will return a
          determiner for a single noun. Otherwise this
          function will return a determiner for a plural
          noun.
  Return: a randomly chosen determiner.
  """
    if quantity == 1:
        words = ['a', 'one', 'the']
    else:
        words = ['some', 'many', 'the']
    word = random.choice(words)
    return word

def get_noun(quantity):
    """Return a randomly chosen noun.
  If quantity is 1, this function will
  return one of these ten single nouns:
      "bird", "boy", "car", "cat", "child",
      "dog", "girl", "man", "rabbit", "woman"
  Otherwise, this function will return one of
  these ten plural nouns:
      "birds", "boys", "cars", "cats", "children",
      "dogs", "girls", "men", "rabbits", "women"
  Parameter
      quantity: an integer that determines if
          the returned noun is single or plural.
  Return: a randomly chosen noun.
    """
    if quantity == 1:
        nouns = ["bird", "boy", "car", "cat", "child","dog", "girl", "man", "rabbit", "woman"]
    else:
        nouns = ["birds", "boys", "cars", "cats", "children","dogs", "girls", "men", "rabbits", "women"]
    noun = random.choice(nouns)
    return noun

def get_verb(quantity, tense):
    """Return a randomly chosen verb. If tense is "past",
  this function will return one of these ten verbs:
      "drank", "ate", "grew", "laughed", "thought",
      "ran", "slept", "talked", "walked", "wrote"
  If tense is "present" and quantity is 1, this
  function will return one of these ten verbs:
      "drinks", "eats", "grows", "laughs", "thinks",
      "runs", "sleeps", "talks", "walks", "writes"
  If tense is "present" and quantity is NOT 1,
  this function will return one of these ten verbs:
      "drink", "eat", "grow", "laugh", "think",
      "run", "sleep", "talk", "walk", "write"
  If tense is "future", this function will return one of
  these ten verbs:
      "will drink", "will eat", "will grow", "will laugh",
      "will think", "will run", "will sleep", "will talk",
      "will walk", "will write"
  Parameters
      quantity: an integer that determines if the
          returned verb is single or plural.
      tense: a string that determines the verb conjugation,
          either "past", "present" or "future".
  Return: a randomly chosen verb.
  """
    if tense == 'past':
        verbs = ["drank", "ate", "grew", "laughed", "thought","ran", "slept", "talked", "walked", "wrote"]
    elif tense == 'present' and quantity==1:
        verbs = ["drinks", "eats", "grows", "laughs", "thinks", "runs", "sleeps", "talks", "walks", "writes"]
    elif tense == 'present' and quantity !=1:
        verbs = ["drink", "eat", "grow", "laugh", "think", "run", "sleep", "talk", "walk", "write"]
    elif tense == 'future':
        verbs = ["will drink", "will eat", "will grow", "will laugh","will think", "will run", "will sleep", "will talk", "will walk", "will write"]
    verb = random.choice(verbs)
    return verb

def get_preposition():
    return random.choice(["about", "above", "across", "after", "along","around", "at", "before", "behind", "below", "beyond", "by", "despite", "except", "for", "from", "in", "into", "near", "of", "off", "on", "onto", "out", "over", "past", "to", "under", "with", "without"])

def get_prepositional_phrase(quantity):
    preposition = get_preposition()
    determiner = get_determiner(quantity)
    noun = get_noun(quantity)
    sentence = f'{preposition} {determiner} {noun}'
    return sentence.lower()




main()



