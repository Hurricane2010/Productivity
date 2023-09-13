import tkinter as tk
import os

def open_note_taking_app():
    # Close the homepage GUI
    app.destroy()
    
    # Run the note-taking app script
    os.system("python Productivity_Notes.py")

app = tk.Tk()
app.title("Homepage")

note_button = tk.Button(app, text="Note-taking App", command=open_note_taking_app)
note_button.pack()

# Add more buttons for other apps/options as needed

app.mainloop()
