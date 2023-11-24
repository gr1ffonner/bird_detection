from tkinter import filedialog, messagebox


def choose_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        messagebox.showinfo("File Path", f"file name is {file_path}")
    return file_path
