import glob
import os
from pathlib import Path
from typing import Union


VIDEO_EXTS = ["mp4", "avi"]
LABEL_EXTS = ["json"]


def get_videos_labels(dir: Union[str, Path]) -> list[str]:
    """폴더 경로로부터 비디오 경로를 리스트로 가져온다. 가져올 수 있는 form은 VIDEO_EXTS에 존재하는 확장자이다.
    Args:
        dir (Union[str,Path]): folder path including video files
    Returns:
        list[str]: video path list
    """
    dir = str(dir)
    file_list = glob.glob(dir + os.sep + "**", recursive=True)
    video_list = [x for x in file_list if x.split(".")[-1] in VIDEO_EXTS]
    label_list = [x for x in file_list if x.split(".")[-1] in LABEL_EXTS]
    return video_list, label_list