# This Python file uses the following encoding: utf-8

"""Generate markov text from text files."""
from sys import argv
from random import choice
import twitter
import os

SEUSS_TEXT = "green-eggs.txt"
GETTY_TEXT = "gettysburg.txt"
AFT_TEXT = "american-fairy-tales.txt"
PNP_TEXT = "pride-and-prejudice.txt"

try:
    input_path = argv[1]
    ngram = int(argv[2])

except IndexError:
    input_path = SEUSS_TEXT
    ngram = 2


def open_and_read_file(file_path=SEUSS_TEXT):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    with open(file_path) as text_file:
        return text_file.read().strip()


def make_chains(text_string, chains, ngram=2):
    """Takes input text as string; returns dictionary of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
    """

    words = text_string.split()

    # This code doesn't create a key for last words.

    for index in range(len(words) - ngram):

        key = tuple(words[index:index + ngram])
        value = words[index + ngram]

        chains[key] = chains.get(key, [])
        chains[key].append(value)

    return chains


def process_texts(text_files, chains, ngram=2):
    """Takes n texts and adds them to the Markov chain dictionary."""
    

    for text_file in text_files:
        input_text = open_and_read_file(text_file)
        chains = make_chains(input_text, ngram, chains)

    return chains


def make_text(chains, ngram=2, set_sent=True):
    """Returns text from chains.
    Takes 3 arguments, chains, ngram, and set_sent.

    chains takes a markov chain dictionary.

    ngram specifies what kind of 'gram' to use. (Optional) 
    The default setting is 2 for bigram.

    set_sent specifies whether to end the chain at one sentence. (Optional)
    The default setting is True, to limit the chain to one sentence 
    unless the sentence is the initial key from the markov dictionary.
    """

    # picks a random consecutive pair of words to start our string
    words = list(choice(chains.keys()))
    end_punctuation = ["?", ".", "!", "”"]

    while True:

        key = tuple(words[-ngram:])

        try:
            value = chains[key]
        except KeyError:
            break

        words.append(choice(value))

        if set_sent and words[-1][-1] in end_punctuation:
            break

    words[0] = words[0].title()

    return " ".join(words)

def tweet(random_text):

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # This will print info about credentials to make sure 
    # they're correct
    print api.VerifyCredentials()

    # Send a tweet
    status = api.PostUpdate(random_text + " #aug17kat")
    print status.text


# Open the file and turn it into one long string
# input_text = open_and_read_file(input_path)
random_text = ""
global_chains = {}


# Get a Markov chain

global_chains = process_texts(["humorous-ghost-stories.txt"], ngram, global_chains)

# Produce random text

while len(random_text) > 140 or random_text == "":
    random_text = make_text(global_chains, ngram)

print random_text


verify = raw_input("Do you want to tweet this Markov? (yes/no) ")
if verify == "yes":

    tweet(random_text)