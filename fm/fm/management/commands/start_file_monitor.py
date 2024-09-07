from django.core.management.base import BaseCommand
from .file_monitor import start_observer

class Command(BaseCommand):
    help = 'Start file monitor to watch for file changes.'

    def handle(self, *args, **kwargs):
        # Specify the path to the file or directory you want to monitor
        path_to_watch = '/home/sadevans/space/personal/BackWPDD/testfolder/file.txt'
        start_observer(path_to_watch)