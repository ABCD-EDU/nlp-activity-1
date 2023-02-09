import re
import string

def preprocess_text(text):
    # lowercase text
    text = text.lower()

    # remove punctuation, excluding hyphens and apostrophes
    exclude = re.sub(r'[-\'\s]', '', string.punctuation)
    text = re.sub("[" + exclude + "]", '', text)

    # remove numbers
    text = re.sub(r'\d+', '', text)

    # remove multiple whitespaces
    text = re.sub(r'\s+', ' ', text)

    return text

def write_to_file(text, filename):
    with open(filename, 'w') as f:
        f.write(text)

if __name__ == '__main__':
    # Read the input text from file
    with open('hist-raw.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    # Preprocess the text
    preprocessed_text = preprocess_text(text)

    # Write the preprocessed text to file
    write_to_file(preprocessed_text, 'hist-preprocessed.txt')
