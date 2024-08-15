import re
from pathlib import Path
from typing import Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .notify import Notifier
import time


class FileWatherHandler(FileSystemEventHandler):

    def __init__(self, pattern: Optional[str] = None):
        self.ntf = Notifier()
        self.pattern = pattern

    def on_created(self, event):
        path = Path(event.src_path)
        if self.pattern is None or re.match(self.pattern, path.name):
            self.ntf(f'event type: {event.event_type} path : {event.src_path}')


def watch_file(path: Path, pattern: Optional[str] = None):
    event_handler = FileWatherHandler(pattern=pattern)
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
