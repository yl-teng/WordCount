# This Python program counts the frequency of all phrases (i.e., 
# combination of words in a text file. Specific phrases can be 
# excluded, like those listed in a file. The most frequently 
# counted words are displayed.
# Last modified: 2022-08-30 14.22


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
        msg += "No phrase is exluded from counting.\n"
        print(msg)
        return ''

    # Abort when the coding is not correct,
    # e.g., if it is not a text file, or the coding is wrong.
    except UnicodeDecodeError:
        msg = "The coding of '" + filename + "' seems wrong.\n"
        msg += "No phrase is exluded from counting.\n"
        print(msg)
        return ''

    else:
        return contents


def remove_char(string, char_list=''):
    """"
    This will remove the specific characters listed in the 
    string 'char_list' from the original string 'orig_string', and
    return a new string.
        DO NOT use any so-called separating characters (like a
    space) in the 'char_list', because ALL the listed characters
    will be chopped off.
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
    Split a string into a list of words, of which the letters are all
    in lower cases, and return that list.
    """
    string = contents.lower()   # turn letters into lower cases.
    
    # Replace each non-alphabetic character with a space.
    string = re.sub('[^A-Za-z\']', ' ', string)

    words = string.split()
    return words


def phrases_in_sentence(sentence, phrase_length=2):
    """
    Extracts all phrases in a string (typically a sentence), and
    return a list of these phrases. When the phrase cannot be
    created (e.g., the sentence fragment is shorter than the given
    length), an empty list is returned.
        Phrases are defined as continuesly written words. The
    length of the phrase (phrase_len) is defined as the number of
    words in the phrase. The words are separated by blanks,
    typically a space. 
    """
    words = split_words(sentence)

    # Count the number of words in the splited sentence.
    word_number = len(words)

    # Create an empty list to store these phrases.
    phrases = []

    # A phrase should not have less than 2 words.
    if phrase_length < 2:
        phrase_length = 2
    
    # Extract phrases in the sentence. 
    # 's_index': the index in the sentence fragment.
    # 'pr_index': the index in the phrase.
    else:
        for s_index in range(word_number):
            if (s_index + phrase_length) <= word_number:
                phrase = ''     # An empty string to store a phrase.
                for pr_index in range(phrase_length):
                    phrase += words[s_index + pr_index] + ' '
                phrase = phrase.rstrip()    # Remove the last space.
                phrases.append(phrase)
            else:
                break
        
        phrases = set(phrases)     # Combine same phrases, if any.
        return phrases


def phrase_set(sentences, phrase_length=2):
    """
    Collect all phrases with given number of words in a list of
    sentences, and return them as a list of phrases.
        Same phrases are combined as one.
    """
    if phrase_length < 2:   # A phrase can't have less than 2 words.
        phrase_length = 2

    phrases = []            # An empty list to store phrases.
    
    for sentence in sentences:
        phrases += phrases_in_sentence(sentence, phrase_length) 

    while '' in phrases:    # Remove empty phrases, if any.
        phrases.remove('')

    phrases = set(phrases)  # Combine same phrases, if any.
    return phrases


def exclude_phrase(phrases, exclusion=''):
    """
    Exclude the phrases, as listed in the given file 'exclusion',
    from a list of phrases (strings). This will return a list of
    phrases without the excluded ones.
        In the file 'exclusion', the phrases to be excluded are
    separated from each other by a new line.
    """
    # When the file for storing excluded words is not given.
    if exclusion == '':
        return phrases
    
    # When the file for storing excluded words is given.
    else:
        contents = open_exclusion(exclusion).lower()
        exclude_phrases = contents.splitlines()

        for exclude_phrase in exclude_phrases:
            while exclude_phrase in phrases:
                phrases.remove(exclude_phrase)
        return phrases


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

            # Compare if list_a is the same as sect_b.
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


def top_counts(count_dict, top_range=10, least_count=0):
    """
    Rearrange the phrase count results based on count numbers, from
    more to less, and list the top counted phrases (by default, the
    top 10). Those whose counts are less than a given number will
    be ignored. In the end, the top counted phrases and their
    corresponding counts are returned.
    """
    # Remove phrases with small counts. ???
    for key in list(count_dict.keys()):
        if count_dict[key] < least_count:
            del count_dict[key]

    # Sort the phrases by their counts
    sorted_counts = sorted(count_dict.items(), key=lambda x:x[1], 
        reverse=True)

    top_counts = []     # An empty list to store top counted items.

    # Pick the items with the count in the top range.
    for index in range(len(sorted_counts)):
        if index < top_range:
            item = (sorted_counts[index][0], sorted_counts[index][1])
            top_counts.append(item)

    return top_counts


def output_results(
    top_results, top_range, least_count, txtsource, output_file
    ):
    """
    Format the results, print them on screen, and store them in a
    file.
    """
    import time     # For recording the time of running program.

    # Format date and test conditions
    msg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg += "\nRead file:\t" + txtsource + "\n"
    msg += "The top " + str(top_range) + " results "
    msg += "(skimmed if counts < " + str(least_count) + "):\n"

    for index in range(len(top_results)):
        msg += top_results[index][0] + "\t\t"
        msg += str(top_results[index][1]) + "\n"

    msg += "Output file:\t" + output_file + "\n\n\n"

    # Print results and associated info.
    print(msg)
    # Also, write the results and associated into to the file.
    with open(output_file, 'a') as file_object:
        file_object.write(msg)



# The main program.

phrase_length = 5   # The number of words in phrase.
top_range = 30      # Show only the top frequent phrases.
least_count = 3     # Phrases with less than this counts are skimmed.

# The file in which the original texts is stored.
txtsource = 'resource\\source.txt'

# The file stores words to be excluded from counting.
#     These words are separated from each other with a newline,
# i.e., each line stores only one phrase in the file.
exclusion = 'resource\\excl_phrase.txt'

# The file where results will be stored.
output_file = 'data\\results.txt'

contents = open_source(txtsource)
clear_contents = remove_char(contents, '"-')

sentences = split_sentence(clear_contents)
phrases = phrase_set(sentences, phrase_length)
phrases = exclude_phrase(phrases, exclusion)
results = count_phrase(phrases, sentences)

top_results = top_counts(results, top_range, least_count)

output_results(
    top_results, top_range, least_count, txtsource, output_file
    )
