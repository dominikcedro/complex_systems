"""
author: Dominik Cedro
date: 15.10.2024
description: Complex systems, lab 1. This file contains solutions to task 2, where parameters a and b were sought
"""
from icecream import ic
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from task_1_english_books import create_dfs_from_csvs, calculate_theoritical_zipf

BOOK_TITLES_TASK_2 = [ # task about describing languages by a and b parameters
    "moby_dick",
    "spanish_book",
    "esperanto_book",
    "danish_book",
    # "russian_book",
    # "hebrew_book"
]

def zipf_mandelbrot(rank, a, b):
    """
    Simple function representing zipf mandelbrot law output

    Args:
        rank (int): rank of chosen word
        a (float): a parameter for zipf mandelbrot equation
        b (float): b parameter for zipf mandelbrot equation

    Returns:
        result (float): a result for zipf mandelbrot equation
    """
    return 1 / (rank + b) ** a

def fit_parameters_extract(df, title):
    """
    Fits a and b parameters from zipf mandelbrot notation to specific df

    Args:
        df (pandas.DataFrame): The DataFrame for operation.
        title (str): The name of the book.

    Returns:
        tuple: A tuple containing the fitted parameters a and b.
    """
    ic(df.head())
    popt_lang, _ = curve_fit(zipf_mandelbrot, df['rank'], df['freq'])
    a, b = popt_lang
    ic(title)
    ic(f"Parameters are: 'a': {a}, 'b': {b}")
    return a, b

if __name__ == "__main__":
    list_dfs_task_2 = create_dfs_from_csvs(BOOK_TITLES_TASK_2)

    plt.figure(figsize=(10, 6))

    for df, book_title in zip(list_dfs_task_2, BOOK_TITLES_TASK_2):
        ic(book_title)
        ic(df.head())
        language_a, language_b = fit_parameters_extract(df, book_title)
        x_pos = BOOK_TITLES_TASK_2.index(book_title) + 1
        plt.scatter([x_pos, x_pos], [language_a, language_b], label=book_title)
        plt.text(x_pos, language_a, f'a: {language_a:.2f}', fontsize=9, ha='right')
        plt.text(x_pos, language_b, f'b: {language_b:.2f}', fontsize=9, ha='right')

    plt.xticks(range(1, len(BOOK_TITLES_TASK_2) + 1), BOOK_TITLES_TASK_2)
    plt.xlabel('Language')
    plt.ylabel('Parameter Value')
    plt.title('Zipf-Mandelbrot Parameters for Different Languages')
    plt.legend()
    plt.grid(True)
    plt.show()