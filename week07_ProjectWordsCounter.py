# ---------------------------
# Import necessary libraries
# ---------------------------

import re                              # Regular expressions for text processing.
import pandas as pd                    # Pandas for data manipulation and DataFrame creation.
import matplotlib.pyplot as plt        # Matplotlib for creating visualizations.
from collections import Counter        # Counter to count word frequencies.

# ---------------------------
# Function Definitions
# ---------------------------

def read_file(file_path):
    """
    Reads the entire content of the file specified by file_path.
    
    Parameters:
        file_path (str): The path to the text file.
    
    Returns:
        str: The content of the file as a single string.
             Returns an empty string if the file is not found.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return ""

def process_text(text):
    """
    Processes the input text by:
      - Converting it to lowercase (to count words case-insensitively).
      - Removing punctuation using a regular expression.
      - Splitting the text into individual words.
    
    Parameters:
        text (str): The raw text to process.
    
    Returns:
        list: A list of words extracted from the text.
    """
    # Convert text to lowercase.
    text = text.lower()
    # Remove punctuation: Replace any character that is not a word character or whitespace.
    text = re.sub(r'[^\w\s]', '', text)
    # Split text by whitespace into a list of words.
    words = text.split()
    return words

def count_words(words):
    """
    Counts the frequency of each word in the given list of words.
    
    Parameters:
        words (list): A list of words.
    
    Returns:
        collections.Counter: A dictionary-like object with words as keys and their frequencies as values.
    """
    return Counter(words)

def create_dataframe(word_count):
    """
    Converts a Counter (word count dictionary) into a pandas DataFrame.
    The DataFrame will have two columns: 'Word' and 'Frequency', sorted in descending order by frequency.
    
    Parameters:
        word_count (Counter): The word frequency counts.
    
    Returns:
        pandas.DataFrame: A DataFrame containing the word frequencies.
    """
    # Convert the Counter into a list of (word, frequency) tuples and then into a DataFrame.
    df = pd.DataFrame(word_count.items(), columns=['Word', 'Frequency'])
    # Sort the DataFrame by frequency in descending order.
    df.sort_values(by='Frequency', ascending=False, inplace=True)
    return df

def visualize_word_counts(df, top_n=10):
    """
    Visualizes the top_n most frequent words using a bar chart.
    
    Parameters:
        df (pandas.DataFrame): The DataFrame containing word counts.
        top_n (int): The number of top words to visualize.
    
    This function uses matplotlib to create and display a bar chart.
    """
    # Get the top_n words from the DataFrame.
    top_df = df.head(top_n)
    
    # Create a bar plot.
    plt.figure(figsize=(10, 6))
    plt.bar(top_df['Word'], top_df['Frequency'], color='skyblue')
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Most Frequent Words')
    # Rotate x-axis labels for better readability.
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust layout to prevent clipping of labels.
    plt.show()

def main():
    """
    Main function to tie all the parts together.
    
    Workflow:
      1. Reads a text file.
      2. Processes the text.
      3. Counts word frequencies.
      4. Converts counts into a DataFrame.
      5. Prints the top words.
      6. Visualizes the top words in a bar chart.
    """
    # Specify the path to your text file.
    file_path = "input.csv"  # Make sure you have a file named 'input.txt' in the same directory.
    
    # Step 1: Read the file.
    text = read_file(file_path)
    if not text:
        return  # Exit if the file was not found or is empty.
    
    # Step 2: Process the text (lowercase, remove punctuation, split into words).
    words = process_text(text)
    
    # Step 3: Count the frequency of each word.
    word_count = count_words(words)
    
    # Step 4: Create a pandas DataFrame from the word counts.
    df = create_dataframe(word_count)
    
    # Step 5: Print the top 10 most frequent words to the console.
    print("Top 10 most frequent words:")
    print(df.head(10))
    
    # Step 6: Visualize the word frequencies using a bar chart.
    visualize_word_counts(df, top_n=10)

# ---------------------------
# Entry Point
# ---------------------------

if __name__ == "__main__":
    main()
