import pytube
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger(__name__)

class Dialogs:
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()
    
    def select_file(self, allowed_types, title):
        return askopenfilename(filetypes=[('Allowed Types', allowed_types)], title=title)
    
    def select_directory(self, title):
        return askdirectory(title=title)

class YTDownloader:
    def __init__(self, url_list_file, download_path="./files"):
        self.__url_list_file = url_list_file
        self.__files_dir = download_path

    def _download_audio(self, yt):
        title = yt.title
        logger.info(f"Downloading 'mp3' for [{title}]")
        stream = yt.streams.filter(only_audio=True, file_extension='mp4')[0]
        stream.download(output_path=f"{self.__files_dir}/mp3", filename=f"{title}.mp3")

    def _download_video(self, yt):
        title = yt.title
        logger.info(f"Downloading 'mp4' for [{title}]")
        try:
            stream = yt.streams.get_by_itag(137)
            stream.download(output_path=f"{self.__files_dir}/mp4", filename=f"{title}.mp4")
        except Exception as e:
            logger.error("There is not 1080 resolution")
    
    def download(self):
        url_list = []
        with open(self.__url_list_file, 'r') as f:
            url_list = f.readlines()

        for url in url_list:
            yt = pytube.YouTube(url)
            self._download_audio(yt)
            self._download_video(yt)

if __name__ == "__main__":
    dialogs = Dialogs()
    file = dialogs.select_file(allowed_types='*.txt', title="Select file that contains urls")
    directory = dialogs.select_directory(title="Select directory where files will be downloaded")

    downloader = YTDownloader(file, directory)
    downloader.download()