import logging
from pathlib import Path

import ffmpeg
from ffmpeg import Error


_logger = logging.getLogger(__name__)


def get_wav_audio(video_path: str) -> str:
    audio_path = Path(video_path).with_suffix(".wav")
    try:
        ffmpeg.input(video_path).output(str(audio_path)).run(overwrite_output=True)
    except Error:
        _logger.warning("Music wasn't extracted in the Video.")
    return audio_path
