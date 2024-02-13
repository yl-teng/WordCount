# This Python program counts the frequency of all words in a text 
# file. Specific words can be excluded, like those listed in a 
# file or those shorter than a given length. and the most
# frequently counted words are displayed.
# Last modified: 2022-08-30 15.16


# For splitting words by blanks and punctuations.
# Used by function 'split_words()'
import re

# For counting by frequency.
from collections import Counter


def open_source(filename):
    """
    Open the file and return contents as a string for further use.
        The file to be opened should be in ASCII encoding.
    """
    try:
        with open(filename) as file_object:
            contents = file_object.read()

    # Abort when the file is not found.
    except FileNotFoundError:
        print("Cannot open file '" + filename + "'.")

    # Abort when the coding is not correct,
    # e.g., if it is not a text file, or the coding is wrong.
    except UnicodeDecodeError:
        message = "Cannot open file '" + filename + ".\n"
        message += "Make sure it is an ASCII text file."
        print(message)

    else:
        return contents


def open_exclusion(filename):
    """
    Open the file containing words to be excluded. This will return
    a string for further use.
        The file to be openned should be in ASCII encoding.
        If the file can't be openned properly, return ''.
    """
    try:
        with open(filename) as file_object:
            contents = file_object.read()

    # Abort when the file is not found.
    except FileNotFoundError:
        msg = "Cannot open file '" + filename + "'.\n"
        msg += "No word is exluded from counting.\n"
        print(msg)
        return ''

    # Abort when the coding is not correct,
    # e.g., if it is not a text file, or the coding is wrong.
    except UnicodeDecodeError:
        msg = "The coding of '" + filename + "' seems wrong.\n"
        msg += "No word is exluded from counting.\n"
        print(msg)
        return ''

    else:
        return contents


def split_words(contents):
    """
    Split a string into a list of words in lower cases, and return
    that list. Requires to import modulus 're' to use re.sub().
    """
    string = contents.lower()   # turn letters into lower cases.
    
    # Replace each non-alphabetic character with a space.
    string = re.sub('[^A-Za-z]', ' ', string)

    words = string.split()
    return words


def exclude_words(words, exclude_string=''):
    """
    Exclude the words listed in the given file 'exclusion'.
    This will return a list words without the excluded words.
    """
    # When the file for storing excluded words is not given.
    if exclude_string == '':
        return words
    
    # When the file for storing excluded words is given.
    else:
        exclude_string = exclude_string.lower()
        exclude_words = split_words(exclude_string)
        for exclude_word in exclude_words:
            while exclude_word in words:
                words.remove(exclude_word)
        return words


def least_word_length(words, least_length=1):
    """
    Exclude words short than the length given by 'least_length'.
    Will return a list of words without the short words.
    """
    if least_length < 1:    # A word cannot be less than one letter.
        least_length = 1

    renewed_words = []      # Store the new word list for returning.
    for index in range(len(words)):
        if len(words[index]) >= least_length:
            renewed_words.append(words[index])

    return renewed_words


def remove_less_counts(results, least_count=1):
    """Exclude words with counts less than the given value."""
    if least_count < 1:
        least_count = 1     # A listed word cannot have < 1 count.

    renewed_results = []    # Store the result list for returning.
    for index in range(len(results)):
        if results[index][1] >= least_count:
            renewed_results.append(results[index])

    return renewed_results


def output_results(
    results, least_length, least_count, top_common, txtsource,
    exclude_string, output_file
    ):
    """
    Format the results, print them on screen, and store them in a
    file.
    """
    import time     # For recording the time of running program.

    # Format date and test conditions
    msg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg += "\nRead file:\t" + txtsource + "\n"

    if exclude_string == '':
        msg += "No word is specifically excluded.\n"
    else:
        msg += "Exclusion word list is applied.\n"

    msg += "Word length >= " + str(least_length) + ", "
    msg += "count >= " + str(least_count) + ". "
    msg += "Top " + str(top_common) + " most frequent words:\n"

    # Format results for printing and storage.
    top_words = results.most_common(top_common)
    printed_words = remove_less_counts(top_words, least_count)

    for printed_word in printed_words:
        msg += printed_word[0] + "\t\t" + str(printed_word[1]) + "\n"

    msg += "Output file:\t" + output_file + "\n\n\n"
    
    # Print results and associated info.
    print(msg)
    # Also, write the results and associated into to the file.
    with open(output_file, 'a') as file_object:
        file_object.write(msg)



# The main program

# The file in which the original texts is stored.
txtsource = 'resource\\source.txt'

# The file stores words to be excluded from counting.
# Words are separated from each other with a comma.
exclusion = 'resource\\excl_word.txt'

# The file where results will be stored.
output_file = 'data\\results.txt'

least_length = 9    # The least lenght of a word.
top_common = 30     # The top frequent words to list out.
least_count = 10     # Only words above this will be listed

contents = open_source(txtsource)
words = split_words(contents)
exclude_string = open_exclusion(exclusion)
words = exclude_words(words, exclude_string)
words = least_word_length(words, least_length)

# Counting the words utilizing class Counter.
# The results forms a dictionary. Words are listed as keys, and the
# corresponding count numbers are the values for those keys.
results = Counter(words)

output_results(
    results, least_length, least_count, top_common, txtsource,
    exclude_string, output_file
    )
