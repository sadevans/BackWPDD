from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import time

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_layer = get_channel_layer()
        self.last_event_time = 0
        self.debounce_delay = 1


    def on_modified(self, event):
        print("MODIFIED", event)
        # Triggered on file modification
        # if not event.is_directory:
        print(self.channel_layer)
        if not event.is_directory:
            current_time = time.time()
            # Process event only if the debounce delay has passed
            if current_time - self.last_event_time > self.debounce_delay:
                async_to_sync(self.channel_layer.group_send)(
            'file_watch_group',
            {
                'type': 'send_file_change_notification',
                'message': f'File {event.src_path} has been modified.'
            }
        )

                self.last_event_time = current_time
        



def start_observer(path):
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"Started monitoring changes in {path}")
    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()