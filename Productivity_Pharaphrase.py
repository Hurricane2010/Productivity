import tkinter as tk
from textblob import TextBlob

# Function to paraphrase the input text
def paraphrase_text():
    input_text = input_textbox.get("1.0", "end-1c")  # Get the input text from the textbox
    if input_text:
        # Use TextBlob for paraphrasing (you may need to install the TextBlob library)
        try:
            blob = TextBlob(input_text)
            paraphrased_text = str(blob.translate(to="en"))  # Translate to English as a paraphrasing method
            output_textbox.delete("1.0", tk.END)  # Clear previous output
            output_textbox.insert("1.0", paraphrased_text)
        except Exception as e:
            output_textbox.delete("1.0", tk.END)  # Clear previous output
            output_textbox.insert("1.0", f"Error: {str(e)}")
    else:
        output_textbox.delete("1.0", tk.END)  # Clear previous output
        output_textbox.insert("1.0", "Input text is empty.")

# Create the main application window
app = tk.Tk()
app.title("Paraphrase Tool")

# Create and pack widgets
tk.Label(app, text="Enter Text to Paraphrase:").pack()
input_textbox = tk.Text(app, wrap=tk.WORD, width=60, height=5)
input_textbox.pack()

paraphrase_button = tk.Button(app, text="Paraphrase", command=paraphrase_text)
paraphrase_button.pack()

output_textbox = tk.Text(app, wrap=tk.WORD, width=60, height=5)
output_textbox.pack()

# Start the application
app.mainloop()
