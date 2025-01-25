import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askdirectory
from threading import Thread
from ttkthemes import ThemedTk
import sv_ttk

class FolderAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Space Analyzer")
        self.root.geometry("900x650")

        sv_ttk.set_theme("dark")

        self.create_ui()

    def create_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#282c34")
        title_frame.pack(fill=tk.X, pady=10)
        self.title_label = tk.Label(
            title_frame, text="📂 Folder Space Analyzer", font=("Segoe UI", 18, "bold"), bg="#282c34", fg="#61dafb"
        )
        self.title_label.pack(pady=10)

        # Directory selection
        self.select_btn = ttk.Button(
            self.root, text="Select Directory", command=self.select_directory, style="Accent.TButton"
        )
        self.select_btn.pack(pady=15)

        # Treeview Frame
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Folder", "Size (MB)"), show="headings", height=20)
        self.tree.heading("Folder", text="Folder", anchor=tk.W)
        self.tree.heading("Size (MB)", text="Size (MB)", anchor=tk.CENTER)
        self.tree.column("Folder", width=600, anchor=tk.W)
        self.tree.column("Size (MB)", width=120, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        tree_scroll = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Button Frame
        button_frame = tk.Frame(self.root, bg="#282c34")
        button_frame.pack(fill=tk.X, pady=10)

        self.delete_btn = ttk.Button(
            button_frame, text="Delete Selected Folder", command=self.delete_selected_folder, style="Accent.TButton"
        )
        self.delete_btn.pack(side=tk.RIGHT, padx=15, pady=10)

    def select_directory(self):
        directory = askdirectory()
        if directory:
            self.scan_directory(directory)

    def scan_directory(self, directory):
        self.tree.delete(*self.tree.get_children())

        def scan():
            folder_sizes = []
            for root_dir, dirs, _ in os.walk(directory):
                for dir_name in dirs:
                    folder_path = os.path.join(root_dir, dir_name)
                    size = self.get_folder_size(folder_path) / (1024 * 1024)
                    folder_sizes.append((folder_path, size))

            folder_sizes.sort(key=lambda x: x[1], reverse=True)

            for folder_path, size in folder_sizes:
                self.tree.insert("", tk.END, values=(folder_path, f"{size:.2f}"))

        Thread(target=scan).start()

    @staticmethod
    def get_folder_size(folder):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    def delete_selected_folder(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a folder to delete.")
            return

        folder_path = self.tree.item(selected_item, "values")[0]
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the folder?\n{folder_path}"):
            try:
                shutil.rmtree(folder_path)
                self.tree.delete(selected_item)
                messagebox.showinfo("Success", "Folder deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete folder: {e}")

if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = FolderAnalyzerApp(root)
    root.mainloop()
