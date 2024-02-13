# coding=utf-8


# This Python program counts the frequency of all words, including the
# hyphenated ones. Specific words can be excluded, like those listed
# in a file or those shorter than a given length. and the most
# frequently counted words are displayed.
# UTF-8 encoding is used for reading all text files.
# Last modified 2022-10-12 18:45



# For counting by frequency.
from collections import Counter

# Modulus for creating word clouds.
import wordcloud

# The class 'Image' is needed to open images.
from PIL import Image

# For preparing the image array for image masking and color pattern.
import numpy as np

# For displaying the word cloud on the screen.
import matplotlib.pyplot as plt

# For getting the time and forming the result report. 
import time



def open_source(filename):
    """
    Open the file and return text contents as a string.
    UTF-8 encoding is used for opening the text file.
    """
    try:
        with open(filename, encoding='utf-8') as file_object:
            contents = file_object.read()    

    except FileNotFoundError:   # Abort when the file is not found.
        print("Cannot open file '" + filename + "'.")

    # Abort when the coding is not correct, e.g., when it is not a
    # text file, or the coding is wrong.
    except UnicodeDecodeError:
        message = "Cannot open file '" + filename + ".\n"
        message += "Make sure it is an UTF-8 encoded text file."
        print(message)

    else:
        return contents


def open_exclusion(filename):
    """
    Open the file containing words to be excluded (sometimes called
    'stop word'). This will return a string for further use.
        The file to be openned should be in ASCII encoding.
        If the file can't be openned properly, return ''.
    """
    try:
        with open(filename, encoding='utf-8') as file_object:
            contents = file_object.read()

    # Abort when the file is not found.
    except FileNotFoundError:
        msg = "Cannot open file '" + filename + "'. for excluding "
        msg += "specific words.\n"
        msg += "No word is exluded from word counting.\n"
        print(msg)
        return ''

    # Abort when the coding is not correct,
    # e.g., if it is not a text file, or the coding is wrong.
    except UnicodeDecodeError:
        msg = "The coding of '" + filename + "' seems wrong.\n"
        msg += "No word is exluded from word counting.\n"
        print(msg)
        return ''

    else:
        return contents


def split_words(contents, split_char="", split_chars=[", ", ". "]):
    """
    Split a text string (the 'contents') into a list of words in lower
    cases, and return the word list. Characters listed in 'split_char'
    will be replaced by a space, and character sets in the list
    'split_chars' will be replaced by a space, too. Then, blank
    characters are used as for word splitting.
    """
    string = contents.lower()    # Turn all letters into lower cases.

    # Replace all spliting characters (mostly punctuations) into
    # spaces. For dealing with acadamic papers, uft-8 encoding is
    # suggested to avoid encoding errors.
    for char in split_char:
        string = string.replace(char, ' ')

    # Replace all splitting character sets into spaces.
    for chars in split_chars:
        string = string.replace(chars, ' ')

    # Split the text string by blank letters, including the space, \t,
    # \r, and \n.
    words = string.split()

    return words


def exclude_words(words, exclude_string=''):
    """
    Exclude the words listed in the given file 'exclusion'.
    This will return a list words without the excluded words.
    """
    # When the file for storing excluded words is not given. This may
    # happen, for instance, when the file storing excluded words
    # cannot be opened properly.
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


def min_word_length(words, min_length=1):
    """
    Exclude words short than the minimum length as defined by the
    'min_length', and return a list of words without these short words.
    """
    if min_length <= 1:     # A word cannot be less than a character.
        return words
    else:
        sorted_words = []   # Store the new word list for returning.
        for index in range(len(words)):
            if len(words[index]) >= min_length:
                sorted_words.append(words[index])
        return sorted_words


def is_num(string):
    """
    Determine if a string is a number or not. The number can be an
    integer or a folat, and can be a positive or a negative number.
    This is used by the following function 'del_num()'.
    """
    if len(string) == 0:
        return False
    
    if (string[0] == '-' or string[0] == '+'):
        string = string[1:]     # Remove the negetive sign.

    # Split the string into sections by the decimal mark '.'.
    sects = string.split('.')

    if len(sects) > 2:          # A number cannot have > 2 sections.
        return False
    else:
        for sect in sects:      # Check if each sector is a number.
            if not sect.isdigit():
                return False
            else:
                return True
    

def del_num(words):
    """
    Remove numbers (including negative ones) from a list of strings.
    """
    sorted_words = []

    for word in words:
        if is_num(word):
            continue
        else:
            sorted_words.append(word)

    return sorted_words


def remove_less_counts(results, min_count=1):
    """
    Exclude words with counts less than a given value.
    The count results are a list of tuples containing two elements - 
    the counted element (the word) and the member of count.
    """
    if min_count <= 1:          # A listed word cannot have < 1 count.
        return results
    else:
        sorted_results = []     # Store the result list for returning.
        for index in range(len(results)):
            if results[index][1] >= min_count:
                sorted_results.append(results[index])
        return sorted_results


def report_results(
    results,        # Word frequency results in class Counter.
    min_length,     # The minimal length of the word for counting.
    min_count,      # The minimal counting number of the word.
    top_common,     # The top most frequently counted words.
    txtsource,      # Where the text is stored (for report).
    exclude_string, # Words to be excluded (for reporting.
    report_file,    # Where the result report is stored.
    ):
    """
    This is the reporting function that will format the results, print
    them on screen, form the word cloud image, display them on screen,
    and save these files.
    """
    # Format date and test conditions
    msg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg += "\nRead file:\t" + txtsource + "\n"

    if exclude_string == '':
        msg += "No word is specifically excluded.\n"
    else:
        msg += "Exclusion word list is applied.\n"

    msg += "Word length >= " + str(min_length) + ", "
    msg += "count >= " + str(min_count) + ". "
    msg += "Top " + str(top_common) + " most frequent words:\n"

    # Format results for printing and storage.
    top_words = results.most_common(top_common)
    printed_words = remove_less_counts(top_words, min_count)

    for printed_word in printed_words:
        msg += printed_word[0] + "\t\t" + str(printed_word[1]) + "\n"

    msg += "Output file:\t" + report_file + "\n\n\n"
    
    # Print results and associated info.
    print(msg)

    # Also, write the results and associated into to the file.
    with open(report_file, 'a') as file_object:
        file_object.write(msg)



def open_mask(mask_image):
    """
    This function forms an image array for generating a mask image and
    a color pattern, both of which will be used for the word cloud.
    Note that words will not show on areas with the white color (NOT
    transparent areas).
    """
    try:
        img_array = np.array(Image.open(mask_image))
    except FileNotFoundError:
        return None
    else:
        info = "Apply the mask file '" + mask_image
        info += "' for the word cloud.\n"
        print(info)
        return img_array


def draw_word_cloud(
    word_frq,       # A dictionary storing the word frequency results. 
    max_words=200,  # How many (most frequent) words will display.
    wc_img=None,    # Where the word cloud image will be stored.
    img_array=None  # The image array for mask and color patterning.
    ):
    """
    Draw the word cloud, display it on the screen, and save it.
    More parameters about the word cloud image formed can be adjusted
    inside this function.
    """
    # Create the word cloud and apply the mask
    wc_obj = wordcloud.WordCloud(
        width=1000,                 # The width of the word cloud.
        height=1000,                # The height of the word cloud.
        background_color='white',   # Background color; default black.
        font_path='arialbd.ttf',    # Use the "Arial Bold" font.
        min_font_size=12,           # Minimum font size; 4 by default.
      # max_font_size=24,           # Maximum font size.
        max_words=max_words,        # Maximal number of words to show.
        mask=img_array              # Apply a mask array for output.
        )

    # Generate the word cloud object using the given text.
    wc_obj.generate_from_frequencies(word_frq)

    # Tailor the color pattern of the word cloud from the patten of a
    # given image. Here, the image used is the same as the mask image.
    # img_colors = wordcloud.ImageColorGenerator(mskimg)
    if img_array is None:
        print("No mask is applied for creating the word cloud.\n")
    else:
        # Extract the color pattern for image mask.
        img_colors = wordcloud.ImageColorGenerator(img_array)
        wc_obj.recolor(color_func=img_colors)

    # Display the word cloud on the screen.
    plt.imshow(wc_obj, interpolation='bilinear')
    plt.axis('off')     # Hide the axis
    plt.show()          # Display the image on the screen

    # Save the word cloud output to an image
    wc_obj.to_file(wc_img)



# The following is the main program:

# All the .TXT files should be in UTF-8 or ASCII encoding.
txtsource = '.\\resource\\SERev.txt'    # Text file to be analyzed.

# This file stores the words to be excluded from counting.
# Words are separated from each other with a comma and/or a space.
exclusion = '.\\resource\\excl_word.txt'

report_file = '.\\data\\results.txt'    # For saving results.
mask_image = ".\\resource\\cube.png"    # For image mask and coloring.
wc_img = ".\\data\\SERev.png"           # For saving word cloud image.


# Parameters for counting the word frequency, which will be saved in
# a report file.
min_length = 4      # The least lenght of a word.
top_common = 40     # The top frequent words to list out.
min_count = 3       # Only words' frequency >= this will be listed.

# Define the characters and character sets for splitting words. Blank
# characters have been already included so it is not necessary to
# list them.
split_char = ":;!?\"#$&{}<>*/÷=\\@|·~‘“”–⋯"
split_chars = [", ", ". ", ".\n", ".\r", "' ", "’ ", " (", ") "]


contents = open_source(txtsource)
words = split_words(contents, split_char, split_chars)

exclude_string = open_exclusion(exclusion)

# remove words that are not taken into account.
words = exclude_words(words, exclude_string)

words = min_word_length(words, min_length)  # Remove short words.
words = del_num(words)      # Remove numbers in the list of words.

# Counting the words utilizing class Counter.
# The results forms a dictionary which is encapsuled in a tuple, so
# that the order of key-value pairs can be kept. Words are listed as
# keys, and the corresponding count numbers are the values for those
# keys. This class will also be used to generate the word cloud.
results = Counter(words)

report_results(results, min_length, min_count, top_common, txtsource,
        exclude_string, report_file)


# Generate the word cloud image applying a mask image.
img_array = open_mask(mask_image)
draw_word_cloud(results, 200, wc_img, img_array)
