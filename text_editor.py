import tkinter as tk
from tkinter import filedialog, messagebox

class TextEditor:
    def __init__(self, master):
        self.master = master
        master.title("Simple Text Editor")

        self.text_area = tk.Text(master)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.master.config(menu=menubar)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        filepath = filedialog.askopenfilename(defaultextension=".txt")
        if filepath:
            try:
                with open(filepath, "r") as f:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, f.read())
            except:
                messagebox.showerror("Error", "Failed to open file")

    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        if filepath:
            try:
                with open(filepath, "w") as f:
                    f.write(self.text_area.get(1.0, tk.END))
            except:
                messagebox.showerror("Error", "Failed to save file")

root = tk.Tk()
text_editor = TextEditor(root)
root.mainloop()
