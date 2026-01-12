"""GUI components."""

import time
import tkinter as tk
from tkinter import filedialog, ttk


class AppGui:
    """Manage Application GUI."""

    def __init__(self) -> None:
        """Initialize the GUI."""
        self.root = tk.Tk()
        self.root.withdraw()
        self.pbar: ttk.Progressbar | None = None
        self.label: tk.Label | None = None
        self.total: int = 0
        self.start_time: float = 0.0

    def select_directory(self) -> str:
        """Open dialog to select directory."""
        return filedialog.askdirectory(title="フォルダを選択してください")

    def setup_progress(self, total: int) -> None:
        """Initialize and show progress bar."""
        self.total = total
        self.start_time = time.time()
        self.root.deiconify()
        self.root.title("変換中...")
        self.root.geometry("500x150")
        self.pbar = ttk.Progressbar(self.root, maximum=total, mode="determinate")
        self.pbar.pack(fill=tk.X, padx=20, pady=20, ipady=10)
        self.label = tk.Label(self.root, text=f"0 / {total}")
        self.label.pack(pady=5)

    def update_progress(self, value: int) -> None:
        """Update progress bar value and refresh window."""
        if self.pbar:
            self.pbar["value"] = value

        if self.label:
            elapsed = time.time() - self.start_time
            if value > 0:
                per_item = elapsed / value
                remaining = (self.total - value) * per_item
                self.label.config(
                    text=f"{value} / {self.total} (残り: {remaining:.1f}秒)"
                )
            else:
                self.label.config(text=f"{value} / {self.total} (計算中...)")

        self.root.update()

    def close(self) -> None:
        """Close the GUI."""
        self.root.destroy()
