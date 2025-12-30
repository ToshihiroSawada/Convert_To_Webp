"""main process."""

import os
import time
import tkinter as tk
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from tkinter import filedialog

import psutil
from PIL import Image

import my_logger
import settings

logger = my_logger.my_logger(__name__)


def convert_image(file: Path) -> None:
    """1ファイル処理(子プロセス側)"""
    # CPU使用コア制限(例: 最初のNコアのみ)
    p = psutil.Process(os.getpid())
    p.cpu_affinity(list(range(settings.MAX_WORKERS)))

    try:
        with Image.open(file) as img:
            start = time.time()

            dst = file.with_suffix(".webp")
            img.save(dst, quality=settings.QUALITY)

            # 擬似CPU制限
            elapsed = time.time() - start
            sleep_time = elapsed * (1 - settings.CPU_LOAD) / settings.CPU_LOAD
            if sleep_time > 0:
                time.sleep(sleep_time)

    except Exception as e:
        logger.exception(e)  # noqa: TRY401


def main() -> None:  # noqa: D103
    root = tk.Tk()
    root.withdraw()

    dir_path = filedialog.askdirectory(title="フォルダを選択してください")
    if not dir_path:
        return

    path = Path(dir_path)
    patterns = settings.FILE_TYPES

    files = []
    for ptn in patterns:
        files.extend(path.rglob(ptn))

    if not files:
        return

    with ProcessPoolExecutor(max_workers=settings.MAX_WORKERS) as executor:
        executor.map(convert_image, files)


if __name__ == "__main__":
    main()
    my_logger.shutdown()
