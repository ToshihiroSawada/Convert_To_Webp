"""main process."""

import os
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import psutil
from PIL import Image, ImageFile

import gui
import my_logger
import settings

ImageFile.LOAD_TRUNCATED_IMAGES = True
logger = my_logger.my_logger(__name__)
start_time = datetime.now(ZoneInfo("Asia/Tokyo"))


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

    except Exception:
        logger.exception("file: %s", file)


def main() -> None:  # noqa: D103
    app = gui.AppGui()

    try:
        dir_path = app.select_directory()
        if not dir_path:
            return

        path = Path(dir_path)
        patterns = settings.FILE_TYPES

        if isinstance(patterns, str):
            patterns = [patterns]

        files = []
        for ptn in patterns:
            files.extend([p for p in path.rglob(ptn) if p.is_file()])

        if not files:
            return

        app.setup_progress(len(files))

        with ProcessPoolExecutor(max_workers=settings.MAX_WORKERS) as executor:
            futures = [executor.submit(convert_image, f) for f in files]
            while True:
                done = sum(f.done() for f in futures)
                app.update_progress(done)
                if done == len(files):
                    break

    finally:
        app.close()

    end_time = datetime.now(ZoneInfo("Asia/Tokyo"))

    logger.info("\n\n")
    logger.info("start_time: %s", str(start_time))
    logger.info("end_time: %s", end_time)
    logger.info("Execution time: %s", str(end_time - start_time))


if __name__ == "__main__":
    main()
    my_logger.shutdown()
