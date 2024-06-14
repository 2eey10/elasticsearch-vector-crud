import clip4clip as c4
import cv2
from typing import List, Tuple, Union
import numpy as np
import torch
from torchvision.transforms import (
    CenterCrop,
    Compose,
    InterpolationMode,
    Normalize,
    Resize,
    ToTensor,
)
from PIL import Image
import tqdm
from utils.log import Logger
logger = Logger(__file__)

class Clip4Clip:
    def __init__(self, device=None, model_file=None):
        self._model = None
        self._device = device
        self._model_file = model_file
        self._load_model()

    def process_video(self, video: np.ndarray, size: int) -> torch.Tensor:
        """
        for each frame in video, to resize, crop, and normalize
        then combine them into one 4D tensor (#frame, 3, size, size)
        @param video: ndarray, (#frame, h, w, 3), rgb
        @param size: int, target pixel size
        """
        process = Compose(
            [
                Resize(size, interpolation=InterpolationMode.BICUBIC),
                CenterCrop(size),
                lambda img: img.convert("RGB"),
                ToTensor(),
                Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
            ]
        )

        video_tensor = torch.stack([process(Image.fromarray(v)) for v in video], dim=0)
        return video_tensor

    def batch_meanpooling(self, x):
        frame_max = x.shape[1]  # 12
        result = []
        for vector in x:
            result.append(vector.sum(axis=0) / frame_max)
        return np.array(result)

    def encode_frames_to_vector(self, frames: torch.Tensor):
        B, F, _, _, _ = frames.size()
        if "cuda" in self._device or self._device == "mps":
            frames = frames.to(self._device)
        x = self._model.get_visual_output(frames, None, shaped=False)
        if x.device.type == "cpu":
            x = x.detach().numpy()
        else:
            x = x.cpu().detach().numpy()
        # meanpooling 진행하기 위해 batch size와 frame 길이 를 기준으로 meanpooing
        x = x.reshape(B, F, x.shape[-1])  # (B*F, 512) --> (B, F, 512)
        x = self.batch_meanpooling(x)  # (B, F, 512) --> (B, 512)
        return x

    def encode_frames_gradcam(
        self, frames: Union[np.ndarray, List[np.ndarray]], text_vec: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        return c4.encode_video_with_gradcam(np.asarray(frames), text_vec, self._model)

    def encode_texts_to_vector(self, text_list: List[str]) -> np.ndarray:
        return c4.encode_text(text_list, self._model)

    def encode_texts_gradcam(
        self, text_list: List[str], video_vec: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        return c4.encode_text_with_gradcam(text_list, video_vec, self._model)

    def _load_model(self):
        self._clear_model()
        self._model = c4.load_model(self._device, self._model_file)
        logger.info(
            f"CLIP4Clip model loaded on {self._device} with {self._model_file}"
            if self._model_file is not None
            else "",
        )

    # release memory
    def _clear_model(self):
        if self._model is not None:
            del self._model
            if "cuda" in self._device:
                torch.cuda.empty_cache()
        self._model = None

    @staticmethod
    def tokenize(text_list: List[str]) -> List[List[str]]:
        return c4.tokenize(text_list)