import platform
import torch
from utils.log import Logger

logger = Logger(__file__)

VALID_DEVICE = ["cpu", "mps", "cuda", "cuda:0", "cuda:1..."]


def get_device(device: str) -> str:
    """단일 디바이스를 문자열로 리턴한다. None이 입력으로 들어올 시 자동으로 device를 하나 지정한다."""
    if device is None:
        # 지정안된 경우 자동 지정
        if platform.system() == "Darwin":
            return "mps"
        else:
            return "cuda" if torch.cuda.is_available() else "cpu"

    else:
        return device