import nltk
import heapq
import re

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')  # Ensures punkt_tab is also downloaded

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

def summarize_text(text, summary_length=3):
    # Step 1: Clean the text
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'👦[0-9]*👦', '', text)

    # Step 2: Tokenize sentences and words
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))
    word_frequencies = {}

    for word in word_tokenize(text.lower()):
        if word.isalnum() and word not in stop_words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1

    # Step 3: Normalize word frequencies
    max_freq = max(word_frequencies.values())

    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    # Step 4: Score each sentence
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if len(sentence.split(' ')) < 30:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequencies[word]

    # Step 5: Select top sentences
    summary_sentences = heapq.nlargest(summary_length, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)

    return summary

# Example usage
if __name__ == "__main__":
    print("Enter the article/text you want to summarize:\n")
    input_text = ""
    while True:
        try:
            line = input()
            if line == "":
                break
            input_text += line + " "
        except EOFError:
            break

    print("\n--- Summary ---\n")
    summary = summarize_text(input_text)
    print(summary)