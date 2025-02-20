# Copyright 2020, Brigham Young University-Idaho. All rights reserved.

import pytest
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Import functions from your module (adjust the module name if needed)
from week07_ProjectWordsCounter import (
    read_file,
    process_text,
    count_words,
    create_dataframe,
    visualize_word_counts,
    main
)

# ---------------------------
# Test for read_file
# ---------------------------
def test_read_file(tmp_path):
    """
    Verify that read_file correctly reads a file's contents.
    """
    # Create a temporary file with known content.
    content = "Hello world! This is a test file."
    file = tmp_path / "test.txt"
    file.write_text(content, encoding="utf-8")
    # Call read_file with the temporary file's path.
    result = read_file(str(file))
    assert result == content, "read_file did not return the expected content."


def test_read_file_not_found(monkeypatch, capsys):
    """
    Verify that read_file handles non-existent files by printing an error and returning an empty string.
    """
    non_existent = "nonexistent_file.txt"
    result = read_file(non_existent)
    assert result == "", "Expected empty string when file not found."
    # Capture printed output
    captured = capsys.readouterr().out
    assert f"Error: The file '{non_existent}' was not found." in captured, "Error message not printed correctly."


# ---------------------------
# Test for process_text
# ---------------------------
def test_process_text():
    """
    Verify that process_text converts text to lowercase, removes punctuation, and splits into words.
    """
    text = "Hello, World! This is a Test."
    expected = ["hello", "world", "this", "is", "a", "test"]
    result = process_text(text)
    assert result == expected, "process_text did not return the expected list of words."


# ---------------------------
# Test for count_words
# ---------------------------
def test_count_words():
    """
    Verify that count_words returns a Counter with correct word frequencies.
    """
    words = ["hello", "world", "hello", "test"]
    result = count_words(words)
    expected = Counter({"hello": 2, "world": 1, "test": 1})
    assert result == expected, "count_words did not count word frequencies correctly."


# ---------------------------
# Test for create_dataframe
# ---------------------------
def test_create_dataframe():
    """
    Verify that create_dataframe converts a Counter to a DataFrame with sorted columns.
    """
    word_count = Counter({"hello": 2, "world": 1, "test": 3})
    df = create_dataframe(word_count)
    # The DataFrame should have two columns: "Word" and "Frequency"
    assert list(df.columns) == ["Word", "Frequency"], "DataFrame columns are not as expected."
    # Check that the DataFrame is sorted in descending order by Frequency.
    assert df.iloc[0]["Word"] == "test" and df.iloc[0]["Frequency"] == 3, "DataFrame is not sorted correctly."


# ---------------------------
# Test for visualize_word_counts
# ---------------------------
def test_visualize_word_counts(monkeypatch):
    """
    Verify that visualize_word_counts calls plt.show (using monkeypatch to prevent plot display).
    """
    called = False
    def dummy_show():
        nonlocal called
        called = True
    monkeypatch.setattr(plt, "show", dummy_show)
    
    # Create a sample DataFrame.
    df = pd.DataFrame({
        "Word": ["hello", "world", "test"],
        "Frequency": [5, 3, 2]
    })
    visualize_word_counts(df, top_n=2)
    assert called, "plt.show was not called in visualize_word_counts."


# ---------------------------
# Test for main()
# ---------------------------
def test_main(monkeypatch, capsys):
    """
    Verify that main() runs without error and prints expected output.
    
    Monkeypatch read_file to return a known text,
    and monkeypatch visualize_word_counts to avoid displaying a plot.
    """
    # Override read_file to return test text regardless of file input.
    monkeypatch.setattr("word_counter.read_file", lambda file_path: "Hello world! Hello test.")
    # Override visualize_word_counts to do nothing.
    monkeypatch.setattr("word_counter.visualize_word_counts", lambda df, top_n=10: None)
    
    # Run main() and capture printed output.
    main()
    captured = capsys.readouterr().out
    assert "Top 10 most frequent words:" in captured, "main() did not print expected output."
    

# Run the tests when this file is executed directly.
if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])
