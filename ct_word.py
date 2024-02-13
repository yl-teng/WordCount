# This program counts the frequency of given words in a text file.
# Last modified 2022-08-30 13.51

# For splitting words by blanks and punctuations.
# Used by function 'split_words()'
import re


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



# The main program

# The file in which the original texts is stored.
txtsource = 'resource\\source.txt'

# The file where results will be stored.
output_file = 'data\\results.txt'

# This list stores which words will be counted.
key_list = [
    'which', 'what', 'who', 'whose', 'where', 'when', 'why',
    'whether', 'while'
    ]

with open(txtsource) as f_obj:
    contents = f_obj.read()

words = split_words(contents)

counts = {}      # Create an empty dict to store counting results.

for key in key_list:
    count = 0
    
    for word in words:
        if key == word:
            count += 1

    counts[key] = count

# Rearrange the order. The function sorted() will return a list of 
# tuples to store the words and corresponding counts.
#
# key=lambda x:x[1]  -- It tells sorted() to sort based on the value 
#                       of the second element in each item (i.e., 
#                       the  counts, or say the value in the dict).
results = sorted(counts.items(), key=lambda x:x[1], reverse=True)

output_results(results, txtsource, output_file)

