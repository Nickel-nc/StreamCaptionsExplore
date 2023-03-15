import logging
import os
from typing import Any, Optional

from pytube import YouTube

from video.captions import Caption


_logger = logging.getLogger(__name__)


def on_complete(stream: Any, file_path: Optional[str]):
    _logger.info("Downloaded successfully.")


def download_video_and_subtitles(url: str, destination_path: str) -> str:
    yt = YouTube(url, on_complete_callback=on_complete, use_oauth=False)

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
        _logger.debug("Destination folder for downloaded file was created.")
    file_path = yt.streams.filter(file_extension="mp4", res="720p").first().download(destination_path)

    # write subtitles of video file
    for caption in yt.captions:
        for method in ["download", "xml_caption_to_srt", "generate_srt_captions", "float_to_srt_time_format"]:
            setattr(caption, method, getattr(Caption, method))

        caption.download(caption, title=caption.name, output_path=destination_path)

    return file_path
