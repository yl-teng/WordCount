# This Python program counts the frequency of given phrases (i.e., 
# combination of words) in a text file. The frequency of these
# phrases will be ranged and their counts will be given.
# Last modified: 2022-08-30 14.06


# For splitting words by blanks, and splitting sentences by 
# punctuations.
import re


def open_source(filename):
    """
    Open the file and return contents as a list of characters for
    further use. The files to be opened should be in ASCII encoding.
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


def remove_char(string, char_list=''):
    """"
    This will remove the specific characters listed in the 
    string 'char_list' from the original string 'orig_string', and
    return a new string.
        DO NOT use any so-called separating characters (like a space)
    in the 'char_list', because ALL the listed characters will be
    chopped off.
    """
    for char in char_list:
        if char in string:
            string = string.replace(char, '')
    return string


def split_sentence(contents, split_chars=',.!?:;()'):
    """
    Split texts into short, sentence-like fragments according to 
    punctuations, and return a list of sentences (strings).
        Punctuation characters for spliting are typically '.!?:;', 
    but a comma ',' is also considered.
    """
    split_pattern = "[" + split_chars + "]+"
    sentences = re.split(split_pattern, contents)

    # This loop removes empty spaces in each sentence fragment.
    for index in range(len(sentences)):
        sentences[index] = sentences[index].strip().lower()

    return sentences


def split_words(contents):
    """
    Split a string into a list of words in lower cases, and return
    that list.
    """
    string = contents.lower()   # turn letters into lower cases.
    
    # Replace each non-alphabetic character with a space.
    string = re.sub('[^A-Za-z\']', ' ', string)

    words = string.split()
    return words


def list_a_in_b(str_a, str_b):
    """
    Count how many list_a, as a whole, continuous series of items,
    can be found in list_b. 
    """
    list_a = split_words(str_a)
    list_b = split_words(str_b)

    a_len = len(list_a)
    b_len = len(list_b)
    count = 0
    
    for b_index in range(b_len):
        if b_index + a_len <= b_len:

            # Make a copy for part of list_b, and the length of the
            # copy is the same length as that of list_a.
            sect_b = []     # An empty list to store part of list_b.
            for a_index in range(a_len):
                sect_b.append(list_b[b_index + a_index])

            if list_a == sect_b:
                count += 1
    
    return count


def count_phrase(phrases, sentences=[]):
    """
    Count the number of phrase in a list of sentences that have no
    punctuations. This will return a dict containing each phrase as
    the key and the corresponding counting as the value.
    """
    count_dict = {}     # An empty dict to store counting results.
    
    for phrase in phrases:
        count = 0
        
        # Count a phrase in each sentence.
        for sentence in sentences:
            count += list_a_in_b(phrase, sentence)

        count_dict[phrase] = count
    
    return count_dict


def output_results(results, txtsource, output_file):
    """
    Format the results, print them on screen, and store them in a
    file.
    """
    import time     # For recording the time of running program.

    # Format date and test conditions
    msg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg += "\nRead file:\t" + txtsource + "\n"
    
    for result in results:
        msg += result[0] + "\t\t" + str(result[1]) + "\n"

    msg += "Output file:\t" + output_file + "\n\n\n"

    # Print results and associated info.
    print(msg)
    # Also, write the results and associated into to the file.
    with open(output_file, 'a') as file_object:
        file_object.write(msg)


# The main program.

# The file in which the original texts is stored.
txtsource = 'resource\\source.txt'

# The file where results will be stored.
output_file = 'data\\results.txt'

# Phrases to be counted, in the form of a list of strings. Phrases
# should be all listed in lower case 
phrases = ["in which", "on which", "at which", "for which", "of which"]

contents = open_source(txtsource)
clear_contents = remove_char(contents, '"-')

sentences = split_sentence(clear_contents)
results = count_phrase(phrases, sentences)
results = sorted(results.items(), key=lambda x:x[1], reverse=True)

output_results(results, txtsource, output_file)
