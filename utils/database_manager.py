import cv2
import numpy as np
import pandas as pd
import torch
from elasticsearch import Elasticsearch

from models.c4c import Clip4Clip
from utils.data import get_videos_labels
from device import get_device
from tiling import preprocess_input_image
from utils.io import load_json, load_yaml
from utils.log import Logger

logger = Logger(__file__)


def before_putDB(
    prompt_file_path: str,
    video_file_path: str,
    model_file: str,
    id: str,
    pw: str,
    prompt_index: str,
    video_index: str,
    device: str = None,
):
    """
    DB 저장 작업을 시작하기 전에 필요한 데이터를 로드하고, 모델을 초기화한다.

    Args:
        prompt_file_path (str): prompt에 대한 yaml파일 경로
        video_file_path (str): video에 대한 dir path
        model_file (str): model file 경로
        id (str): elasticsearch id
        pw (str): elasticsearch pw
        prompt_index (str): elasticsearch에 저장될 prompt index 지정
        video_index (str): elasticsearch에 저장될 video index 지정
        device (str):  "cpu", "mps", "cuda" 중에 하나
    Returns:
        client: elasticsearch의 client
        prompt_df (pd.DataFrame): prompt data의 dataframe
        video_data (list): video path 내 video data
        model (Clip4Clip): model
        prompt_index (str): prompt index name
        video_index (str): video index name
    """
    logger.info("DB 저장 작업을 시작합니다.")
    prompt_data = load_yaml(prompt_file_path)
    video_data = get_videos_labels(video_file_path)[0]
    prompt_df = pd.DataFrame(
        [(k, " ".join(v)) for k, v in prompt_data.items()], columns=["category", "prompts"]
    )
    device = get_device(device)
    model = Clip4Clip(device=device, model_file=model_file)
    client = Elasticsearch(["https://localhost:9200"], http_auth=(id, pw), verify_certs=False)
    prompt_index = None
    video_index = None
    # putDB의 인자들을 출력
    logger.info("DB input arguments:")
    for arg_name, arg_value in locals().items():
        logger.info(f"{arg_name}: {arg_value}")
    return client, prompt_df, video_data, model, prompt_index, video_index


def encode_prompt_vector(texts, model_type, model):
    """
    입력된 텍스트를 인코딩하여 벡터로 변환한다.
    """
    if model_type == "C4-fine-tuned":
        vectors = model.encode_texts_to_vector(texts)
        return vectors
    else:
        raise ValueError(f"Unsupported model type: {model_type}")


def insert_prompt_vector(client, prompt, vector, category, prompt_index):
    """
    prompt vector를 mapping.json format에 맞게 elasticsearch에 저장하는 코드.
    """
    mapping_file_path = "macs_profiler/cfg/DBvector/mapping_prompt.json"
    mapping = load_json(mapping_file_path)
    if not client.indices.exists(index=prompt_index):
        client.indices.create(index=prompt_index, body=mapping)
    client.index(
        index=prompt_index, body={"category": category, "prompt": prompt, "vector": vector.tolist()}
    )


def encode_video_vector(video_data, model_type, model):
    """
    비디오를 인코딩하여 벡터로 변환한다.
    프레임마다 인코딩된 벡터의 평균값을 512차원 벡터로 변환한다.
    """
    if model_type == "C4-fine-tuned":
        video_vectors = []
        for video in video_data:
            video_capture = cv2.VideoCapture(video)
            counter = 0
            fps = video_capture.get(cv2.CAP_PROP_FPS)
            while True:
                res, frame = video_capture.read()
                if not res:
                    break
                if counter % int(fps) == 0:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    tiles, wn, hn = preprocess_input_image(
                        model, frame, tile_size=224, margin_size=0
                    )
                    frame = torch.tensor(np.array([tiles]))
                    frame = frame.permute((1, 0, 2, 3, 4)).contiguous()
                    vectors = model.encode_frames_to_vector(frame)
                    if isinstance(vectors, torch.Tensor):
                        vectors = vectors.cpu().numpy()
                    mean_vector = np.mean(vectors, axis=0)
                    video_vectors.append({"vector": mean_vector.flatten().tolist()})
                counter += 1
            video_capture.release()
        return video_vectors


def insert_video_vector(client, video_name, vectors, category, video_index):
    """
    video vector를 mapping.json format에 맞게 elasticsearch에 저장하는 코드.
    """
    mapping_file_path = "macs_profiler/cfg/DBvector/mapping_video.json"
    mapping = load_json(mapping_file_path)
    if not client.indices.exists(index=video_index):
        client.indices.create(index=video_index, body=mapping)
    for i, vector_info in enumerate(vectors):
        client.index(
            index=video_index,
            body={
                "category": category,
                "video_name": video_name,
                "frame_index": i,
                "video_vector": vector_info["vector"],
            },
        )


def putting_prompt_DB(client, prompt_df, model, prompt_index):
    """
    prompt vector를 elasticsearch에 저장한다.
    """
    model_type = "C4-fine-tuned"
    for idx, row in prompt_df.iterrows():
        vectors = encode_prompt_vector([row["prompts"]], model_type, model)
        insert_prompt_vector(
            client, row["prompts"], vectors[0], row["category"], prompt_index="prompt_vectors"
        )
    logger.info(f"{prompt_index}에 prompt vector 저장 작업을 완료하였습니다.")


def putting_video_DB(client, video_data, model, video_index):
    """
    video vector를 elasticsearch에 저장한다.
    """
    model_type = "C4-fine-tuned"
    vectors = encode_video_vector(video_data, model_type, model)
    insert_video_vector(client, video_data, vectors, "Fire", video_index="video_vectors")
    logger.info(f"{video_index}에 video vector 저장 작업을 완료하였습니다.")


def search_prompt_API(client):
    """
    prompt DB에서 입력 Query에 따른 검색을 실행하고 이를 출력한다.
    """
    prompt_index = "prompt_vectors"
    body = {"size": 1, "query": {"match_all": {}}}
    res = client.search(index=prompt_index, body=body)
    print(res)


def search_video_API(client):
    """
    video DB에서 입력 Query에 따른 검색을 실행하고 이를 출력한다.
    """
    video_index = "video_vectors"
    body = {"size": 1, "query": {"match_all": {}}}
    res = client.search(index=video_index, body=body)
    print(res)
