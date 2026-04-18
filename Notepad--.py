import sys, os
from tkinter import Tk
import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import keyboard

def resource_path(relative_path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)

root = Tk()
root.geometry("600x300")
root.title("Notepad--")
root.iconbitmap(resource_path("icon.ico"))

tkinter.Grid.rowconfigure(root,0,weight=1)
tkinter.Grid.columnconfigure(root,0,weight=1)

content = ""
docpath = ""
filename = ""

root.tk.call('source', resource_path('forest-dark.tcl'))
ttk.Style().theme_use('forest-dark')

def OpenFile():
    global docpath, content, filename
    File = filedialog.askopenfilename()
    print(File)
    if File != "":
        if content != TextBox.get(1.0, "end"):
            response = messagebox.askyesnocancel("Save", "The current file has not been saved. Would you like to save it?")
            if response == True:
                Save()
        try:
            r = open(File)
            r = r.read()
            content = r
            docpath = File
            filename = os.path.basename(docpath)
            root.title(filename+" - Notepad--")
            TextBox.delete(1.0, "end")
            TextBox.insert("end", content)
        except FileNotFoundError:
            messagebox.showerror("File not found", "The specified file could not be found.")

def SaveAs():
    global docpath, filename
    File = filedialog.asksaveasfilename()
    if File != "":
        try:
            r = open(File)
            r = r.read()
            docpath = File
            filename = os.path.basename(docpath)
            root.title(filename+" - Notepad--")
            Save()
        except FileNotFoundError:
            messagebox.showerror("File not found", "The specified file could not be found.")


def Save():
    global content, docpath
    if content != TextBox.get(1.0, "end"):
        if docpath == "":
            SaveAs()
        else:
            content = TextBox.get(1.0, "end")
            w = open(docpath, "w")
            w.write(content)
            messagebox.showinfo("Saved", "Saved as "+filename)
    else:
        messagebox.showinfo("Did not save", "No changes were detected.")


MenuBar = tkinter.Menu(root)
FileMenu = tkinter.Menu(MenuBar, tearoff=0)
FileMenu.add_command(label="Open", command=OpenFile)
FileMenu.add_command(label="Save (CTRL+S)", command=Save)
FileMenu.add_command(label="Save As", command=SaveAs)
MenuBar.add_cascade(label="File", menu=FileMenu)
root.config(menu=MenuBar)

TextBox = tkinter.Text(
    root,
)
TextBox.grid(row=0,column=0,sticky="NSEW")

print(str(sys.argv))

if len(sys.argv) >= 2:
    try:
        content = open(sys.argv[1])
        File = sys.argv[1]
        content = content.read()
        docpath = File
        filename = os.path.basename(docpath)
        TextBox.delete(1.0, "end")
        TextBox.insert("end", content)
    except FileNotFoundError:
        messagebox.showerror("File not found", "The specified file could not be found.")

keyboard.add_hotkey("ctrl+s", Save)

root.mainloop()