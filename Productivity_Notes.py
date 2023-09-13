import tkinter as tk
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
from tkinter import filedialog
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest
import os

# nltk.download('punkt') <-- Need this to run the program, but only need to download punkt once
# nltk.download('stopwords') <-- Need this to run the program, but only need to download stopwords once
# Function to clear the default text in the URL entry field
def clear_entry(event):
    if url_entry.get() == "Paste URL here":
        url_entry.delete(0, tk.END)
        url_entry.config(fg="black")  # Change text color to black when user starts typing

# Function to scrape and filter the main content of a webpage
def scrape_website():
    url = url_entry.get()
    
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Filter out specific HTML elements (e.g., script, style, iframe, button, a)
        for unwanted_tag in soup(["script", "style", "iframe", "button", "a"]):
            unwanted_tag.extract()

        # Extract and display the text from the remaining content
        text = soup.get_text()

        # Display the text in the result_text widget
        result_text.delete(1.0, tk.END)  # Clear previous content
        result_text.insert(tk.END, text)
    except requests.exceptions.RequestException as e:
        # Handle request errors
        result_text.delete(1.0, tk.END)  # Clear previous content
        result_text.insert(tk.END, f"Error: {str(e)}")

# Function to save the scraped content to a text file
def save_to_file():
    text = result_text.get(1.0, tk.END)
    
    # Prompt the user for a file name and location
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    
    if file_path:
        # Write the text to the selected file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)

# Function to generate a more accurate summary of the scraped content
def generate_summary():
    text = result_text.get(1.0, tk.END)
    
    # Tokenize the text into words and sentences
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    
    # Calculate word frequencies
    word_frequencies = {}
    for word in words:
        if word.isalnum():
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    
    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]
    
    # Get the summary sentences based on sentence scores
    summary_sentences = nlargest(5, sentence_scores, key=sentence_scores.get)
    
    # Generate the summary
    summary = "\n".join(summary_sentences)

    # Display the summary in the result_text widget
    result_text.delete(1.0, tk.END)  # Clear previous content
    result_text.insert(tk.END, summary)

# Function to go back to the homepage
def back_to_home():
    # Destroy the current page
    app.destroy()
    
    # Open the homepage again
    os.system("python Productivity_Home.py")  # Assuming your homepage script is named "homepage.py"

# Create the main application window
app = tk.Tk()
app.title("Web Page Text Scraper")

# Create and pack widgets
tk.Label(app, text="Enter URL:").pack()
url_entry = tk.Entry(app, width=40, fg="gray")
url_entry.insert(0, "Paste URL here")
url_entry.bind("<FocusIn>", clear_entry)  # Bind event to clear entry on focus
url_entry.pack()
scrape_button = tk.Button(app, text="Scrape", command=scrape_website)
scrape_button.pack()

result_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=60, height=20)
result_text.pack()

download_button = tk.Button(app, text="Download as Text", command=save_to_file)
download_button.pack()

summary_button = tk.Button(app, text="Generate Summary", command=generate_summary)
summary_button.pack()

# Add a "Back to Home" button
back_to_home_button = tk.Button(app, text="Back to Home", command=back_to_home)
back_to_home_button.pack()

# Start the application
app.mainloop()
