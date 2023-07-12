from tkinter import *
from tkinter import filedialog, messagebox, simpledialog, font


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete(1.0, END)
            text_area.insert(END, file.read())
        root.title("Text - " + file_path)

def save_file():
    file_path = filedialog.asksaveasfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, END))
        root.title("Notepad - " + file_path)
        messagebox.showinfo("Save", "File saved successfully!!!!")

def exit_app():
    if messagebox.askokcancel("Exit", "Are you want to exit?"):
        root.destroy()

def undo():
    try:
        text_area.edit_undo()
    except Exception:
        pass

def redo():
    try:
        text_area.edit_redo()
    except Exception:
        pass

def cut():
    text_area.event_generate("<<Cut>>")

def copy():
    text_area.event_generate("<<Copy>>")

def paste():
    text_area.event_generate("<<Paste>>")

def select_all():
    text_area.tag_add(SEL, "1.0", END)
    text_area.mark_set(INSERT, "1.0")
    text_area.see(INSERT)

def find_text():
    search_text = simpledialog.askstring("Find", "Enter text:")
    if search_text:
        start_pos = text_area.search(search_text, "1.0", stopindex=END)
        if start_pos:
            end_pos = f"{start_pos}+{len(search_text)}c"
            text_area.tag_add(SEL, start_pos, end_pos)
            text_area.mark_set(INSERT, start_pos)
            text_area.see(INSERT)
        else:
            messagebox.showinfo("Find", "Text not found.")

def replace_text():
    search_text = simpledialog.askstring("Replace", "Enter text:")
    if search_text:
        replace_text = simpledialog.askstring("Replace", "Enter text:")
        if replace_text:
            start_pos = text_area.search(search_text, "1.0", stopindex=END)
            if start_pos:
                end_pos = f"{start_pos}+{len(search_text)}c"
                text_area.delete(start_pos, end_pos)
                text_area.insert(start_pos, replace_text)
                messagebox.showinfo("Replace", "Text replaced.")
            else:
                messagebox.showinfo("Replace", "Text not found.")

def word_count():
    content = text_area.get(1.0, END)
    word_list = content.split()
    word_count = len(word_list)
    messagebox.showinfo("Word Count", f"Word count: {word_count}")


root = Tk()
root.title("Text")
root.geometry("800x800")
text_area = Text(root, wrap=WORD, undo=True)
text_area.pack(expand=True, fill=BOTH)
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all)
edit_menu.add_separator()
edit_menu.add_command(label="Find", command=find_text)
edit_menu.add_command(label="Replace", command=replace_text)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

view_menu = Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Word Count", command=word_count)
menu_bar.add_cascade(label="View", menu=view_menu)

root.config(menu=menu_bar)

root.mainloop()