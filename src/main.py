"""main process."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog

from PIL import Image

import my_logger
import settings

logger = my_logger.my_logger(__name__)

root = tk.Tk()
root.withdraw()

dir_path = filedialog.askdirectory(title="フォルダを選択してください。")
path = Path(dir_path)


patterns = settings.FILE_TYPES
file_list = []
for pattern in patterns:
    for file_path in path.rglob(pattern):
        file_list.append(file_path)  # noqa: PERF402


for file in file_list:
    dst = file.with_suffix(".webp")
    try:
        with Image.open(file) as img:
            img.save(dst, quality=settings.QUALITY)
    except Exception as e:
        logger.exception(e)  # noqa: TRY401

my_logger.shutdown()
