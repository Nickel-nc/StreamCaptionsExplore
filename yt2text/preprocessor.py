import os
from glob import glob
import subprocess
from speech_engine import SpeechEngine

from pytube import YouTube


class YT2Text():
    """
    # 1. Extract YT audio stream
    # 2. Convert format
    # 3. Perform wav transcription
    """

    def __init__(self, download_dir='/downloads'):

        self.current_dir = os.getcwd()
        self.download_path = self.current_dir + download_dir
        self.check_file_structure()

    def check_file_structure(self):
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def clear_temp_folder(self):
        if os.path.exists(self.download_path):
            files = glob(f'{self.download_path}/*')
            for f in files:
                os.remove(f)

    def download_audio_stream(self, url):

        yt = YouTube(url=url)
        yt.streams.filter(only_audio=True).all()[0].download(self.download_path)

        full_name = os.listdir(self.download_path)[0]
        self.fn, self.init_ext = full_name.split('.')

    def format_converter(self, target_ext='wav'):
        # convert to proper format
        self.cp_source = f'"{self.download_path}/{self.fn}.{self.init_ext}"'
        self.cp_dest = f'"{self.download_path}/{self.fn}.{target_ext}"'

        command = f"ffmpeg -i {self.cp_source} -ab 160k -ac 1 -ar 16000 -vn {self.cp_dest}"
        subprocess.call(command, shell=True)

    def run(self, url):
        try:
            self.download_audio_stream(url)
            self.format_converter()
            sm = SpeechEngine()
            result = sm.wav2vec(self.cp_dest.replace("\"", ""))
            # result = get_large_audio_transcription(self.cp_dest.replace("\"", ""))
        except Exception as e:
            raise e
        # self.clear_temp_folder()
        return result






