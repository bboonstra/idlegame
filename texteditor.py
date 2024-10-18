import tkinter as tk
from tkinter import scrolledtext

class NanobotEditor:
    def __init__(self, master):
        self.master = master
        master.title("Nanobot Logic Editor")

        self.text_area = scrolledtext.ScrolledText(master, width=60, height=20)
        self.text_area.pack(pady=10)

        self.save_button = tk.Button(master, text="Save Logic", command=self.save_logic)
        self.save_button.pack(pady=5)

        self.load_button = tk.Button(master, text="Load Logic", command=self.load_logic)
        self.load_button.pack(pady=5)

    def save_logic(self):
        with open('nanobot_logic.txt', 'w') as file:
            file.write(self.text_area.get("1.0", tk.END))

    def load_logic(self):
        try:
            with open('nanobot_logic.txt', 'r') as file:
                self.text_area.delete("1.0", tk.END)  # Clear the text area
                self.text_area.insert(tk.END, file.read())  # Load saved logic
        except FileNotFoundError:
            self.text_area.insert(tk.END, "No saved logic found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NanobotEditor(root)
    root.mainloop()
