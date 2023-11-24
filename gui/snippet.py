import tkinter as tk
from tkinter import ttk
import time


def run_progressbar():
    progress_window = tk.Toplevel(root)
    progress_window.title("Progress Window")
    progress_window.geometry("300x100")

    progress_label = ttk.Label(progress_window, text="Processing...")
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(
        progress_window, orient=tk.HORIZONTAL, length=200, mode="determinate"
    )
    progress_bar.pack(pady=10)

    # Simulate a process that updates the progress bar
    for i in range(1, 101):
        time.sleep(0.1)  # Simulate some processing time
        progress_bar["value"] = i
        progress_window.update_idletasks()

    progress_label.config(text="Process complete!")


root = tk.Tk()
root.title("Progress Bar Example")

button = ttk.Button(root, text="Run Progress Bar", command=run_progressbar)
button.pack(pady=20)

root.mainloop()
