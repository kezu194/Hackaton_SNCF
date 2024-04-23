import os
from pathlib import Path

AUDIO_DIR = Path(__file__).parent.parent.parent.joinpath('assets/sounds')


def get_first_file() -> Path:
    """
    Get first file path from the assets/sounds directory.

    :return: The Path of the file
    """

    first_file = os.listdir(AUDIO_DIR)[0]
    file_path = AUDIO_DIR / first_file
    return file_path
