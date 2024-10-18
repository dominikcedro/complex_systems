"""
author: Dominik Cedro
date: 15.10.2024
description: Complex systems, lab 1. This file contains solutions to task 3, LLM comparison to literature (a and b params)
"""

from matplotlib import pyplot as plt
from lab1.task_1_english_books import create_dfs_from_csvs
from lab1.task_2_languages import fit_parameters_extract, BOOK_TITLES_TASK_2

BOOK_TITLES_TASK_3 = [ # task with LLM generated text
    "llm_english",
    "llm_danish",
    "llm_spanish",
    "llm_esperanto"
]


if __name__ == "__main__":
    list_dfs_task_2 = create_dfs_from_csvs(BOOK_TITLES_TASK_2)
    plt.figure(figsize=(10, 6))

    for df, book_title in zip(list_dfs_task_2, BOOK_TITLES_TASK_2):
        language_a, language_b = fit_parameters_extract(df,book_title)
        x_pos = BOOK_TITLES_TASK_2.index(book_title) * 2 + 1
        plt.scatter([x_pos, x_pos], [language_a, language_b], label=book_title)
        plt.text(x_pos, language_a, f'a: {language_a:.2f}', fontsize=9, ha='right')
        plt.text(x_pos, language_b, f'b: {language_b:.2f}', fontsize=9, ha='right')

    list_dfs_task_3 = create_dfs_from_csvs(BOOK_TITLES_TASK_3)

    for df, book_title in zip(list_dfs_task_3, BOOK_TITLES_TASK_3):
        language_a, language_b = fit_parameters_extract(df,book_title)
        x_pos = BOOK_TITLES_TASK_3.index(book_title) * 2 + 2
        plt.scatter([x_pos, x_pos], [language_a, language_b], label=book_title)
        plt.text(x_pos, language_a, f'a: {language_a:.2f}', fontsize=9, ha='right')
        plt.text(x_pos, language_b, f'b: {language_b:.2f}', fontsize=9, ha='right')

    all_titles = [title for pair in zip(BOOK_TITLES_TASK_2, BOOK_TITLES_TASK_3) for title in pair]
    plt.xticks(range(1, len(all_titles) + 1), all_titles, rotation=45)
    plt.xlabel('Language')
    plt.ylabel('Parameter Value')
    plt.title('Zipf-Mandelbrot Parameters for Different Languages (Books vs LLM)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()