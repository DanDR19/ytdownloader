from time import sleep
import pytube
import logging
import subprocess
from os import path
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

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
        self.__temp_dir = "./temp"
        self.__files_dir = download_path

    def _download_audio(self, yt):
        title = yt.title
        logger.info(f"Downloading 'AUDIO' for [{title}]")
        stream = yt.streams.filter(only_audio=True, file_extension='mp4')[0]
        stream.download(output_path=f"{self.__files_dir}/mp3", filename=f"{title}.mp3")
    
    def _merge_audio_video(self, video_name):
        command = ["ffmpeg", "-nostdin", "-y", "-i", f"{self.__files_dir}/mp4/{video_name}_no_audio.mp4", "-i", f"{self.__files_dir}/mp3/{video_name}.mp3", "-c:v", "copy", "-c:a", "aac", f"{self.__files_dir}/mp4/{video_name}.mp4"]
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

        attempts = 0
        while not path.exists(f"{self.__files_dir}/mp4/{video_name}.mp4") and attempts < 30:
            sleep(1)
            attempts += 1
        
        logger.info(f"Finished merging audio and video for [{video_name}] -- Removing temporary files")
        subprocess.Popen(["rm", f"{self.__files_dir}/mp4/{video_name}_no_audio.mp4"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)


    def _download_video(self, yt):
        title = yt.title
        logger.info(f"Downloading 'VIDEO' for [{title}]")
        try:
            stream = yt.streams.get_by_itag(137)
            stream.download(output_path=f"{self.__files_dir}/mp4", filename=f"{title}_no_audio.mp4")
            self._merge_audio_video(title)
        except Exception as e:
            logger.error(f"There is not 1080p resolution available for this video... Omitting video download - {e}")
    
    def download(self):
        url_list = []
        with open(self.__url_list_file, 'r') as f:
            url_list = f.readlines()

        for url in url_list:
            yt = pytube.YouTube(url)
            self._download_audio(yt)
            self._download_video(yt)

if __name__ == "__main__":
    # dialogs = Dialogs()
    # file = dialogs.select_file(allowed_types='*.txt', title="Select file that contains urls")
    # directory = dialogs.select_directory(title="Select directory where files will be downloaded")

    file = "url_list.txt"
    directory = "./files"

    downloader = YTDownloader(file, directory)
    downloader.download()