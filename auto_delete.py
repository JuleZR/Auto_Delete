"""Auto Clean download Folder with Python"""


import os
from datetime import datetime, timedelta
from send2trash import send2trash


class AutoDelte:
    def __init__(self, directory: str):
        file_list = [f for f in os.listdir(directory)]
        for file in file_list:
            if os.path.isdir(directory + file):
                continue
            last_modified = datetime.fromtimestamp(
                os.path.getmtime(directory + file)
                )
            now = datetime.now()
            t_delta = timedelta(-30)
            date_threshold = now + t_delta
            if date_threshold > last_modified:
                dump_file = (directory + file).replace('/', "\\")
                send2trash(dump_file)
                print(f"{file} was deleted.")


def main(directory: str):
    AutoDelte(directory)


if __name__ == '__main__':
    main('D:/Downloads/')
