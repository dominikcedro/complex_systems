"""
author: Dominik Cedro
date: 04.10.2024
"""
import os
import string
from collections import Counter
import pandas as pd
from icecream import ic


def read_file(book_name):
    """
    Reads the content of a book file.

    This function opens a text file with the given book name, reads its content, and returns it as a string.

    Args:
        book_name (str): The name of the book file (without the .txt extension).

    Returns:
        str: The content of the book file.
    """
    with open(f'./assets/{book_name}.txt', 'r', encoding='utf-8') as file:
        read = file.read()
    return read


def prepare_tokens(book):
    """
    Creates tokens based on the book content.

    This function processes the book content by converting it to lowercase, removing punctuation,
    splitting it into words, and cleaning non-alphabetic characters. It returns a Counter object
    with the word frequencies.

    Args:
        book (str): The content of the book.

    Returns:
        collections.Counter: A Counter object with word frequencies.
    """
    # lower case
    book.lower()
    # remove punctuation
    book.translate(str.maketrans('', '', string.punctuation))
    # into words
    words = book.split()
    # clean from symbols and digits
    for word in words:
        if not word.isalpha():
            # delete trailing dots and comas
            word_len = len(word)
            if not word[word_len - 1].isalpha():
                word = word[:-1]
            if word.isdigit():
                word = ""

    # clean empty strs
    while ("" in words):
        words.remove("")

    # turn into counter
    return Counter(words)


def create_df_analysis(word_counter: Counter):
    """
    Creates a DataFrame analysis from a word counter.

    This function generates a DataFrame with ranks, words, counts, and frequencies based on the word counter.

    Args:
        word_counter (collections.Counter): A Counter object with word frequencies.

    Returns:
        pandas.DataFrame: A DataFrame containing ranks, words, counts, and frequencies.
    """
    df = pd.DataFrame.from_dict(word_counter, orient="index").reset_index()
    df = df.rename(columns={'index': 'word', 0: 'count'})
    df.insert(2, "rank", 0, True)
    df.insert(3, "freq", 0.1, True)
    df = df.sort_values(by=['count'], ascending=False)
    df = df.reset_index(drop=True)
    total_count = df['count'].sum()

    for row in range(len(df)):
        df.at[row, 'rank'] = row + 1
        df.at[row, 'freq'] = df.at[row, 'count'] / total_count
    df = df.set_index('rank')

    return df

def write_to_csv_file(df, name_book):
    """
    Writes a DataFrame to a CSV file.

    This function saves the DataFrame to a CSV file in the 'csv_output' directory. The filename is based on the book name and the number of rows in the DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame to be saved.
        name_book (str): The name of the book, used for the filename.

    Returns:
        None
    """
    output_dir = 'csv_output'
    os.makedirs(output_dir, exist_ok=True)
    name_out_file = os.path.join(output_dir, name_book + f'_{len(df)}' + '.csv')
    df.to_csv(name_out_file, sep=',')
    ic("created csv file for ", name_book)


if __name__ == "__main__":

    book_titles = [ # these titles can be changed, but must relate to contents of "./assets" directory
        "moby_dick",
        "metamorphosis",
        "pride_and_prejudice",
        "the_great_gatsby",
        "spanish_book",
        "esperanto_book",
        "danish_book",
        "llm_english",
        "llm_danish",
        "llm_spanish",
        "llm_esperanto"
    ]

    for title in book_titles:
        book = read_file(title)
        word_count = prepare_tokens(book)
        df = create_df_analysis(word_count)
        write_to_csv_file(df, title)
