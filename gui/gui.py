import tkinter as tk
from tkinter import ttk
from helpers import choose_file
from logic.show_out_gui import show_out
from logic.save_out import save_out
from logic.img import save_image, show_image
from tkinter import messagebox

# Main class
class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bird Detection")
        self.root.geometry("600x400")
        self.file_path = None
        self.video_label = ttk.Label(self.root)
        self.video_label.grid(column=0, row=0, columnspan=2)
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure(
            "TButton",
            font=("Helvetica", 14),
            foreground="#ffffff",
            background="#4CAF50",
            padding=(10, 10),
        )

        style.configure("TProgressbar", troughcolor="#ffffff", background="#4CAF50")

        self.index_frame = ttk.Frame(self.root, style="TFrame")
        self.index_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Button(
            self.index_frame,
            text="Images",
            style="TButton",
            command=lambda: self.show_actions_frame("img"),
            compound=tk.CENTER,
        ).pack(pady=5)
        ttk.Button(
            self.index_frame,
            text="Videos",
            style="TButton",
            command=lambda: self.show_actions_frame("vid"),
            compound=tk.CENTER,
        ).pack(pady=5)
        ttk.Button(
            self.index_frame,
            text="Quit",
            style="TButton",
            command=self.root.destroy,
            compound=tk.CENTER,
        ).pack(pady=5)

    def show_actions_frame(self, media_type):
        # Destroy the index frame
        self.index_frame.destroy()

        self.actions_frame = ttk.Frame(self.root, style="TFrame")
        self.actions_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Button(
            self.actions_frame,
            text="Choose File",
            style="TButton",
            command=self.choose_and_store_file_path,
        ).pack(pady=5)
        if media_type == "vid":
            ttk.Button(
                self.actions_frame,
                text="Show Output",
                style="TButton",
                command=self.show_video_output,
            ).pack(pady=5)
            ttk.Button(
                self.actions_frame,
                text="Save Output",
                style="TButton",
                command=self.save_video_output,
            ).pack(pady=5)
        if media_type == "img":
            ttk.Button(
                self.actions_frame,
                text="Show Output",
                style="TButton",
                command=lambda: show_image(self.file_path),
            ).pack(pady=5)
            ttk.Button(
                self.actions_frame,
                text="Save Output",
                style="TButton",
                command=lambda: save_image(self.file_path, self.root),
            ).pack(pady=5)
        ttk.Button(
            self.actions_frame,
            text="Back",
            style="TButton",
            command=lambda: self.destroy_create_frame(
                self.actions_frame, self.create_widgets
            ),
        ).pack(pady=5)

    def destroy_create_frame(self, destroyed_frame, create_frame):
        destroyed_frame.destroy()
        create_frame()

    def choose_and_store_file_path(self):
        self.file_path = choose_file()

    def show_video_output(self):
        if not self.file_path:
            messagebox.showinfo("Error", "Please choose a file first.")
            return
        show_out(self.root, self.file_path)

    def save_video_output(self):
        if not self.file_path:
            messagebox.showinfo("Error", "Please choose a file first.")
            return
        try:
            save_out(self.file_path, self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopApp(root)
    root.mainloop()
