import csv
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

with open("bbc-text.csv", "r") as csvfile:
    print(f"First line (header) looks like this:\n\n{csvfile.readline()}")
    print(f"Each data point looks like this:\n\n{csvfile.readline()}")

def remove_stopwords(sentence):
    stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]

    sentence = sentence.lower()

    sentence_no_stopwords = [word for word in sentence.split(' ') if not word in stopwords]
    sentence = ' '.join(sentence_no_stopwords)
    return sentence

sen=remove_stopwords("I am about to go to the store and get any snack")
print(f"ANs = {sen}")

def parse_data_from_file(filename):
    sentences=[]
    labels=[]
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            labels.append(row[0])
            sentences.append(remove_stopwords(row[1]))

    return sentences,labels

# Test your function

# With original dataset
sentences, labels = parse_data_from_file("bbc-text.csv")

print("ORIGINAL DATASET:\n")
print(f"There are {len(sentences)} sentences in the dataset.\n")
print(f"First sentence has {len(sentences[0].split())} words (after removing stopwords).\n")
print(f"There are {len(labels)} labels in the dataset.\n")
print(f"The first 5 labels are {labels[:5]}\n\n")


def fit_tokenizer(sentences):
    """
    Instantiates the Tokenizer class

    Args:
        sentences (list): lower-cased sentences without stopwords

    Returns:
        tokenizer (object): an instance of the Tokenizer class containing the word-index dictionary
    """
    ### START CODE HERE
    # Instantiate the Tokenizer class by passing in the oov_token argument
    tokenizer = Tokenizer(oov_token="<OOV>")
    # Fit on the sentences
    tokenizer.fit_on_texts(sentences)
    ### END CODE HERE
    return tokenizer

tokenizer = fit_tokenizer(sentences)
word_index = tokenizer.word_index

print(f"Vocabulary contains {len(word_index)} words\n")
print("<OOV> token included in vocabulary" if "<OOV>" in word_index else "<OOV> token NOT included in vocabulary")


def get_padded_sequences(tokenizer, sentences):
    """
    Generates an array of token sequences and pads them to the same length

    Args:
        tokenizer (object): Tokenizer instance containing the word-index dictionary
        sentences (list of string): list of sentences to tokenize and pad

    Returns:
        padded_sequences (array of int): tokenized sentences padded to the same length
    """

    ### START CODE HERE
    # Convert sentences to sequences
    sequences = tokenizer.texts_to_sequences(sentences)

    # Pad the sequences using the post padding strategy
    padded_sequences = pad_sequences(sequences, padding='post')
    ### END CODE HERE

    return padded_sequences

padded_sequences = get_padded_sequences(tokenizer, sentences)
print(f"First padded sequence looks like this: \n\n{padded_sequences[0]}\n")
print(f"Numpy array of all sequences has shape: {padded_sequences.shape}\n")
print(f"This means there are {padded_sequences.shape[0]} sequences in total and each one has a size of {padded_sequences.shape[1]}")


def tokenize_labels(labels):
    """
    Tokenizes the labels

    Args:
        labels (list of string): labels to tokenize

    Returns:
        label_sequences, label_word_index (list of string, dictionary): tokenized labels and the word-index
    """
    ### START CODE HERE

    # Instantiate the Tokenizer class
    # No need to pass additional arguments since you will be tokenizing the labels
    label_tokenizer = Tokenizer()

    # Fit the tokenizer to the labels
    label_tokenizer.fit_on_texts(labels)

    # Save the word index
    label_word_index = label_tokenizer.word_index

    # Save the sequences
    label_sequences = label_tokenizer.texts_to_sequences(labels)

    ### END CODE HERE

    return label_sequences, label_word_index

label_sequences, label_word_index = tokenize_labels(labels)
print(f"Vocabulary of labels looks like this {label_word_index}\n")
print(f"First ten sequences {label_sequences[:10]}\n")